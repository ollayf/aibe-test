# Setup

## Requirements
- `pip install requirements.txt`

## Option 1: Run Inference server
- `docker load -i photon_server_v1.tar`
- run_docker.sh (on terminal 1)
    - Do not run gpu if you dont have nvidia container toolkit already installed
- python predict_server.py (on terminal 2)

## Option 2: Run ONNX
- python predict_ONNX.py