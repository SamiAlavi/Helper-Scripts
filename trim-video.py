import moviepy

name = input('Enter video path to trim: ')
start = int(input('Enter starting time (in seconds): '))
end = int(input('Enter ending time (in seconds): '))
result = f"{name} (trimmed).mp4"

print(f'Saving trimmed video in path: {result}')

video = moviepy.editor.VideoFileClip(name).subclip(start, end)
video.write_videofile(result, fps=30)
