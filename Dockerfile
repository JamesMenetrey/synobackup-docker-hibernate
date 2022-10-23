FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    zlib1g-dev \
    upx \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD pyinstaller --distpath ./singlefolder --workpath ./singlefolder-build --specpath ./singlefolder --noconfirm synobackup_docker_interrupt.py && \
    pyinstaller --distpath ./singlefile --workpath ./singlefile-build --specpath ./singlefile --onefile --noconfirm synobackup_docker_interrupt.py