FROM ubuntu:20.04

RUN apt-get update && apt-get -y install sudo
RUN apt-get upgrade -y
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install wget unzip curl build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev alien -y

RUN sudo adduser --disabled-password --gecos "" docuser

RUN mkdir /home/docuser/Tools

RUN mkdir /home/docuser/Tools/Python && cd /home/docuser/Tools/Python && wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz && tar -xvf Python-3.10.4.tgz && cd Python-3.10.4 && ./configure --enable-optimizations && make -j $(nproc) && make altinstall
ENV PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.10;/usr/local/lib/python3.10/bin
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

RUN mkdir /home/docuser/Tools/chrome && cd /home/docuser/Tools/chrome && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && apt-get install ./google-chrome-stable_current_amd64.deb -y

RUN mkdir /home/docuser/Tools/SCNR
RUN cd /home/docuser/Tools/SCNR && wget https://downloads.ecsypno.com/scnr-1.0dev-1.0dev-1.0dev-linux-x86_64.tar.gz && tar -xvf scnr-1.0dev-1.0dev-1.0dev-linux-x86_64.tar.gz

RUN mkdir /home/docuser/Tools/NMap
RUN cd /home/docuser/Tools/NMap && wget https://nmap.org/dist/nmap-7.92-1.x86_64.rpm && alien nmap-7.92-1.x86_64.rpm && dpkg --install nmap_7.92-2_amd64.deb

RUN mkdir /home/docuser/Tools/OWASP
RUN cd /home/docuser/Tools/OWASP && wget https://github.com/jeremylong/DependencyCheck/releases/download/v7.1.0/dependency-check-7.1.0-release.zip && unzip dependency-check-7.1.0-release.zip

RUN mkdir /home/docuser/Tools/SonarScanner
RUN cd /home/docuser/Tools/SonarScanner && wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.7.0.2747-linux.zip && unzip sonar-scanner-cli-4.7.0.2747-linux.zip

RUN mkdir /home/docuser/Orchestration
COPY ./ /home/docuser/Orchestration
WORKDIR /home/docuser/Orchestration
RUN pip3.10 install -r requirements.txt
ENV PATH=$PATH:/home/docuser/Orchestration;$PYTHONPATH;/home/docuser/Tools/SonarScanner/sonar-scanner-4.7.0.2747-linux/bin
RUN chown -R docuser /home/docuser/Orchestration/
RUN chmod 777 /home/docuser/Orchestration/
USER docuser
CMD ["python3.10", "/home/docuser/Orchestration/webapps/WebAutomation.py", "-u", "http://172.31.3.192/DVWA/", "-l", "linux"]