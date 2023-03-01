from pydub import AudioSegment
DESIRED_SAMPLERATE = 16000

def get_audio_segment(file_path, ext='.wav'):
    if ext == '.wav':
        res = AudioSegment.from_wav(file_path)
    else:
        res = AudioSegment.from_file(file_path)
    return res

def get_channels(audio_seg):
    return audio_seg.channels

def export_to_1ch(audio_seg, dst_path):
    audio_seg = audio_seg.set_channels(1)
    audio_seg.export(dst_path, format='wav')

def resample_if_needed(aud_seg, save_path=None):
    if aud_seg.frame_rate != DESIRED_SAMPLERATE:
        aud_seg = aud_seg.set_frame_rate(DESIRED_SAMPLERATE)
        if save_path:
            aud_seg.export(save_path, format='wav')
    
    return aud_seg