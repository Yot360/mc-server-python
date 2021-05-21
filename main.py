import urllib.request
import progressbar
import os
import subprocess

print("--------------------")
print("Made by Yot, @Yot360")
print("--------------------\n")

#URLS FOR SERVER FILES
paper_url = 'https://papermc.io/api/v1/paper/1.16.5/latest/download'
vanilla_url = 'https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar'


# PROGRESS BAR
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
    urllib.request.urlretrieve(paper_url, path + '/server.jar', show_progress)
    print("Download Complete!\n")
elif choice == 2:
    print("Downloading Minecraft vanilla server latest file: ")
    urllib.request.urlretrieve(vanilla_url, path + '/server.jar', show_progress)
    print("Download Complete!\n")
else:
    print("Please try again and choose a valid number.")


#SERVER SETUP
print("The server will now start and stop.\n")
os.chdir(path)
os.system('java -jar server.jar')
eula = input("You need to accept the eula to launch your server. Accept it? [y/n] ")
if eula == "y":
    a_file = open("eula.txt", "r")
    list_of_lines = a_file.readlines()
    list_of_lines[3] = "eula=true\n"
    a_file = open("eula.txt", "w")
    a_file.writelines(list_of_lines)
    a_file.close()
    print("Eula accepted.\n")
elif eula == "n":
    print('Eula refused.\n')
serv_prop_ask = input("Do you wish to change any settings in the system.properties file? [y/n] ")
if serv_prop_ask == "n":
    exit()
while True:
    if serv_prop_ask == "y":
        serv_prop_ask2 = int(input("\n1. Edit world seed\n2. Edit server name\n3. Edit max player value\n4. Edit view distance\n5. Server port\n6. Enbale/Disbale online mode\n7. Exit\n\n"))
        if serv_prop_ask2 == 1:
            serv_prop = open("server.properties", "r")
            lines_prop = serv_prop.readlines()

            seed = str(input("\nWhich seed would you like to set? "))
            lines_prop[4] = "level-seed="+seed+"\n"
            serv_prop = open("server.properties", "w")
            serv_prop.writelines(lines_prop)
            serv_prop.close()
            print("\nSeed changed to "+seed+".")

        elif serv_prop_ask2 == 2:
            serv_prop = open("server.properties", "r")
            lines_prop = serv_prop.readlines()
            
            name = str(input("\nWhich name would you like to set for your server? "))
            lines_prop[10] = "motd="+name+"\n"
            serv_prop = open("server.properties", "w")
            serv_prop.writelines(lines_prop)
            serv_prop.close()
            print("\nServer name changed to "+name+".")
        elif serv_prop_ask2 == 3:
            serv_prop = open("server.properties", "r")
            lines_prop = serv_prop.readlines()
            
            players = str(input("\nHow many players do you want to be able to join simultaneously? "))
            lines_prop[18] = "max-players="+players+"\n"
            serv_prop = open("server.properties", "w")
            serv_prop.writelines(lines_prop)
            serv_prop.close()
            print("\nPlayer limit changed to "+players+".")
        elif serv_prop_ask2 == 4:
            serv_prop = open("server.properties", "r")
            lines_prop = serv_prop.readlines()
            
            view = str(input("\nHow many chunks do you want the server to render? "))
            lines_prop[23] = "view-distance="+view+"\n"
            serv_prop = open("server.properties", "w")
            serv_prop.writelines(lines_prop)
            serv_prop.close()
            print("\nRender distance changed to "+view+".")
        elif serv_prop_ask2 == 5:
            serv_prop = open("server.properties", "r")
            lines_prop = serv_prop.readlines()
            
            port = str(input("\nWhat port do you want the server to run on? "))
            lines_prop[27] = "server-port="+port+"\n"
            serv_prop = open("server.properties", "w")
            serv_prop.writelines(lines_prop)
            serv_prop.close()
            print("\nServer port changed to "+port+".")

        elif serv_prop_ask2 == 6:
            serv_prop = open("server.properties", "r")
            lines_prop = serv_prop.readlines()
            
            online = str(input("\nDo you want to enable online mode? [y/n] "))
            if online == "y":
                online_check = "enabled."
                lines_prop[19] = "online-mode=true\n"
                serv_prop = open("server.properties", "w")
                serv_prop.writelines(lines_prop)
                serv_prop.close()
            if online == "n":
                online_check = "disabled."
                lines_prop[19] = "online-mode=false\n"
                serv_prop = open("server.properties", "w")
                serv_prop.writelines(lines_prop)
                serv_prop.close()   
            print("Online mode "+online_check)
        elif serv_prop_ask2 == 7:
            break

start = input("\n Your server is now complete. Do you want to have a start.sh file to start it easily? [y/n] ")
if start == "y":
    ram = input("\nHow much ram do you want to give to the server? ")
    start_sh = open("start.sh", "x")
    start_sh.writelines('#!/bin/bash\njava -Xmx'+ram+'M -Xms'+ram+'M -jar server.jar nogui')
    start_sh.close()
    os.chmod('start.sh', 0o777)

start_rn = input("\nDo you to start your server right now? [y/n] ")
if start_rn == "y":
    print("\nServer starting...")
    os.system('./start.sh')
if start_rn == "n":
    print("Ok, if you want to launch your server simply run the start.sh file!")
    print("Have fun!")
