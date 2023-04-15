import json
from flask import Flask, request
from flask_jwt import JWT, jwt_required
from services.auth import authenticate, identity
from services.gsheet import GoogleSheetService
from services.drive_storage import DriveStorageService
from models.record import Record
from datetime import datetime
from flask_cors import CORS
import os
from deploy.predict_server import get_score, predict
import audio_utils
from pydub import AudioSegment
import os
import re

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

@app.route('/prompts/<path:file>/', methods=['GET'])
@jwt_required()
def get_prompts(file: str):

    NOT_ALPHANUMERIC_REGEX = "[^a-zA-Z0-9_]"    
    if re.search(NOT_ALPHANUMERIC_REGEX, file):
        return "Error: Invalid File Name. It can only be alphanumeric with _"

    file_path = f"./prompt_lists/{file}.json"

    if not os.path.exists(file_path):
        return f"Error: File not Found: {file}.", 404


    prompts = json.load(open(file_path, 'r'))
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
    RECORDING_TIME_LIMIT = 20 # seconds
    # Temporarily save file
    recording = request.files['file']
    filename = datetime.now().strftime("%d-%m-%y-%H:%M:%S")
    src_path = f'tmp/{filename}.wav'
    recording.save(src_path)
    ch1_path = f'tmp/{filename}-1ch.wav'

    aud_seg = audio_utils.get_audio_segment(src_path)
    if (audio_utils.get_audio_length(aud_seg) > RECORDING_TIME_LIMIT):
        return "Audio too long. Must not be above 20 seconds", 501
    converted = False
    channels = audio_utils.get_channels(aud_seg)

    # only saves 16KHz to save space
    aud_seg = audio_utils.resample_if_needed(aud_seg, src_path)

    if channels > 1:
        audio_utils.export_to_1ch(aud_seg, ch1_path)
        converted = True
        

    # Upload to storage bucket
    storage_service.upload(filename)

    if converted:
        file_for_inference = ch1_path
    else:
        file_for_inference = src_path
    
    # prediction = predict(ONNX_MODEL, file_for_inference)
    prediction, score = get_score(ONNX_MODEL, file_for_inference, 
        request.form["prompt"], grading_algo=request.form["grading_algo"])
    
    # Process in DTO and evaluate
    record = Record(request.form, filename)
    record._evaluate(score)

    # Save record to database
    sheet_service.add_result(record.dump())

    # Delete file
    os.remove(src_path)
    if converted:
        os.remove(ch1_path)

    return {'result': 'success', 'channels': channels, 'scores': score}
