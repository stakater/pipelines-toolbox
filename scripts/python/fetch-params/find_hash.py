from fetch_params_bitbucket import fetch_params_bitbucket
from fetch_params_github import fetch_params_github
import argparse

def find_hash(provider, username, password, hash, workspace, repository):
  pr_number = None
  if provider == "bitbucket":
    pr_number = fetch_params_bitbucket(provider, username, password, hash, workspace, repository)
  elif provider == "github":
    pr_number = fetch_params_github(provider, username, password, hash, workspace, repository)
  return pr_number
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("provider", help="Name of git provider")
    parser.add_argument("username", help="Username for git provider")
    parser.add_argument("password", help="Password/Token for provider")
    parser.add_argument("hash", help="Hash of the commit that triggered the pipeline")
    parser.add_argument("workspace", help="Workspace/Organization")
    parser.add_argument("repository",  help="Git repository name")
    args = parser.parse_args()
    pr_number = find_hash(args.provider, args.username, args.password, args.hash, args.workspace, args.repository)
    print(pr_number)