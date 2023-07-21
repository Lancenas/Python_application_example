import os
import librosa
import scipy
import soundfile as sf

def load_audio(filepath):
    data, samplerate = sf.read(filepath)
    return data, samplerate

audio_file = '80-90年代经典老歌尽在-经典老歌500首一人一首成名曲.wav'
output_dir = '/Users/lixiao/Desktop/80-90'
silence_threshold = -30

# 载入音频
y, sample_rate = load_audio(audio_file)

# 检测静音片段
silence_segments = librosa.effects.split(y, top_db=silence_threshold)

# 切割音频并导出
for i, segment in enumerate(silence_segments):
    start_sample, end_sample = segment
    chunk = audio[start_sample:end_sample]

    # 构造输出文件路径
    output_path = os.path.join(output_dir, f"{i}.wav")

    # 导出音频
    librosa.output.write_wav(output_path, chunk, sample_rate)

print('Processing completed!')