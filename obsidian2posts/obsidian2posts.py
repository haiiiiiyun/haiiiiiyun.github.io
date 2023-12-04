import os
import re
import shutil

src = '/home/hy/workspace/obsidian-notes/TIL_Today I Learned/'
dst = '/home/hy/workspace/haiiiiiyun.github.io/obsidian2posts/_posts/'


if __name__ == '__main__':
    # if os.path.exists(dst):
    #    print('rm')
    #    shutil.rmtree(dst)
    #os.makedirs(dst)

    for subdir, dirs, files in os.walk(src):
        subdir_prefix = subdir
        if subdir_prefix.startswith(src):
            subdir_prefix = subdir_prefix.replace(src, '')
        subdir_prefix.replace('/', '__')

        for filename in files:
            if filename.endswith('.md') and filename != 'index.md':
                contents = ['---\n']
                contents.append(f'title: {filename[:-3]}\n')
                src_filepath = os.path.join(subdir, filename)
                print('subdir=', subdir)
                print('filename=', filename)
                dst_filename = filename.replace(' ', '_')
                if subdir_prefix:
                    dst_filename = f'{subdir_prefix}__{dst_filename}'

                [first_line, *rest_lines] = open(src_filepath).readlines()
                file_tags = {}
                for tag in first_line.split():
                    if tag.startswith('#'):
                        tag = tag[1:]
                        if re.search(r'\d{4}/\d{2}/\d{1,2}', tag):
                            file_date = tag.replace('/', '-')
                            dst_filename = f'{file_date}-{dst_filename}'
                            contents.append(f'date: {file_date}\n')
                        else:
                            for tag_name in tag.split('/'):
                                if tag_name not in file_tags:
                                    file_tags[tag_name] = True
                tag_str = ' '.join(file_tags.keys())
                contents.append(f'tags: {tag_str}\n')
                contents.append('categoris: Programming\n')
                contents.append('---\n')

                contents += rest_lines

                dst_filepath = os.path.join(dst, dst_filename)
                print('dst=', dst_filepath)
                open(dst_filepath, 'w').writelines(contents)
