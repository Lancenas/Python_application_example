import os
import shutil
import re


def time_to_seconds(time_str):
    pattern = re.compile(r'(\d+):(\d+):(\d+)')
    match = pattern.match(time_str)
    if match:
        hours, minutes, seconds = map(int, match.groups())
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds
    else:
        raise ValueError("Invalid time format. Please use HH:MM:SS format.")


def check_existing_bookmarks(audio_path, bookmarks_file):
    existing_bookmarks = []
    if os.path.exists(bookmarks_file):
        with open(bookmarks_file, "r") as f:
            for line in f:
                time, name = line.strip().split(',')
                existing_bookmarks.append((float(time), name))
    return existing_bookmarks


def insert_bookmark(audio_path):
    bookmarks_file = "../bookmarks.txt"
    existing_bookmarks = check_existing_bookmarks(audio_path, bookmarks_file)

    print("已存在的书签：")
    if existing_bookmarks:
        for idx, (time, name) in enumerate(existing_bookmarks, start=1):
            print(f"{idx}. 时间：{time}秒, 书签名称：{name}")

        print("是否删除已存在的书签？（是/否/'a'全部删除）")
        delete_input = input().lower()

        if delete_input == 'a':
            existing_bookmarks = []
            print("已全部删除已存在的书签。")
        elif delete_input == '是':
            print("请输入要删除的书签序号（多个序号使用逗号分隔）：")
            indexes_to_delete = input().split(',')
            indexes_to_delete = [int(idx.strip()) - 1 for idx in indexes_to_delete]

            for idx in sorted(indexes_to_delete, reverse=True):
                if idx >= 0 and idx < len(existing_bookmarks):
                    print(f"删除书签：{existing_bookmarks[idx][1]}")
                    existing_bookmarks.pop(idx)

    bookmarks = []
    while True:
        print("请输入书签插入时间（格式：00:00:00），输入 'o' 退出：")
        user_input = input()

        if user_input.lower() == 'o':
            break

        try:
            bookmark_time = time_to_seconds(user_input)
        except ValueError as e:
            print(e)
            continue

        print("请输入书签名称：")
        bookmark_name = input()

        bookmarks.append((bookmark_time, bookmark_name))

    all_bookmarks = existing_bookmarks + bookmarks

    print("您插入的所有书签如下：")
    for idx, (time, name) in enumerate(all_bookmarks, start=1):
        print(f"{idx}. 时间：{time}秒, 书签名称：{name}")

    print("是否在书签处分割音频？（是/否）")
    split_audio = input().lower() == "是"

    output_folder = None
    if split_audio:
        print("请输入自定义分割输出文件夹路径：")
        output_folder = input()

        # 执行插入书签和分割音频的逻辑
        # 这里只是一个示例，具体的音频处理方法需要使用相应的音频处理库
        # 假设使用 PyDub 进行音频处理
        from pydub import AudioSegment

        audio = AudioSegment.from_file(audio_path)

        for i in range(len(all_bookmarks)):
            start_time = all_bookmarks[i][0] * 1000  # 转换为毫秒
            if i < len(all_bookmarks) - 1:
                end_time = all_bookmarks[i + 1][0] * 1000
            else:
                end_time = len(audio)

            segment = audio[start_time:end_time]

            # 使用第 i 个书签的名称来命名分割文件
            if output_folder:
                output_file = os.path.join(output_folder, f"{all_bookmarks[i][1]}.wav")
            else:
                output_file = f"{all_bookmarks[i][1]}.wav"

            segment.export(output_file, format="wav")

    print("书签插入成功！")

    if split_audio:
        print("音频已分割并保存到指定文件夹。")

    # 将所有书签保存到文件中
    with open(bookmarks_file, "w") as f:
        for time, name in all_bookmarks:
            f.write(f"{time},{name}\n")


if __name__ == "__main__":
    print("请输入音频文件路径：")
    audio_file_path = input()

    if os.path.exists(audio_file_path):
        insert_bookmark(audio_file_path)
    else:
        print("文件路径不存在，请检查输入的音频文件路径。")
