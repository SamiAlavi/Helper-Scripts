import os
import shutil
import numpy as np
import eyed3

def check_files_format(files, ft):
    extension = '.mp3'
    for f in files:
        # check if extension is .mp3
        if f.endswith(extension):
            v = f.count('-')
            # check if there is only 1 dash
            if v==1:
                songname = f.split('-')[1]
                # check if ft elements are on right side
                for p in ft:
                    if p in songname:
                        shutil.move(path+f,temp+f)
                        break
            else:
                shutil.move(path+f,temp+f)
        else:
            shutil.move(path+f,temp+f)
    return len(os.listdir(temp))==0
            

def seperate_artists(artists, names):
    global ft    
    # iterate over each separator in music names
    for separator in ft:
        listt = artists.split(separator)
        # if seperator found, do recursion
        if len(listt)!=1:
            for artists2 in listt:
                names.append(seperate_artists(artists2, names))
            break
        
    if len(listt)==1:
        return listt[0].strip()
    else:
        return '~' # temp value

def get_artists(files_names, ft):
    song_artists = dict()
    for file_name in files_names:
        if file_name.endswith('.mp3'):
            v = file_name.count('-')
            if v==1:
                names = list()
                artists_str = file_name.split('-')[0]
                artists_list = seperate_artists(artists_str, names)
                if not names:
                    names = [artists_list]
                names, index = np.unique(names, return_index=True)
                names = names[index.argsort()]
                names = names[names!='~']
                song_artists.update({file_name:names})
            else:
                temp = np.array(file_name.split('-')[:-1]).flatten()
                #print(temp)
    return song_artists

def set_tags(path, files_names, songs_artists):
    dash = '–' # U+2013
    separator = '/'
    extension = '.mp3'
    for i, file_name in enumerate(files_names):
        if file_name.endswith(extension):
            artists = songs_artists.get(file_name)
            tagg = eyed3.load(f'{path}{file_name}').tag
            print(file_name)
            album_artist = artists[0].replace(dash,'-')
            if len(artists)>1:
                #artists = sep.join(ar[1:]).replace(dash,'-')        
                #tagg.artist = f'{album_artist} feat. {artists}'
                artists = separator.join(artists).replace(dash, '-')        
                tagg.artist = artists
            else:
                tagg.artist = album_artist
            tagg.title = file_name[:-4]
            tagg.album_artist = None
            # tagg.album = f'{1068+i}'
            tagg.save()           
            
            

def main():
    flag = True
    files_names = os.listdir(path)
    if temp in files_names:
        files_names.remove('temp')

    # flag = check_files_format(files_names, ft)
    if flag:
        songs_artists = get_artists(files_names, ft)
        set_tags(path, files_names, songs_artists)
    else:
        print("Format your files' names")

if 'src' in os.listdir():
    path = './src/Music/'
    temp = './src/Music/temp/'
else:
    path = './Music/'
    temp = './Music/temp/'

ft = [' feat.',' Feat.',' Ft.',' ft.',' feat',' Feat',' Ft',' ft',' & ',',',' x ']
artists = list()

main()
