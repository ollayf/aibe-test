from pydub import AudioSegment

def get_audio_segment(file_path, file_type='wav'):
    if file_type == 'wav':
        res = AudioSegment.from_wav(file_path)
    else:
        res = AudioSegment.from_file(file_path)
    return res

def get_channels(audio_seg):
    res = audio_seg.get_sample_slice(0, 1).get_array_of_samples()
    return len(res)

def export_to_1ch(audio_seg, dst_path):
    audio_seg.export(dst_path, format='wav')