FROM python:3.8-slim-buster

WORKDIR /

RUN apt update
RUN apt install -y libsndfile1-dev espeak
RUN apt autoremove -y
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENV GRPC_DNS_RESOLVER=native
ENV GOOGLE_APPLICATION_CREDENTIALS=credentials.json
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]