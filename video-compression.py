import os
import subprocess
import shutil

def write_error(input_filepath, error):
    text = f'{input_filepath}\r\n{error}'
    with open("errors.txt", mode='a+') as file:
        file.write(text)

def get_files_list(dir_path):
    files_list = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if not file.endswith('.mp4'):
                continue
            file_path = os.path.join(root, file)
            files_list.append(file_path)
    return files_list

def copy(input_filepath, output_filepath):
    shutil.copy2(input_filepath, output_filepath)

def compress_video(input_filepath, output_filepath):
    # Construct FFmpeg command to compress video
    ffmpeg_cmd = ['ffmpeg',
                '-hide_banner', # hide FFmpeg banner
                '-loglevel', 'quiet', # set logging level to quiet
                '-progress', 'pipe:1', # output progress information in machine-readable format
                '-i', input_filepath,
                '-c:v', 'hevc_nvenc', # libx265 for x265 software encoding, hevc_nvenc for x265 hardware encoding
                '-gpu', '0', # if gpu available, else remove this line
                '-preset', 'slow',
                '-b:v', '0',
                '-maxrate', '0',
                '-bufsize', '0',
                '-movflags', '+faststart',
                '-c:a', 'copy',
                output_filepath]

    # Execute FFmpeg command using subprocess
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # print(out)

def get_directory_size(dir_path):
    total_size = 0
    num_files = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
            num_files+=1
    print(f"The size for {dir_path} is {total_size/1024/1024/1024} GBs (files: {num_files})")

parent_dir = "./"
input_dir = f"{parent_dir}input/"
output_dir = f"{parent_dir}output/"

files_list = get_files_list(input_dir)
length = len(files_list)

for i, input_filepath in enumerate(files_list):
    print(f'{i+1}/{length}) {input_filepath}')

    file_name = input_filepath.split('/')[-1]
    output_filepath = f'{output_dir}{file_name}'

    if os.path.exists(output_filepath):
        continue
    try:
        if input_filepath.endswith('.mp4'):
            compress_video(input_filepath, output_filepath)
        else:
            copy(input_filepath, output_filepath)
    except Exception as e:
        write_error(input_filepath, e)
