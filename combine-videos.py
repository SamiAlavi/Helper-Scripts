import subprocess
import os

# specify input video file names
parent_dir = "parent_dir"
input_files = [file_name for file_name in os.listdir(parent_dir) if file_name.endswith(".mp4")]

# specify output video file name
output_file = 'combined.mp4'

# construct FFmpeg command
ffmpeg_cmd = ['ffmpeg']
for input_file in input_files:
    ffmpeg_cmd.extend(['-i', f'{parent_dir}{input_file}'])
ffmpeg_cmd.extend(['-filter_complex', f'concat=n={len(input_files)}:v=1:a=0', output_file])

# use subprocess to execute FFmpeg command
subprocess.call(ffmpeg_cmd)
