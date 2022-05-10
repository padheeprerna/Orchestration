# set python base image (host OS)
FROM python:3.10

# set the working directory in the container
WORKDIR /home/ubuntu/Orchestration

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY ./webapps ./webapps

# copy the content of the local lib directory to the working directory
COPY ./lib ./lib

# copy the content of the local test directory to the working directory
COPY ./webappsSonar ./webappsSonar

#set PYTHONPATH and other ENV variables
#ENV PATH="C:/Orchestration/sonar-scanner-cli-4.7.0.2747-windows/sonar-scanner-cli-4.7.0.2747-windows/bin"
ENV PYTHONPATH="/home/ubuntu/Orchestration"

# command to run on container start
CMD [ "python", "./webapps/WebAutomation.py", "-u", "http://172.31.33.131/dvwa/index.php", "-n", "admin", "-p", "password", "-l", "linux"]


