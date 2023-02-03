import tritonclient.grpc as grpcclient

from .utils import wer2, wer
from phonemizer import phonemize, separator

#NEW STUFF
import numpy as np

import os

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import soundfile as sf
import numpy as np
import time
import sys

def predict(model_path, audio_file):

    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")
    waveform, _ = sf.read(audio_file)
    input_values = processor(waveform, return_tensors="pt").input_values
    input_values = input_values.numpy()

    triton_client = grpcclient.InferenceServerClient(
            url='localhost:8001',
            verbose=False,
            ssl=False,
            root_certificates=None,
            private_key=None,
            certificate_chain=None)

    input = grpcclient.InferInput('modelInput', input_values.shape, "FP32")

    input.set_data_from_numpy(input_values)
    output = grpcclient.InferRequestedOutput('modelOutput')
    results = triton_client.infer(
        model_name=model_path,
        inputs=[input],
        outputs=[output],
        client_timeout=None,
        headers={'test': '1'},
        compression_algorithm=None)
    
    output0_data = results.as_numpy('modelOutput')

    predicted_ids = np.argmax(output0_data, axis=-1)
    transcription = processor.decode(predicted_ids[0])
    return transcription
    

def get_score(model_path, audio_file, correct, grading_algo):
    transcription = predict(model_path, audio_file)
    sp =  separator.Separator(phone=' ', word='')
    ref = phonemize(correct, separator=sp)
    if grading_algo == "wer2":
        return wer2(ref, transcription, False)
    else:
        return wer(ref, transcription, False)


if __name__ == '__main__':
    # ONNX_MODEL = 'onnx_exports/w2v2p2.onnx'
    ONNX_MODEL = 'phoneme1'
    AUDIOFILE='deploy/a_fat_cat_aaron.wav'
    # print(predict(ONNX_MODEL, AUDIOFILE))
    start = time.time()
    print(get_score(ONNX_MODEL, AUDIOFILE, 'a fat cat'))
    print("Time Taken:", time.time() - start)