import os

def txt_to_m3u(txt_file, m3u_file, encoding='utf-8'):
    """
    将 txt 文件转换为 m3u 播放列表
    - 如果行数为偶数，且非注释/空行，则按 (名称, URL) 成对处理
    - 否则，每行视为独立 URL（无标题）
    """
    with open(txt_file, 'r', encoding=encoding) as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    # 判断是否为 (名称, URL) 成对格式
    use_extinf = len(lines) % 2 == 0 and all(
        '://' in lines[i] for i in range(1, len(lines), 2)
    )

    with open(m3u_file, 'w', encoding='utf-8-sig') as f:  # utf-8-sig 写入 BOM（兼容 Windows）
        f.write('#EXTM3U\n')
        if use_extinf:
            for i in range(0, len(lines), 2):
                title = lines[i]
                url = lines[i + 1]
                f.write(f'#EXTINF:-1,{title}\n{url}\n')
        else:
            for line in lines:
                if '://' in line:  # 确保是有效 URL
                    f.write(f'{line}\n')

if __name__ == '__main__':
    txt_to_m3u('input.txt', 'output.m3u')
    print("✅ 转换完成！")
