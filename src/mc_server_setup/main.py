import fileinput
import os
import progressbar
import urllib.request
from pyngrok import ngrok


print("--------------------")
print("Made by Yot, @Yot360")
print("--------------------\n")

# URLS FOR SERVER FILES
paper_url = 'https://papermc.io/api/v1/paper/1.16.5/latest/download'
vanilla_url = 'https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar'

# SETUP PROGRESS BAR
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

def main():
    # SERVER LOCATION
    home_dir = os.path.expanduser("~")
    print(
        "Where do you want the server to be installed:\n \n1. In a new folder named server, in home directory \n2. In a custom location"
    )

    path = None
    while True:
        try:
            server_location = int(input("(e.g 1 or 2) : "))
        except ValueError:
            print("Please try again and choose a valid number.")
            continue

        if server_location == 1:
            path = home_dir + "/server"
        elif server_location == 2:
            path = input("\nPlease enter the custom location : ")

        if path:
            if os.path.isdir(path):
                print("Folder already exists. Try again.")
                continue
            break
        else:
            print("Please try again and choose a valid number.")
            continue

    print(f"\nMaking the server in {path}.\n")
    os.mkdir(path)

    # MINECRAFT SERVERS JAR DOWNLOADS
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

    # SERVER SETUP
    print("The server will now start and stop.\n")
    os.chdir(path)
    os.system('java -jar server.jar')
    eula = input("You need to accept the eula to launch your server. Accept it? [y/n] ")
    if eula == "y":
        with fileinput.FileInput('eula.txt', inplace=True) as file:
            for line in file:
                print(line.replace('eula=false', 'eula=true'), end='')
        print("Eula accepted.\n")
    elif eula == "n":
        print('Eula refused.\n')
    serv_prop_ask = input("Do you wish to change any settings in the system.properties file? [y/n] ")
    while True:
        if serv_prop_ask == "y":
            serv_prop_ask2 = int(
                input(
                    "\n1. Edit world seed\n2. Edit server name\n3. Edit max player value\n4. Edit view distance\n5. Server port\n6. Enbale/Disbale online mode\n7. Exit\n\n"
                )
            )
            if serv_prop_ask2 == 1:
                serv_prop = open("server.properties", "r")
                lines_prop = serv_prop.readlines()

                seed = str(input("\nWhich seed would you like to set? "))
                lines_prop[4] = "level-seed=" + seed + "\n"
                serv_prop = open("server.properties", "w")
                serv_prop.writelines(lines_prop)
                serv_prop.close()
                print("\nSeed changed to " + seed + ".")

            elif serv_prop_ask2 == 2:
                serv_prop = open("server.properties", "r")
                lines_prop = serv_prop.readlines()

                name = str(input("\nWhich name would you like to set for your server? "))
                lines_prop[10] = "motd=" + name + "\n"
                serv_prop = open("server.properties", "w")
                serv_prop.writelines(lines_prop)
                serv_prop.close()
                print("\nServer name changed to " + name + ".")
            elif serv_prop_ask2 == 3:
                serv_prop = open("server.properties", "r")
                lines_prop = serv_prop.readlines()

                players = str(input("\nHow many players do you want to be able to join simultaneously? "))
                lines_prop[18] = "max-players=" + players + "\n"
                serv_prop = open("server.properties", "w")
                serv_prop.writelines(lines_prop)
                serv_prop.close()
                print("\nPlayer limit changed to " + players + ".")
            elif serv_prop_ask2 == 4:
                serv_prop = open("server.properties", "r")
                lines_prop = serv_prop.readlines()

                view = str(input("\nHow many chunks do you want the server to render? "))
                lines_prop[23] = "view-distance=" + view + "\n"
                serv_prop = open("server.properties", "w")
                serv_prop.writelines(lines_prop)
                serv_prop.close()
                print("\nRender distance changed to " + view + ".")
            elif serv_prop_ask2 == 5:
                serv_prop = open("server.properties", "r")
                lines_prop = serv_prop.readlines()

                port = str(input("\nWhat port do you want the server to run on? "))
                lines_prop[27] = "server-port=" + port + "\n"
                serv_prop = open("server.properties", "w")
                serv_prop.writelines(lines_prop)
                serv_prop.close()
                print("\nServer port changed to " + port + ".")

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
                print("Online mode " + online_check)
            elif serv_prop_ask2 == 7:
                break
        if serv_prop_ask == "n":
            break

    start = input("\n Your server is now complete. Do you want to have a start file to start it easily? [y/n] ")
    if start == "n":
        pass
    if start == "y":
        os_detect = input("\n Will you run the server on Windows? [y/n] ")
        if os_detect == "y":
            start_type = int(input("\nDo you want :\n1. An optimized start file so your server will run better\n2. A normal start file\n"))
            if start_type == 1:
                ram = input("\nHow much ram do you want to give to the server? ")
                start_bat = open("start.bat", "x")
                start_bat.writelines('java -Xmx'+ram+'M -Xms'+ram+'M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar server.jar nogui\nPAUSE')
                start_bat.close()
            if start_type == 2:
                ram = input("\nHow much ram do you want to give to the server? ")
                start_bat = open("start.bat", "x")
                start_bat.writelines('java -Xmx'+ram+'M -Xms'+ram+'M -jar server.jar nogui\nPAUSE')
                start_bat.close()
        if os_detect == "n":
            start_type = int(input("\nDo you want :\n1. An optimized start file so your server will run better\n2. A normal start file\n"))
            if start_type == 1:
                ram = input("\nHow much ram do you want to give to the server? ")
                start_sh = open("start.sh", "x")
                start_sh.writelines('#!/bin/bash\njava -Xmx'+ram+'M -Xms'+ram+'M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar server.jar nogui')
                start_sh.close()
            if start_type == 2:
                ram = input("\nHow much ram do you want to give to the server? ")
                start_sh = open("start.sh", "x")
                start_sh.writelines('#!/bin/bash\njava -Xmx'+ram+'M -Xms'+ram+'M -jar server.jar nogui')
                start_sh.close()
            os.chmod('start.sh', 0o777)

    ngrok_ask = input("\nDo you want to start ngrok/minecraft server (access server without opening ports)? [y/n] ")
    if ngrok_ask == "y":
        while True:
            auth = str(input("Please crate an account at https://dashboard.ngrok.com/signup, and enter your AUTH Token: "))
            ngrok.set_auth_token(auth)
            break
        # <NgrokTunnel: "tcp://0.tcp.ngrok.io:25565" -> "localhost:225565">
        ssh_tunnel = ngrok.connect(25565, "tcp")
        tunnels = ngrok.get_tunnels()
        print("\n\033[1;32;40mNgrok started, you can now access the server with"+str(tunnels))
        if os_detect == "y":
            print("\nServer starting...")
            os.system(path+'/start.bat')
        if os_detect == "n":
                print("\nServer starting...")
                os.system('./start.sh')
    if ngrok_ask == "n":
        pass
    start_rn = input("\nDo you to start your server right now? [y/n] ")
    if start_rn == "n":
        print("Ok, if you want to launch your server simply run the start.sh(.bat) file!")
        print("Have fun!")
        exit()
    if os_detect == "y":
        if start_rn == "y":
            print("\nServer starting...")
            os.system(path+'/start.bat')
    if os_detect == "n":
        if start_rn == "y":
            print("\nServer starting...")
            os.system('./start.sh')

main()
