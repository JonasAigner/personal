import socket
import os
import sys
import random

connected = False

password = ""
pwd1 = str(random.randint(0, 9))
pwd2 = str(random.randint(0, 9))
pwd3 = str(random.randint(0, 9))
pwd4 = str(random.randint(0, 9))
pwd5 = str(random.randint(0, 9))
pwd6 = str(random.randint(0, 9))
pwd7 = str(random.randint(0, 9))
pwd8 = str(random.randint(0, 9))
pwd9 = str(random.randint(0, 9))
password = pwd1 + pwd2 + pwd3 + pwd4 + pwd5 + pwd6 + pwd7 + pwd8 + pwd9

server_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
                              
                            
                              
# socket.gethostname() geht nur wenn server und client nicht auf einem pc sind
# ansonsten localhost ip adresse: 127.0.0.1
host = socket.gethostname()
ip = "127.0.0.1"
port = 1337
server_socket.bind((ip, port)) #'erstellt' server


def sys_shell():
    out = os.popen("date").read()
    client_socket.send(str(out), "utf8")


def send_file(filname):
    fil = open(filname, "rb")
    file_data = fil.read(1024)
    print("[*]Sending File '{}'...".format(filname))
    while (file_data):
        client_socket.send(file_data)
        file_data = fil.read(1024)
    print("[*]File Sended Successful!")
    print("[*]Closing client socket...")
    client_socket.send(bytes("File sended", "utf8"))
    client_socket.close()
    connected = False
    print("[*]client socked is closed")

def syscom(co):
    x = os.popen(co).read()
    return x

def execute(co):
    new = ""
    colist = list(co)
    colist[0] = ""
    colist[1] = ""
    for x in colist:
        new += x
    newsplit = new.split()
    print("[CLIENT]:/" + new)
    if new == "quit":
        server_socket.close()
    elif newsplit[0] == "send_file":
        send_file(newsplit[1])
    if new == "dirname":
        #out = subprocess.run(("dir", "/W"), capture_output=True)
        out = os.getcwd()
        print("[*]Output: " + out)
        client_socket.send(bytes(out, "utf8"))
    elif new == "list":
        out = os.listdir()
        client_socket.send(bytes("---- direct of server ----", "utf8"))
        client_socket.send(bytes("\n", "utf8"))
        for entry in out:
            client_socket.send(bytes(entry + "\n", "utf8"))
        client_socket.send(bytes("---- end of server directory ----", "utf8"))
    elif new == "platform":
        out = sys.platform
        if out == "win32":
            x = sys.getwindowsversion()
            out += " -version {}.{} -build {}".format(x.major, x.minor, x.build)
        client_socket.send(bytes(out, "utf8"))
    elif new == "walk":
        counter = 0
        way = "\n---------------- Walk ----------------\n"
        for root, dirs, files in os.walk("."):
            way += "Direcory: "+root+"\n"
            way += "----- Minor Directorys -----\n"
            for d in dirs:
                way += d+"\n"
            way += "--- Files ---\n"
            for f in files:
                way += f+"\n"
            counter += 1
        way += "\n\n" + str(counter) + " Directorys"
        client_socket.send(bytes(way, "utf8"))
        
    elif new == "walk_root":
        counter = 0
        way = "\n---------------- Walk ----------------\n"
        for root, dirs, files in os.walk("/"):
            way += "Direcory: "+root+"\n"
            way += "----- Minor Directorys -----\n"
            for d in dirs:
                way += d+"\n"
            way += "--- Files ---\n"
            for f in files:
                way += f+"\n"
            counter += 1
        way += "\n\n" + str(counter) + " Directorys"
        client_socket.send(bytes(way, "utf8"))
    elif new == "os.system":
        perm = False
        client_socket.send(bytes("Password:", "utf8"))
        pwd = client_socket.recv(1024)
        if str(pwd, "utf8") == password:
            print("[*]Permission for 'os.system' granted!")
            client_socket.send(bytes("Permission granted! Type in command:", "utf8"))
            perm = True
        else:
            client_socket.send(bytes("Wrong Password! Permission denied!", "utf8"))
        if perm == True:
            co = client_socket.recv(1024)
            out = syscom(str(co, "utf8"))
            print("[*]Executed '{}'".format(str(co, "utf8")))
            client_socket.send(bytes("\n" + out, "utf8"))
    
    else:
        try:
            exec(new)
            client_socket.send(bytes("Executed Command Successful", "utf8"))
        except:
            client_socket.send(bytes("[ERROR]:Command '{}' can not executed!".format(new), "utf8"))
        
        
def send_back(msg):
    new_msg = str(msg, "utf8")
    if new_msg == "ping":
        client_socket.send(bytes("ping", "utf8"))
        print("[SERVER]: ping")
    elif new_msg == "Disconnecting...":
        pass
    elif new_msg == "" or new_msg == " ":
        client_socket.send(bytes(" ", "utf8"))
        print("[SERVER]: ")
    elif new_msg == "hi" or new_msg == "hallo" or new_msg == "hello" or new_msg == "Hi" or new_msg == "Hallo" or new_msg == "Hello":
        client_socket.send(bytes("Hi", "utf8"))
        print("[SERVER]: Hi")
    elif new_msg == "help" or new_msg == "?" or new_msg == "Help" or new_msg == "HELP" or new_msg == "Hilfe" or new_msg == "hilfe":
        client_socket.send(bytes("Type '/help' for help", "utf8"))
        print("[SERVER]: Type '/help' for help")
    
    else:
        client_socket.send(bytes(" ", "utf8"))
        print("[SERVER]: ")
    

print("")
print("----- Server Information -----")
print("IP: " + ip)
print("Port: " + str(port))
print("Password: " + password)
print("")
print("--------------- Listening ---------------")
server_socket.listen(1) #schaut ob sich wer verbinden will 
# listen(>1<) 1 bedeutet es darf sich nur einer gleichzeitig verbinden

while True:
    if connected == False:
        try:
            (client_socket, addr) = server_socket.accept()
            connected = True
            print("------------ Connection ------------")
            print("[*]Successfully connected with {} : {}".format(addr[0], addr[1]))
            #client_socket.send(bytes("ping", "utf8"))
        except OSError:
            print("[*]Can't accept socket!")
        except ConnectionResetError:
            print("[*]Connection Lost!\n")
    
    try:
        msg = client_socket.recv(1024)
        list_msg = list(str(msg, "utf8"))
        if list_msg[0] == "/":
            execute(str(msg, "utf8"))
            #client_socket.send(bytes(" ", "utf8"))
            continue
        print("[CLIENT]: " + str(msg, "utf8")) # standart
        
        send_back(msg)
        

       
    except ConnectionResetError:
        print("[*]Connection Lost!\n")
        connected = False
    except IndexError:
        print("[*]Connection Lost!\n")
        connected = False
    except OSError:
        print("[*]Connection Lost!\n")
        connected = False
           
    
    

#LAPTOP-FHIN1JKR
