import os
import platform
import fileinput
import progressbar
import urllib.request
import json
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

def print_color(message, color):
    print(f"{color}{message}{bcolors.ENDC}")

def get_folder():
    running = True
    while running:
        path = str(input("[?] Where do you want to install the server to (folder must be empty): "))
        if path is not None:
            # Getting the list of directories
            dir = os.listdir(path)
            
            # Checking if the list is empty or not
            if len(dir) == 0:
                # Dir is empty
                return path
            else:
                print_color("[x] Directory isn't empty", bcolors.FAIL)

def get_server_type():
    running = True
    while running:
        server_type = str(input("\n[?] Which minecraft server will this server be running, Paper or Vanilla: "))
        if (server_type == "Paper") or (server_type == "Vanilla"):
            running = False
            return server_type
        else:
            print_color("Enter a valid answer.", bcolors.FAIL)
            continue


def get_latest_paper(version):
    print_color("[i] Getting latest paper server url from: https://papermc.io", bcolors.WARNING)

    with urllib.request.urlopen(f"https://papermc.io/api/v2/projects/paper/versions/{version}") as baseurl:
        basedata = json.loads(baseurl.read().decode())
        buildsList = []
        for i in basedata["builds"]:
            buildsList.append(i)
        
        print_color(f"[*] Found correct version, {version}: searching for download link...", bcolors.OKGREEN)
        
        with urllib.request.urlopen(f"https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{buildsList[-1]}") as buildurl:
            builddata = json.loads(buildurl.read().decode())
            name = builddata["downloads"]["application"]["name"]
            final = f"https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{buildsList[-1]}/downloads/{name}"
            return final

def download_file(path, url, name):
    print_color(f"[i] Downloading server to {path}, as {name}", bcolors.WARNING)
    print_color("[i] Downloading latest server file: ", bcolors.WARNING)
    urllib.request.urlretrieve(url, os.path.join(path, name), show_progress)
    print_color("[*] Download Complete!\n", bcolors.OKGREEN)


def get_latest_vanilla(version):
    print_color("[i] Getting latest vanilla server url from: https://launchermeta.mojang.com/mc/game/version_manifest.json", bcolors.WARNING)
    
    # Get json file with all versions
    with urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json") as url:
        data = json.loads(url.read().decode())
        for i in data["versions"]:
            id = i["id"]
            versionJson = i["url"]
            
            if id == version:
                print_color(f"[*] Found correct version, {version}: searching for download link...", bcolors.OKGREEN)

                with urllib.request.urlopen(versionJson) as versionUrl:
                    dataUrl = json.loads(versionUrl.read().decode())
                    download = dataUrl["downloads"]["server"]["url"]

                    return download                   

def first_run(path):
    running = True
    while running:
        print_color("[i] The server will now start and stop to create folders.", bcolors.WARNING)
        input("[Press ENTER to continue]\n")
        os.chdir(path) # CD into server folder
        try:
            subprocess.run(['java', '-jar', 'server.jar'], check = True)
        except subprocess.CalledProcessError:
            print_color("[x] Could not start the server, make sure Java is installed.")

        eula = input("[?] You need to accept the eula to launch your server. Accept it? [y/n]: ")
        if eula == "y":
            with fileinput.FileInput('eula.txt', inplace=True) as file:
                for line in file:
                    print(line.replace('eula=false', 'eula=true'), end='')
            print_color("[*] Eula accepted.\n", bcolors.OKGREEN)
            running = False
        elif eula == "n":
            print_color("[x] Eula refused.\n", bcolors.FAIL)
        else:
            print_color("[x] Enter a valid answer", bcolors.FAIL)

def modify_props():
    running = True
    runningModif = True
    while running:
        # Ask question
        modif_question = str(input("[?] Do you want to modify the server properties [y/n]: "))
        if modif_question == "y":
            print_color("[*] Modifying config.\n", bcolors.WARNING)

            # All modifications will happen here
            while runningModif:
                what_to_edit = str(input(
"""
\n1. Edit world seed
2. Edit server name
3. Edit max player value
4. Edit view distance
5. Server port
6. Enbale/Disbale online mode
7. Continue\n
"""
                ))

                # Check answer
                serv_prop = open("server.properties", "r+")
                lines_prop = serv_prop.readlines()
                match what_to_edit:
                    case "1":
                        seed = str(input("\n[?] Which seed would you like to set: "))
                        lines_prop[4] = f"level-seed={seed}\n"
                        
                        print_color(f"[*] Seed changed to {seed}.", bcolors.OKGREEN)

                    case "2":
                        name = str(input("\n[?] Which name would you like to set for your server: "))
                        lines_prop[10] = f"motd={name}\n"

                        print_color(f"[*] Server name changed to {name}.", bcolors.OKGREEN)

                    case "3":
                        players = str(input("\n[?] How many players do you want to be able to join simultaneously: "))
                        lines_prop[18] = f"max-players={players}\n"
                        
                        print_color(f"[*] Player limit changed to {players}.", bcolors.OKGREEN)

                    case "4":
                        view = str(input("\nHow many chunks do you want the server to render? "))
                        lines_prop[23] = "view-distance=" + view + "\n"
                        
                        print_color(f"[*] Render distance changed to {view}.", bcolors.OKGREEN)

                    case "5":
                        port = str(input("\nWhat port do you want the server to run on? "))
                        lines_prop[27] = f"server-port={port}\n"
                        
                        print_color(f"[*] Server port changed to {port}.", bcolors.OKGREEN)
                        
                    case "6":
                        online = str(input("\n[?] Do you want to enable online mode [y/n]: "))
                        if online == "y":
                            online_check = "enabled."
                            lines_prop[19] = "online-mode=true\n"
                            
                        if online == "n":
                            online_check = "disabled."
                            lines_prop[19] = "online-mode=false\n"
                            
                        print_color(f"[*] Online mode {online_check}", bcolors.OKGREEN)

                    case "7":
                        print_color("[*] Saving config and exiting...", bcolors.WARNING)

                        # Save file
                        serv_prop.writelines(lines_prop)
                        serv_prop.close()

                        # Quit loops
                        runningModif = False
                        running = False
                    case _:
                        print_color("[x] Enter a valid answer", bcolors.FAIL)


        elif modif_question == "n":
            print_color("[*] Continuing without modifications.\n", bcolors.WARNING)
            running = False
        else:
            print_color("[x] Enter a valid answer", bcolors.FAIL)

def make_start_script():
    running = True
    while running:
        start = input("[?] Your server is now complete. Do you want to have a start script to start it easily [y/n]: ")

        if start == "y":
            # Finds running OS
            os = platform.system()

            running2 = True
            while running2:
                # Linux/macOS - make .sh file
                if os == "Linux" or os == "Darwin":
                    script_type = str(input("[?] Do you want an optimized start script (PAPER ONLY) [y/n]: "))
                    start_sh = open("start.sh", "x")

                    # Optimized start script
                    if script_type == "y":
                        ram = input("[?] How much ram do you want to give to the server: ")
                        
                        start_sh.writelines('#!/bin/bash\njava -Xmx'+ram+'M -Xms'+ram+'M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar server.jar nogui')
                        start_sh.close()
                        # Make file executable
                        os.chmod('start.sh', 0o777)
                        running2 = False
                        running = False

                        print_color("[*] Created script", bcolors.OKGREEN)

                    # Normal start script
                    elif script_type == "n":
                        ram = input("[?] How much ram do you want to give to the server: ")
                        
                        start_sh.writelines('#!/bin/bash\njava -Xmx'+ram+'M -Xms'+ram+'M -jar server.jar nogui')
                        start_sh.close()
                        # Make file executable
                        os.chmod('start.sh', 0o777)
                        running2 = False
                        running = False

                        print_color("[*] Created script", bcolors.OKGREEN)

                    # Wrong answer
                    else:
                        print_color("[x] Enter a valid answer.", bcolors.FAIL)

                # Windows - make .bat file
                elif os == "Windows":
                    script_type = str(input("[?] Do you want an optimized start script (PAPER ONLY) [y/n]: "))
                    start_sh = open("start.bat", "x")

                    # Optimized start script
                    if script_type == "y":
                        ram = input("[?] How much ram do you want to give to the server: ")
                        
                        start_sh.writelines('java -Xmx'+ram+'M -Xms'+ram+'M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar server.jar nogui')
                        start_sh.close()

                        running2 = False
                        running = False

                        print_color("[*] Created script", bcolors.OKGREEN)

                    # Normal start script
                    elif script_type == "n":
                        ram = input("[?] How much ram do you want to give to the server: ")
                        
                        start_sh.writelines('java -Xmx'+ram+'M -Xms'+ram+'M -jar server.jar nogui')
                        start_sh.close()

                        running2 = False
                        running = False

                        print_color("[*] Created script", bcolors.OKGREEN)

                    # Wrong answer
                    else:
                        print_color("[x] Enter a valid answer.", bcolors.FAIL)
            


        elif start == "n":
            print_color("[i] Skipping start script.", bcolors.WARNING)
            running = False
        else:
            continue


def main():

    print("--------------------")
    print("Made by Yot, @Yot360")
    print("--------------------\n")

    running = True
    while running:
        
        # Ask where to install server
        path = get_folder()

        # Ask server type
        if get_server_type() == "Vanilla":
            # Tries to find vanilla URL
            get_dl_question = True
            while get_dl_question:
                version = str(input("\n[?] Please enter the minecraft version that you would like your server to be running: "))
                url = get_latest_vanilla(version)
                if url is None:
                    print_color(f"[x] Didn't find a download link for version {version}.", bcolors.FAIL)
                    continue
                else:
                    print_color(f"[*] Found download link for version {version}: {url}", bcolors.OKGREEN)

                    # Download
                    download_file(path, url, "server.jar")

                    get_dl_question = False # Go to next question
        else:
            #Tries to find paper URL
            get_dl_question = True
            while get_dl_question:
                version = str(input("\n[?] Please enter the minecraft version that you would like your server to be running: "))
                url = get_latest_paper(version)
                if url is None:
                    print_color(f"[x] Didn't find a download link for version {version}.", bcolors.FAIL)
                    continue
                else:
                    print_color(f"[*] Found download link for version {version}: {url}", bcolors.OKGREEN)

                    # Download
                    download_file(path, url, "server.jar")

                    get_dl_question = False # Go to next question

        # Setup server
        first_run(path)
        modify_props()

        # Finish server + start script
        make_start_script()

        print_color("[*] Server is done, simply start it by running the start script!", bcolors.OKGREEN)
        running = False


main()