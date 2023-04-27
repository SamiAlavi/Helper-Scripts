import os  
import glob  
import win32com.client  
  
def convert(files, formatType = 32):  
    powerpoint = win32com.client.Dispatch("Powerpoint.Application")  
    powerpoint.Visible = 1  
    for filename in files:
        print(filename)
        newname = f"{os.path.splitext(filename)[0]}.pdf"
        deck = powerpoint.Presentations.Open(filename)
        deck.SaveAs(newname, formatType)  
        deck.Close()  
    powerpoint.Quit()
  
dirr = os.getcwd()
print(dirr)
files = glob.glob(os.path.join(dirr, "*.ppt*"))  
print(len(files))

convert(files)
