FROM python:3.10-slim

# Install dependencies for nsjail and other system packages
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

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install nsjail from source
RUN git clone https://github.com/google/nsjail.git && \
    cd nsjail && make && cp nsjail /usr/local/bin/ && cd .. && rm -rf nsjail

# Set working directory and copy project files
WORKDIR /app
COPY app/ app/
COPY scripts/ scripts/
COPY nsjail.cfg .

# Expose Flask app port
EXPOSE 8080

# Run the Flask app
CMD ["python", "app/main.py"]
