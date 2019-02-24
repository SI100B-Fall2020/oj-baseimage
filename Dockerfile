FROM ubuntu:16.04

# Proudly served by GeekPie Association and SIST @ ShanghaiTech
RUN sed -i 's/archive.ubuntu.com/mirrors.geekpie.club/' /etc/apt/sources.list

# install dependencies of sandbox and scripts
RUN apt-get update && apt-get install -y cmake python3 python3-pip libseccomp-dev gcc g++

# Install sandbox
COPY qdujudger /tmp/qdujudger
RUN cd /tmp/qdujudger && \
	cmake . && \
	make && \
	make install && \
	rm -rf /tmp/qdujudger

# you can add dependencies from other kind of repositories as well.
# Just prefix the installation command with RUN,
# and make sure the package manangement tool is installed
RUN pip3 install pip

# /test will hold test output, but it's not mandatory nor hardcoded
# /submission will hold student submission and this name is mandatory and hardcoded
RUN mkdir /test /submission

# Copy the grading scripts
COPY *.awk *.sh *.py /judge/
COPY grade /judge/grade
RUN chmod +x /judge/*.sh && chmod +x /judge/*.py

# Generate the test samples
# While in this case it's static,
# you could replace it with a reference implementation running on testcases.
# The process of this genenration will run on your provided judging server(s)
# and its result will be cached.
RUN python3 /judge/grade/generate_sample.py > /test/input

ENTRYPOINT /judge/entry-point.sh

