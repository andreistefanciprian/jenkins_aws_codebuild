FROM jenkins/jenkins:2.235.1-lts-centos7

WORKDIR /var/tmp

USER root

COPY requirements.txt requirements.txt

RUN yum install -y python3 make \
&& pip3 install -r requirements.txt \
&& curl -sk https://releases.hashicorp.com/terraform/0.12.26/terraform_0.12.26_linux_386.zip -o /tmp/terraform_0.12.26_linux_386.zip \
&& unzip /tmp/terraform_0.12.26_linux_386.zip -d /usr/local/bin/