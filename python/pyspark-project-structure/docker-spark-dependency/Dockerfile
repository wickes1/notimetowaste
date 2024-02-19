FROM amazoncorretto:8u392

# Add Dependencies for PySpark
RUN yum -y update && yum install -y curl vim software-properties-common ssh net-tools ca-certificates tar procps hostname gcc openssl-devel bzip2-devel libffi-devel zlib-devel wget make

RUN wget https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tgz && tar -xf Python-3.9.13.tgz && cd Python-3.9.13 && ./configure --enable-optimizations && make install
RUN pip3 install --upgrade pip

RUN yum install -y zip

RUN mkdir /project_files
WORKDIR /project_files
