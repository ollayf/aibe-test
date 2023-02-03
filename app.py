import json
from flask import Flask, request
from flask_jwt import JWT, jwt_required
from services.auth import authenticate, identity
from services.gsheet import GoogleSheetService
from services.storage import StorageService
from services.drive_storage import DriveStorageService
from models.record import Record
from datetime import datetime
from flask_cors import CORS
import os
from deploy.predict_server import get_score

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'random-string'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
jwt = JWT(app, authenticate, identity)
sheet_service = GoogleSheetService()
storage_service = DriveStorageService()
print("Created everything")


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
    '''
    Other than standard form components, form needs:
    - grading_algo: wer/ wer2 
    - prompt: <String>
    '''
    ONNX_MODEL = 'phoneme1'
    # Temporarily save file
    recording = request.files['file']
    filename = datetime.now().strftime("%d-%m-%y-%H:%M:%S")
    recording.save(f'tmp/{filename}.wav')

    # Upload to storage bucket
    storage_service.upload(filename)

    # Process in DTO and evaluate
    record = Record(request.form, filename)
    print(request.form)
    print(type(request.form))

    # Save record to database
    sheet_service.add_result(record.dump())
    score = get_score(ONNX_MODEL, f'tmp/{filename}.wav', 
        request.form["prompt"], grading_algo=request.form["grading_algo"])
    # Delete file
    os.remove(f'tmp/{filename}.wav')

    return {'result': 'success', 'scores': score}