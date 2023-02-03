import utils

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import torch
import soundfile as sf
import torch.onnx
import onnx
import onnxruntime as ort
import numpy as np
import time
from phonemizer import phonemize, separator

def predict(model_path, audio_file):

    # read audio file into (1, ?) numpy array
    waveform, _ = sf.read(audio_file)
    # load model and processor
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")
    # print(onnx.checker.check_model(onnx_model))
    # 'TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider'
    ort_sess = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider'])
    input_values = processor(waveform, return_tensors="pt").input_values.numpy()
    outputs = ort_sess.run(['modelOutput'], {'modelInput': input_values})
    predicted_ids = np.argmax(outputs[0], axis=-1)
    transcription = processor.decode(predicted_ids[0])
    return transcription

def get_score(model_path, audio_file, correct):
    transcription = predict(model_path, audio_file)
    sp =  separator.Separator(phone=' ', word='')
    ref = phonemize(correct, separator=sp)

    return utils.wer2(ref, transcription, False)['acc']


if __name__ == '__main__':
    # ONNX_MODEL = 'onnx_exports/w2v2p2.onnx'
    ONNX_MODEL = './model_repository/phoneme1/1/w2v2p2.onnx'
    AUDIOFILE='a_fat_cat_aaron.wav'
    # print(predict(ONNX_MODEL, AUDIOFILE))
    print(get_score(ONNX_MODEL, AUDIOFILE, 'a fat cat'))