import json
from flask import Flask, request
from flask_jwt import JWT, jwt_required
from services.auth import authenticate, identity
from services.gsheet import GoogleSheetService
from services.storage import StorageService
from models.record import Record
from datetime import datetime
import os

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'random-string'
app.config['JWT_AUTH_ENDPOINT'] = 'Bearer'
jwt = JWT(app, authenticate, identity)
sheet_service = GoogleSheetService()
storage_service = StorageService()


@app.route('/')
def health_check():
    return 'Success'


@app.route('/prompts', methods=['GET'])
@jwt_required()
def get_prompts():
    prompts = json.load(open('assets/prompts.json', 'r'))
    return {'prompts': prompts}


@app.route('/recordings', methods=['POST'])
@jwt_required()
def post_recording():
    # Upload wav file to storage, temporarily saving to file
    recording = request.files['file']
    filename = datetime.now().strftime("%d-%m-%y-%H:%M:%S")
    recording.save(f'tmp/{filename}.wav')
    storage_service.upload(filename)
    os.remove(f'tmp/{filename}.wav')

    # Process in DTO
    record = Record(request.form, filename)

    # Save record to database
    sheet_service.add_result(record.dump())
    return {'result': 'success'}
