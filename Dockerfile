# Using debian-slim
FROM debian:bullseye
MAINTAINER castile

# Installs
RUN apt update

RUN apt install -y curl=7.74.0-1.3+deb11u1
RUN apt install -y python3-pip=20.3.4-4+deb11u1
RUN pip install flask==2.0.1
RUN pip install flask_restful==0.3.9
RUN pip install mysql-connector-python==8.0.29

#RUN apt install -y requirements_apt.txt
#RUN pip install requirements_pip.txt

ADD api.py /api.py

# Setup
EXPOSE 5000

# Run
ENTRYPOINT ["python3"]
CMD ["/api.py"]
