import socket
import sys

client_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
                        
serveradress = "127.0.0.1"
port = 1337

def end():
   # client_socket.send(bytes("/quit", "utf8"))
    #client_socket.close()
    client_socket.send(bytes("Disconnecting...", "utf8"))
    sys.exit()

def helptext():
    print("[*]Help Coming Soon")

def execute(co):
    if co == "/help":
        helptext()
    elif co == "/quit":
        end()
    elif co == "/transfer_file":
        file_name = input("[*]Enter name of the file: ")
        string = "//send_file " + file_name
        client_socket.send(bytes(string, "utf8"))
        newfil = open(file_name, "wb")
        fil_data = client_socket.recv(1024)
        #newfil.write(fil_data)
        print("[*]Receiving File...")
        while (fil_data):
            newfil.write(fil_data)
            if fil_data < bytes(1024):
                break
            fil_data = client_socket.recv(1024)
        newfil.close()
        print("[*]File Received!")
    
    
    else:
        print("Command '{}' not found!".format(co))
    
    print("")
    
def server_execute(co):
    com = "/" + co
    client_socket.send(bytes(com, "utf8"))
    
def sudo_execute(r):
    rlist = r.split()
    if rlist[0] == "@server":
        server_execute(rlist[1])
        


try:
    client_socket.connect((serveradress, port))  # I.P. Adresse von Server 127.0.0.1 ist localhost
except ConnectionRefusedError:
    print("[*]Connection Refused!")
    sys.exit()


send_msg = "ping"

print("")
print("---- Server Information ----")
print("")
print("=======================")
print("Server IP: {}".format(serveradress))
print("Port: {}".format(port))
print("=======================")
print("")
print("")
print("------ Connection ------")
print("[*]Connection Sucessfully!")
client_socket.send(bytes(send_msg, "utf8"))
print("[CLIENT]: {}".format(send_msg))
msg_start = client_socket.recv(1024)
print("[SERVER]: " + str(msg_start, "utf8"))

while True:
    try:
        r = input("[CLIENT]: ")
        rlist = list(r)
        try:
            if rlist[0] == "/":
                execute(r)
                continue
            elif rlist[0] == "@":
                sudo_execute(r)
            else:
                client_socket.send(bytes(r, "utf8"))
        except IndexError:
            r = " "
            client_socket.send(bytes(r, "utf8"))
            
        msg = client_socket.recv(1024)
        print("[SERVER]: " + str(msg, "utf8"))
    
    except ConnectionResetError:
        print("[*]Connection Lost!")
        sys.exit()
    except ConnectionAbortedError:
        print("[*}Connection Lost!")
        sys.exit()

