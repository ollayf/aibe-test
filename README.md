# aibe-test

## Pending work
- integrate audio file predictor

## API usage
See [here](docs/README.md)

## Setup instructions

### 1. Create a google service account
This service account grants access to google sheets and google cloud buckets

https://cloud.google.com/iam/docs/creating-managing-service-accounts

Grant the account role 'Storage Object Admin'

Export the account key as a JSON ([instructions](https://stackoverflow.com/questions/46287267/how-can-i-get-the-file-service-account-json-for-google-translate-api))

Rename the JSON to `credentials.json` and store it in the root of this project.

### 2a. Create a storage bucket
See [here](https://cloud.google.com/storage/docs/creating-buckets)
After creating bucket, go to [storage.py]('services/storage.py') and add in
### 2b. Create a google sheet
Create a google sheet from the [following template](https://docs.google.com/spreadsheets/d/1T5P6UVy6jnTe_S9nnvUQ-P17xrCBq_rtQDOx1SttcD4/edit?usp=sharing) ['File' -> 'Make a copy']

Rename the google sheet to '[SHINE] AIBE test data' (name is hardcoded in [code](services/gsheet.py))

Grant edit access to the service account.

### 3. Run project
Create docker image

```docker build --tag shine-aibe .```

Run on http://localhost:5001

```docker run -d -p 5001:80 shine-aibe```

## Further works
1. Abstract env configuration file to safely store JWT secret
2. Swagger docs
3. Add a more robust class for google sheet: difficult to add new fields and ensure columns are 'aligned'
4. Fix hardcoding of google sheet name, project id, storage bucket (ideally done when env vars are set up)
5. Use production settings for app [ref](https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/)

## Dependencies
### If you are testing it locally
- Python: requirements.txt
- Ubuntu:
    - espeak
    - libsndfile1-dev
- nvidia-container-toolkit (GPU Accelerated Inference)
- Get credentials file and docker
### If you are using docker
- docker (20.10.12)
- docker-compose (2.14.2)
- nvidia-container-toolkit (GPU Accelerated Inference)
## Main system
- Ubuntu 20.04
- NVIDIA GPU (Compute Capability 6.0)
- x86_64 Architecture
- AMD CPU

## Quick Setup

### Install Depedencies
```
sudo apt update

# docker and docker-compose
sudo snap install docker
sudo curl -L "https://github.com/docker/compose/releases/download/2.14.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# espeak
sudo apt install espeak
```


### Docker compose
This is the quickest way to set everything up  
Firstly, load the docker image of the inference server  
`docker load < <inference_server>.tar`
Then, build the image for the endpoint server using:  
`docker build -t shine_aibe:v1 .`
Set up both containers together (detach mode)
`docker-compose up -d`

## When making edits
You wouldn't usually make edits to the inference server since I've built a custom image, so I will omit details here

### Endpoint server
After edits, run:  
`docker build -t shine_aibe:v1 .`

### Locally on your PC
Firstly, ensure that all dependencies are installed  
Edit the URL in this function [script](deploy/predict_server.py).  
- For docker: "172.28.1.1:8001"
- For local hosting: "localhost:8001"