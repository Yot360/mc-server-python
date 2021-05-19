import urllib.request
import progressbar
import os


#URLS FOR SERVER FILES
paper_url = 'https://papermc.io/api/v1/paper/1.16.5/latest/download'
vanilla_url = 'https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar'


#DOWNLOADS PROGRESS BAR
pbar = None
def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

#SERVER LOCATION
home_dir = os.path.expanduser("~")
print("Where do you want the server to be installed:\n \n1. In a new folder named server, in home directory \n2. In a custom location")

server_location = int(input("(e.g 1 or 2) : "))

if server_location == 1:
    path = home_dir + "/server"
    if os.path.isdir(path) == True:
        print("Folder already exists...")
        exit()
    elif os.path.isdir(path) == False:
        print("\nMaking the server in " + path + " .\n")
        os.mkdir(path)

elif server_location == 2:
    path = input("\nPlease enter the custom location : ")
    if os.path.isdir(path) == True:
        print("Folder already exists...")
        exit()
    elif os.path.isdir(path) == False:
        print("\nMaking server in " + path + " .\n")
        os.mkdir(path)
else:
    print("Please try again and choose a valid number.")


#MINECRAFT SERVERS JAR DOWNLOADS
print("Choose which minecraft server type you want to download:\n \n1. Paper \n2. Vanilla")
choice = int(input("(e.g 1 or 2) : "))

if choice == 1:
    print("Downloading PaperMC latest server file: ")
    urllib.request.urlretrieve(paper_url, path + '/paper.jar', show_progress)
    print("Download Complete!")
elif choice == 2:
    print("Downloading Minecraft vanilla server latest file: ")
    urllib.request.urlretrieve(vanilla_url, path + '/vanilla.jar', show_progress)
    print("Download Complete!")
else:
    print("Please try again and choose a valid number.")


#SERVER SETUP
print("The server will now start setting up.")