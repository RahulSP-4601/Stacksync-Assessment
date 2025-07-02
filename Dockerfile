FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    clang \
    libprotobuf-dev \
    libnl-route-3-dev \
    libcap-dev \
    libseccomp-dev \
    protobuf-compiler \
    pkg-config \
    flex \
    bison \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/google/nsjail.git && \
    cd nsjail && make && cp nsjail /usr/local/bin/ && cd .. && rm -rf nsjail

WORKDIR /app
COPY app/ app/
COPY scripts/ scripts/
COPY nsjail.cfg .

EXPOSE 8080

CMD ["python", "app/main.py"]

ENV USE_NSJAIL=false