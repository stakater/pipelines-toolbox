FROM registry.access.redhat.com/ubi8-minimal:8.1-407

RUN mkdir -p /projects

ENV GLIBC_VERSION=2.30-r0 \
    OC_VERSION=4.15 \
    KUBECTL_VERSION=v1.28.11 \
    TKN_VERSION=0.37.0 \
    MAVEN_VERSION=3.9.8 \
    NODEJS_VERSION=14 \
    JDK_VERSION=11 \
    YQ_VERSION=v4.44.3 \
    ARGOCD_VERSION=v2.8.4 \
    HELM_VERSION=3.15.3 \
    KUBECONFORM=v0.6.7 \
    ROX_VERSION=4.5.0 \
    ANSIBLE_VERSION=2.12.1 \
    SONAR_CLI_VERSION=6.1.0.4477 \
    HOME="/opt/root"\
    JAVA_TOOL_OPTIONS="-Djava.net.preferIPv4Stack=true"
    
# Create Home directory which has permissions for all users. issue https://github.com/tektoncd/pipeline/issues/2013
RUN mkdir $HOME

# add Nodejs Version to nodejs.module file
RUN echo -e "[nodejs]\nname=nodejs\nstream=$NODEJS_VERSION\nprofiles=\nstate=enabled\n" > /etc/dnf/modules.d/nodejs.module

# install packages
RUN microdnf install -y \
    bash curl wget tar gzip unzip java-${JDK_VERSION}-openjdk-devel git openssh which httpd python38 procps tar podman iptables openssl nodejs nodejs-nodemon npm findutils yum && \
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
    
RUN pip3 install requests && \
    echo "Installed requests package"

# install maven
ENV MAVEN_HOME /usr/lib/mvn
ENV PATH ${MAVEN_HOME}/bin:$PATH

RUN wget http://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz && \
  tar -zxvf apache-maven-$MAVEN_VERSION-bin.tar.gz && \
  rm apache-maven-$MAVEN_VERSION-bin.tar.gz && \
  mv apache-maven-$MAVEN_VERSION /usr/lib/mvn && \
    echo "Installed maven"

RUN wget -O jq https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 && \
   chmod +x ./jq && \
   mv jq /usr/bin
# configure Java
ENV JAVA_HOME ${GRAALVM_HOME}

# change permissions to let any arbitrary user
RUN for f in "/etc/passwd" "/projects"; do \
      echo "Changing permissions on ${f}" && chgrp -R 0 ${f} && \
      chmod -R g+rwX ${f}; \
    done

# install sonarqube scanner
RUN wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_CLI_VERSION}.zip && \
    unzip sonar-scanner-cli-${SONAR_CLI_VERSION}.zip && mv sonar-scanner-${SONAR_CLI_VERSION} /var/opt
ENV PATH="/var/opt/sonar-scanner-${SONAR_CLI_VERSION}/bin:${PATH}"
RUN echo "sonarqube-scanner installed"

# install unzip & buildah
RUN yum install buildah -y

# install aws cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    echo "Installed AWS CLI"

# install kubeconform (https://github.com/yannh/kubeconform/releases)
RUN wget https://github.com/yannh/kubeconform/releases/download/$KUBECONFORM/kubeconform-linux-amd64.tar.gz && tar zxvf kubeconform-linux-amd64.tar.gz && \
    chmod +x kubeconform && mv kubeconform /usr/local/bin && \
    kubeconform -v && \
    echo "Installed kubeconform-"${KUBECONFORM}

# install ansible
RUN microdnf install -y \
    shadow-utils passwd
RUN useradd ansible; echo "Docker!" | passwd --stdin ansible
RUN echo "ansible ALL=(ALL) NOPASSWD: ALL ">> /etc/sudoers
RUN python3 -m pip install --user ansible && \
    pip3 install openshift pyyaml kubernetes && \
    PATH=$PATH:/opt/root/.local/bin && \
    ansible-galaxy collection install kubernetes.core

RUN /opt/root/.local/bin/ansible --version
# Install Ansible inventory file.
RUN mkdir -p /etc/ansible
RUN echo -e '[local]\nlocalhost ansible_connection=local' > /etc/ansible/hosts

# roxctl client
RUN curl -sL -o /usr/local/bin/roxctl https://mirror.openshift.com/pub/rhacs/assets/${ROX_VERSION}/bin/Linux/roxctl && \
    chmod +x /usr/local/bin/roxctl

# install yarn
RUN npm install -g yarn

RUN mkdir /scripts
COPY scripts /scripts/

RUN chmod -R a+rwx $HOME

WORKDIR /projects
