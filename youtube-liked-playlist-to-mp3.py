import youtube_dl
from bs4 import BeautifulSoup, SoupStrainer
from os import makedirs, chdir


def create_folder(download_dir):
    try:
        makedirs(download_dir)    
        print(f"Directory {download_dir} created ")
    except FileExistsError:
        print(f"Directory {download_dir} already exists")
    chdir(download_dir)

def get_links(yt_liked_playlist_path, limit):
    listt = list()
    
    try:
        limit = limit*2
        
        with open(yt_liked_playlist_path, 'r', encoding='utf8') as file:
            webpage = file.read()
            count = 0
            soup = BeautifulSoup(webpage,'html.parser', parse_only=SoupStrainer('a'))
            for link in soup:
                if link.has_attr('href'):
                    href = link['href']
                    if '&index=' in href:
                        count+=1
                        listt.append(href[:43])
                if count==limit:
                    break
        listt = list(set(listt))
        [print(i) for i in listt]
        print(f'Got {len(listt)} links')
    except:
        print(f'Error reading html file at {yt_liked_playlist_path}')
    return listt
        
def download_mp3(urls, options):
    # options, see youtube_dl documentation for more options
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': options['quality'],
        }],
        'keepvideo': False,
        'outtmpl': '%(title)s.%(etx)s',
        'quiet' : not options['verbose']
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for i, url in enumerate(urls):            
            try:
                ydl.download([url])
                print(f'Downloaded {i+1} audio(s)')
            except Exception as e:
                print(repr(e))

download_dir = './Music'
yt_liked_playlist_path = './Liked videos - YouTube.html'
limit = 22 # limit number of youtube audio(s)/video(s) to download

# options for ydl
options = {
    'quality': '320',
    'verbose': False,
}

create_folder(download_dir)
urls = get_links(yt_liked_playlist_path, limit)
download_mp3(urls, options)
