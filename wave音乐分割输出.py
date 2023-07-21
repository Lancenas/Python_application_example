import os
import librosa
import soundfile as sf
import datetime


def split_music():
    # 获取输入音频文件名
    input_file = input("请输入音频文件名（包含文件路径）：")

    # 获取输出文件夹路径
    output_folder = input("请输入输出文件夹路径：")

    # 获取最小静音时长
    min_silence_duration = float(input("请输入最小静音时长（单位：秒）："))

    # 获取最小音量分贝数
    min_volume_db = float(input("请输入最小音量分贝数："))

    # 读取音频文件和采样率
    audio, sr = librosa.load(input_file, sr=None)

    segment_list = []
    for i, (start, end) in enumerate(librosa.effects.split(audio, top_db=min_volume_db)):
        duration = (end - start) / sr

        if duration >= min_silence_duration:
            segment_number = i + 1
            segment_start_time = str(datetime.timedelta(seconds=int(start / sr)))
            segment_end_time = str(datetime.timedelta(seconds=int(end / sr)))
            segment_duration = duration
            segment_size = (end - start) * audio.itemsize / (1024 * 1024)  # 转换为MB

            segment_list.append((segment_number, segment_start_time, segment_end_time, segment_duration, segment_size))

    while True:
        for segment in segment_list:
            segment_number, segment_start_time, segment_end_time, segment_duration, segment_size = segment
            print(
                f"{segment_number}. {segment_start_time}-{segment_end_time} (时长: {segment_duration:.2f}秒, 大小: {segment_size:.2f}MB)")

        choice = input("请选择分割方式（输入序号分割；输入'a'选择全部输出；输入's'自定义分割方式；输入'o'退出）：")

        if choice == 'o':
            break

        if choice.isdigit():
            selected_segments = [int(choice)]
            for segment in segment_list:
                segment_number, segment_start_time, segment_end_time, _, _ = segment
                if segment_number in selected_segments:
                    segment_name = input("请输入分割段的自设定文件名：")
                    segment_name = segment_name.replace(':', '-')  # 替换':'为'-'

                    output_name = f"{segment_name}.wav"
                    output_path = os.path.join(output_folder, output_name)

                    start = int(segment_start_time.split(":")[0]) * 3600 + int(
                        segment_start_time.split(":")[1]) * 60 + int(segment_start_time.split(":")[2])
                    end = int(segment_end_time.split(":")[0]) * 3600 + int(segment_end_time.split(":")[1]) * 60 + int(
                        segment_end_time.split(":")[2])

                    segment = audio[start * sr:end * sr]

                    sf.write(output_path, segment, sr)

                    print(f"保存文件: {output_name}")
        elif choice == 'a':
            segment_name = input("请输入分割段的自设定文件名：")
            segment_name = segment_name.replace(':', '-')  # 替换':'为'-'

            for segment in segment_list:
                segment_number, segment_start_time, segment_end_time, _, _ = segment
                output_name = f"{segment_name}_{segment_number}.wav"
                output_path = os.path.join(output_folder, output_name)

                start = int(segment_start_time.split(":")[0]) * 3600 + int(segment_start_time.split(":")[1]) * 60 + int(
                    segment_start_time.split(":")[2])
                end = int(segment_end_time.split(":")[0]) * 3600 + int(segment_end_time.split(":")[1]) * 60 + int(
                    segment_end_time.split(":")[2])

                segment = audio[start * sr:end * sr]

                sf.write(output_path, segment, sr)

                print(f"保存文件: {output_name}")
        elif choice == 's':
            start_time_str = input("请输入分割开始时间（格式：小时:分钟:秒）：")
            end_time_str = input("请输入分割结束时间（格式：小时:分钟:秒）：")

            segment_name = input("请输入分割段的自设定文件名：")
            segment_name = segment_name.replace(':', '-')  # 替换':'为'-'

            output_name = f"{segment_name}.wav"
            output_path = os.path.join(output_folder, output_name)

            start = int(start_time_str.split(":")[0]) * 3600 + int(start_time_str.split(":")[1]) * 60 + int(
                start_time_str.split(":")[2])
            end = int(end_time_str.split(":")[0]) * 3600 + int(end_time_str.split(":")[1]) * 60 + int(
                end_time_str.split(":")[2])

            segment = audio[start * sr:end * sr]

            sf.write(output_path, segment, sr)

            print(f"保存文件: {output_name}")

        continue_choice = input("是否继续选择分割方式？（输入'y'继续选择；输入其他任意键退出）：")
        if continue_choice.lower() != 'y':
            break

    print("分割完成！")


# 调用分割函数
split_music()
