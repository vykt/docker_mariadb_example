# Using debian-slim
FROM debian:stable
MAINTAINER castile

# Installs
RUN apt update
RUN apt install -y requirements_apt.txt
RUN pip install requirements_pip.txt

ADD api.py /api.py

# Setup
EXPOSE 5000

# Run
ENTRYPOINT ["python3"]
CMD["api.py"]
