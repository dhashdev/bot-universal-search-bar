FROM python:3.9.16-slim-buster

# Tiktoken requires Rust toolchain, so build it in a separate stage
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    dpkg-sig \
    python3-dev 

RUN pip install --upgrade pip && pip install tiktoken==0.4.0

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD [ "uvicorn", "api.app:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]