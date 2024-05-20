FROM ubuntu:22.04

WORKDIR /

COPY . /

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev libpq-dev && \
    pip3 install --no-cache-dir -r requirements.txt

# Ensure that Python and Pip point to Python3 versions
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1


# REQUIRE ENV variables on runtime
#DB_USER
#DB_PASS
#DB_HOST
#DB_PORT
#DB_NAME

EXPOSE 8082

CMD ["python", "run.py"]

