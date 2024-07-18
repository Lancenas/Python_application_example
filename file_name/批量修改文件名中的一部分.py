import os


def rename_files_in_folder(folder_path, old_string, new_string):
    """
    批量修改文件名中的一部分字符串。

    :param folder_path: 文件夹路径
    :param old_string: 需要被替换的字符串
    :param new_string: 新的字符串，用于替换旧字符串
    """
    for filename in os.listdir(folder_path):
        if old_string in filename:
            os.rename(os.path.join(folder_path, filename),
                      os.path.join(folder_path, filename.replace(old_string, new_string)))


# 使用示例
# 假设我们要在当前目录下的"example_folder"中将所有包含"old"的文件名替换为"new"
folder = "/Users/lixiao/github/hexo_blog/source/_posts"  # 文件夹路径
old_str = "mp3"  # 需要被替换的字符串
new_str = ".mp3"  # 新的字符串
rename_files_in_folder(folder, old_str, new_str)