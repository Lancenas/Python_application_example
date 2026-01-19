def simple_txt_to_m3u(txt_file, m3u_file):
    with open(txt_file, 'r', encoding='utf-8') as fin, \
         open(m3u_file, 'w', encoding='utf-8-sig') as fout:
        fout.write('#EXTM3U\n')
        for line in fin:
            url = line.strip()
            if url and not url.startswith('#') and '://' in url:
                fout.write(url + '\n')

# 使用
simple_txt_to_m3u('urls.txt', 'playlist.m3u')
