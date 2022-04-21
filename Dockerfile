# set python base image (host OS)
FROM python:3.10

# set the working directory in the container
WORKDIR /Orchestration

#COPY ./ ./

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY webapps/ ./webapps/

# copy the content of the local lib directory to the working directory
COPY lib/ ./lib/

# copy the content of the local test directory to the working directory
COPY webappsSonar/ ./webappsSonar/

#Copy SSLScan to Docker image
COPY SSLScan/ ./SSLScan/

#Copy OWASP Dep Check to Docker image
COPY dependency-check-7.0.4-release/ ./dependency-check-7.0.4-release/

#Copy Sonar Scanner to Docker image
COPY sonar-scanner-cli-4.7.0.2747-windows/ ./sonar-scanner-cli-4.7.0.2747-windows/

#Install NMap in Docker image
#FROM mcr.microsoft.com/windows/servercore:ltsc2019
COPY nmap-7.92-setup.exe/ .
RUN .\nmap-7.92-setup.exe

#Copy Arachni to Docker image
COPY arachni-1.6.1-0.6.1-windows-x86_64/ ./arachni-1.6.1-0.6.1-windows-x86_64/

#set PYTHONPATH and other ENV variables
ENV PATH "${PATH}:/Orchestration/sonar-scanner-cli-4.7.0.2747-windows/sonar-scanner-cli-4.7.0.2747-windows/bin"
ENV PYTHONPATH "${PYTHONPATH}:/Orchestration/"

# command to run on container start
CMD [ "python", "./webapps/WebAutomation.py", "-u", "http://172.31.33.131/dvwa/index.php", "-n", "admin", "-p", "password", "-l", "windows"]


