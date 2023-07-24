import os
import subprocess
from pydub import AudioSegment

def get_audio_format(file_path):
    _, ext = os.path.splitext(file_path)
    return ext[1:]

def convert_audio_with_pydub(source_file, target_format):
    audio = AudioSegment.from_file(source_file)
    target_file = os.path.splitext(source_file)[0] + '.' + target_format
    # 指定更高的音频比特率（根据需要调整）
    audio.export(target_file, format=target_format, bitrate='128k')
    return target_file

def convert_audio_with_ffmpeg(source_file, target_format):
    target_file = os.path.splitext(source_file)[0] + '.' + target_format
    command = ['ffmpeg', '-i', source_file, '-c:a', 'aac', '-strict', 'experimental', target_file]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.returncode == 0:
            return target_file
        else:
            print(f"转换失败：{result.stderr}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"转换失败：{e}")
        return None

def convert_audio(source_file, target_format):
    source_format = get_audio_format(source_file)
    if source_format == target_format:
        print("源格式和目标格式相同，无需转换。")
        return None

    try:
        target_file = os.path.splitext(source_file)[0] + '.' + target_format

        # Check if the target file already exists
        if os.path.exists(target_file):
            overwrite = input(f"文件 '{target_file}' 已存在。是否删除并覆盖？(y/n): ")
            if overwrite.lower() == 'y':
                os.remove(target_file)
            else:
                print("转换已取消。")
                return None

        if target_format == 'm4a':
            return convert_audio_with_ffmpeg(source_file, target_format)
        else:
            return convert_audio_with_pydub(source_file, target_format)
    except Exception as e:
        print(f"转换失败：{e}")
        return None

def main():
    print("欢迎使用音频格式转换工具！输入 'o' 可退出程序。")

    while True:
        source_file = input("请输入源文件名: ")
        if source_file.lower() == 'o':
            print("程序已退出。")
            break

        if not os.path.isfile(source_file):
            print("文件不存在，请重新输入。")
            continue

        source_format = get_audio_format(source_file)
        if not source_format:
            print("无法识别源文件格式，请输入支持的音频格式。")
            continue

        target_format = input("请输入目标转换格式: ")
        if target_format.lower() == 'o':
            print("程序已退出。")
            break

        if target_format not in ['wav', 'mp3', 'flac', 'm4a']:
            print("不支持的目标格式，请输入支持的音频格式。")
            continue

        try:
            target_file = convert_audio(source_file, target_format)
            if target_file:
                print(f"文件已成功转换为 {target_format} 格式：{target_file}")
        except Exception as e:
            print(f"转换失败：{e}")

if __name__ == "__main__":
    main()