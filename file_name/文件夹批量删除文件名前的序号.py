import os
import re

def remove_numbers_from_file_names(directory):
    for filename in os.listdir(directory):
        if re.match(r'\d+', filename):  # 匹配文件名开头的数字序号
            number_pattern = re.compile(r'^\d+')  # 编译正则表达式以提高性能
            new_filename = re.sub(number_pattern, '', filename)  # 删除序号
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))  # 重命名文件

# 使用示例
directory_path = '/Volumes/music/韩红最-令人感动的专辑《醒了》'  # 替换为你的文件夹路径
remove_numbers_from_file_names(directory_path)