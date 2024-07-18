import os


def remove_chars_from_filenames(directory, num_chars):
    # 遍历指定目录中的所有文件
    for filename in os.listdir(directory):
        # 获取文件的完整路径
        filepath = os.path.join(directory, filename)

        # 检查是否是文件且不是隐藏文件
        if os.path.isfile(filepath) and not filename.startswith('.'):
            # 删除文件名前指定数量的字符
            new_filename = filename[num_chars:]
            new_filepath = os.path.join(directory, new_filename)

            # 重命名文件
            os.rename(filepath, new_filepath)
            print(f'Renamed: {filename} -> {new_filename}')


# 示例用法
directory_path = '/Users/lixiao/github/hexo_blog/source/_posts'  # 将此处替换为你的文件夹路径
num_chars_to_remove = 11  # 将此处替换为你想要删除的字符数量

remove_chars_from_filenames(directory_path, num_chars_to_remove)
