'''
Module : openapi2json-schema-build-script.py
This utility extracts openapi spec file, 
extracts definitions and creates seprate 
json schemas for cluster resources 
'''
from shutil import which
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import argparse
import os
import urllib
import sys
import urllib
import ssl
import yaml
import json
import subprocess
def getArgumentParser():
    """
    argumentParser : returns arguement parser object
    ()
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", action="store", dest="url",
                        required=True, help="OpenShift API URL")
    parser.add_argument("-t", "--token", action="store",
                        dest="token", required=True, help="OpenShift API Token")
    parser.add_argument("-d", "--destination", action="store",
                        dest="destination", required=True, help="Output file")
    return parser

def getSSLContext():
    '''
    getSSLContext : return ssl context object
    ()
    '''
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def loadYAML(url,token):
    '''
    loadYAML : get openapi spec from openshift openapi endpoint 
    (
        url : openshift openapi url
        token: openshift token
    )
    '''
    headers = {"Authorization": "Bearer {}".format(token)}
    # Send request to server
    req = urllib.request.Request(url=url, headers=headers)
    try:
        res = urllib.request.urlopen(req, context=getSSLContext())
        # Return request payload
        return yaml.load(res.read(), Loader=yaml.SafeLoader)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        sys.exit(1)
    except URLError as e:
        print('Failed to reach a server.')
        print('Reason: ', e.reason)
        sys.exit(1)

def removeInvalidCRDs(openapi_data):
    '''
    removeInvalidCRDs : removes definitions without properties key as they are invalid
    (
        openapi_data : dict
    )
    '''
    definitions = openapi_data["definitions"]
    delete_list = []
    for type_name in definitions:
        type_def = definitions[type_name]
        if "x-kubernetes-group-version-kind" in type_def:
            for kube_ext in type_def["x-kubernetes-group-version-kind"]:
                if "properties" not in type_def:
                    delete_list.append(type_name)
    print("The following API resources have invalid OpenAPI specifications:\n")
    for del_item in delete_list:
        print(del_item)
        del definitions[del_item]
    with open("openshift-api-spec.json", "w") as openapi_spec_file:
        openapi_spec_file.write(json.dumps(openapi_data, indent=2))

def runOpenApi2Json(output_destination): 
    '''
    runOpenApi2Json : Run openapi2jsonschema (https://github.com/instrumenta/openapi2jsonschema) over the spec file
    (
        output_destination: output folder
    )
    '''
    openapi2jsonschema_location = which("openapi2jsonschema")
    command = [openapi2jsonschema_location,"-o",
              output_destination, "--expanded", "--kubernetes","--stand-alone", "openshift-api-spec.json"]

    print("\nProcessing schemas into {}\n".format(output_destination))
    job = subprocess.Popen(
        command,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
    )
    try:
        (stdout, stderr) = job.communicate(timeout=300)
    except subprocess.TimeoutExpired:
        job.kill()
        (stdout, stderr) = job.communicate()
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")
    print("[STDERR]: %s" % stderr)
    print("[STDOUT]: %s" % stdout)

def main(args):
    '''
    main:(args)
    '''
    # API endpoint ( https://api.devtest.kubeapp.cloud:6443/openapi/v2 )
    openapi_endpoint = "{}/openapi/v2".format(args.url)
    # API Token ( sha )
    oc_token = args.token
    # Schemas directory ( path)
    destination= args.destination
    
    print("Getting OpenAPI Spec from server...................")
    openapi_data = loadYAML(openapi_endpoint,oc_token)     

    # Remove invalid definitions     
    print("Removing Invalid resources from OpenAPI Spec.......")
    removeInvalidCRDs(openapi_data)
    
    # Convert spec file to seprate json schemas
    print("Converting spec file to seprate schemas............")
    runOpenApi2Json(destination)

if __name__ == "__main__":
    args = getArgumentParser().parse_args()
    main(args)
