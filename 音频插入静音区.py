from pydub import AudioSegment
import os
import datetime

def convert_to_milliseconds(time_str):
    # 将时间字符串转换为毫秒
    time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S")
    total_milliseconds = (time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second) * 1000
    return total_milliseconds

def insert_silence(input_file, output_file, start_times, duration_ms):
    # 加载音频文件
    audio = AudioSegment.from_file(input_file)

    # 在指定时间点插入静音
    for start_time in start_times:
        start_time_ms = convert_to_milliseconds(start_time)
        silence = AudioSegment.silent(duration=duration_ms)
        audio = audio[:start_time_ms] + silence + audio[start_time_ms:]

    # 导出到输出文件
    audio.export(output_file, format=os.path.splitext(output_file)[1][1:])  # 保留输出文件的格式

if __name__ == "__main__":
    input_file_path = input("请输入输入音频文件路径：")
    output_file_path = input("请输入输出音频文件路径：")

    start_times_input = input("请输入静音区的开始时间（格式为00:00:00），多个时间用逗号分隔：")
    start_times = start_times_input.split(",")  # 用逗号分割多个输入的start_time

    duration_s = input("请输入静音区的持续时间（秒）：")
    duration_ms = int(float(duration_s) * 1000)  # 转换为毫秒

    insert_silence(input_file_path, output_file_path, start_times, duration_ms)
