from pytube import YouTube
from bs4 import BeautifulSoup, SoupStrainer
from os import makedirs, chdir

def create_folder(dirName):
    try:
        makedirs(dirName)    
        print(f"Directory {dirName} created ")
    except FileExistsError:
        print(f"Directory {dirName} already exists")
    chdir(dirName)

def get_links(name):
    listt = list()
    with open(name, 'r', encoding='utf8') as file:
        webpage = file.read()
        count = 0
        soup = BeautifulSoup(webpage, 'html.parser', parse_only=SoupStrainer('a'))
        for link in soup:
            if link.has_attr('href'):
                href = link['href']
                if '&index=' in href:
                    count+=1
                    listt.append(href[:43])

    listt = list(set(listt))
    [print(i) for i in listt]
    print(f'Got {len(listt)} links')
    return listt

def download_yt_videos(links):    
    for link in links:
        try:
            yt = YouTube(link)
        except:
            print("Connection Error")
            continue

        mp4files = yt.streams.filter(progressive=True, file_extension='mp4')

        try:
            yt.streams.get_by_itag(mp4files[-1].itag).download()
            print(link, 'downloaded')
        except Exception as e:
            print(e)  

name = 'Playlist - YouTube.html'
dirName = './Playlist'

create_folder(dirName)
links = get_links(name)
download_yt_videos(links)

print('Task Completed!')
