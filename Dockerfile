FROM registry.access.redhat.com/ubi8-minimal:8.1-407

RUN mkdir -p /projects

ENV GLIBC_VERSION=2.30-r0 \
    OC_VERSION=4.8 \
    KUBECTL_VERSION=v1.20.6 \
    TKN_VERSION=0.20.0 \
    MAVEN_VERSION=3.6.3 \
    NODEJS_VERSION=14 \
    JDK_VERSION=11 \
    YQ_VERSION=v4.22.1 \
    ARGOCD_VERSION=v2.1.5 \
    HELM_VERSION=3.6.1 \
    JAVA_TOOL_OPTIONS="-Djava.net.preferIPv4Stack=true"

# add Nodejs Version to nodejs.module file
RUN echo -e "[nodejs]\nname=nodejs\nstream=$NODEJS_VERSION\nprofiles=\nstate=enabled\n" > /etc/dnf/modules.d/nodejs.module

# install packages
RUN microdnf install -y \    
    bash curl wget tar gzip unzip java-${JDK_VERSION}-openjdk-devel git openssh which httpd python36 procps tar podman iptables openssl nodejs nodejs-nodemon npm findutils yum && \
    microdnf -y clean all && rm -rf /var/cache/yum && \
    echo "Installed packages" && rpm -qa | sort -V && echo "End Of Installed Packages"

# install oc
RUN wget -qO- https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable-${OC_VERSION}/openshift-client-linux.tar.gz | tar xvz -C /usr/local/bin && \
    oc version --client && \
    echo "Installed oc"

# install kubectl
ADD https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl /usr/local/bin/kubectl
RUN chmod +x /usr/local/bin/kubectl && \
    kubectl version --client && \
    echo "Installed kubectl"

# install tekton cli
RUN wget -qO- https://github.com/tektoncd/cli/releases/download/v${TKN_VERSION}/tkn_${TKN_VERSION}_Linux_x86_64.tar.gz | tar xvz -C /usr/local/bin && \
    tkn version && \
    echo "Installed tekton"

# install yq
RUN wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64 && \
    chmod +x /usr/local/bin/yq && \
    echo "Installed yq"

# install argocd
RUN wget -qO /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/download/${ARGOCD_VERSION}/argocd-linux-amd64 && \
    chmod +x /usr/local/bin/argocd && \
    echo "Installed argocd"

# install helm
RUN cd /tmp && \
    wget -q https://get.helm.sh/helm-v${HELM_VERSION}-linux-amd64.tar.gz && \
    tar -xvf helm-v${HELM_VERSION}-linux-amd64.tar.gz && \
    chmod +x linux-amd64/helm && \
    mv linux-amd64/helm /usr/local/bin/ && \
    rm -rf ./* && \
    echo "Installed helm"

# install jinja2 cli
RUN pip3 install j2cli && \
    echo "Installed jinja2 cli"

# install maven
ENV MAVEN_HOME /usr/lib/mvn
ENV PATH ${MAVEN_HOME}/bin:$PATH

RUN wget http://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz && \
  tar -zxvf apache-maven-$MAVEN_VERSION-bin.tar.gz && \
  rm apache-maven-$MAVEN_VERSION-bin.tar.gz && \
  mv apache-maven-$MAVEN_VERSION /usr/lib/mvn && \
    echo "Installed maven"


# configure Java
ENV JAVA_HOME ${GRAALVM_HOME}

# change permissions to let any arbitrary user
RUN for f in "/etc/passwd" "/projects"; do \
      echo "Changing permissions on ${f}" && chgrp -R 0 ${f} && \
      chmod -R g+rwX ${f}; \
    done

# Install sonarqube scanner
RUN wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-linux.zip && \
  unzip sonar-scanner-cli-4.2.0.1873-linux.zip  && \
  mv sonar-scanner-4.2.0.1873-linux /var/opt
ENV PATH="/var/opt/sonar-scanner-4.2.0.1873-linux/bin:${PATH}"
RUN echo "sonarqube-scanner installed"

# install unzip & buildah
RUN yum install buildah -y

# install aws cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    echo "Installed AWS CLI"

# install yarn
RUN npm install -g yarn

# install chromium
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
RUN dnf install -y chromium
    
WORKDIR /projects
