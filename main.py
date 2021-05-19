import urllib.request
import progressbar
import os



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


#URLS FOR SERVER FILES
paper_url = 'https://papermc.io/api/v1/paper/1.16.5/latest/download'
vanilla_url = 'https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar'

#MINECRAFT SERVERS JAR DOWNLOADS
os.mkdir('server')
print("Choose which minecraft server type you want to download: \n 1. Paper \n 2. Vanilla")
choice = int(input("(e.g 1 or 2) : "))

if choice == 1:
    print("Downloading PaperMC latest server file: ")
    urllib.request.urlretrieve(paper_url, './server/paper.jar', show_progress)
    print("Download Complete!")
elif choice == 2:
    print("Downloading Minecraft vanilla server latest file: ")
    urllib.request.urlretrieve(vanilla_url, './server/vanilla.jar', show_progress)
    print("Download Complete!")
else:
    print("Please try again and choose a valid number.")

#SERVER SETUP (LOCATION, CONFIG)
print("The server will now start setting up.")
print("Where do you want the server to be installed: \n (Default)1. In a new folder named server, in home directory \n 2. In a custom location")

server_location = int(input("(e.g 1 or 2) : "))
server_dir = os.system("cd ~")


if server_location == 1:
    print("Making the server in server directory.")
elif server_location == 2:
    server_dir = input("Please enter the custom location : ")
    print("Making server in " + server_dir)
else:
    print("Please try again and choose a valid number.")

os.system('echo ')