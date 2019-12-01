import socket
import subprocess
import sys
import socket
import time
from datetime import datetime
import numpy as np

# clear shell
subprocess.call('clear', shell=True)



# request input
remoteServer = input("Enter remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)

# print banner of info on host to scan
print("-"*60)
print("Please wait, scanning remote host ", remoteServerIP)
print("-"*60)

# initializing a few global variables
openPorts = 0
usrIntrpt = False
openPortArray = []

def scanPorts(targetIP, tPorts):

    global openPorts
    global usrIntrpt
    # use range function to specify ports (using 1-1024)
    # also includes error handling for catching runtime errors

    try:
        for port in range(1, tPorts):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP only
            result = sock.connect_ex((targetIP, port))
            if result == 0:
                print("Port {}:     \033[1;32;40mOpen\033[0;37;40m".format(port))
                openPorts += 1
                openPortArray.append(port)
            sock.close()

    except KeyboardInterrupt:
        usrIntrpt = True
        print("[ KeyboardInterrupt ] Continuing...")
        pass

    except socket.gaierror:
        print("Hostname could not be resolved.  (exiting...)")
        sys.exit[0]

    except socket.error:
        print("Couldn't connect to server.  (exiting...)")
        sys.exit[0]

    print(openPortArray)

def portListen(targetIP, portIn):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((targetIP, portIn))
    while 1:
        time.sleep(5)
        # 512 bytes of data
        data = client_socket.recv(512)
        if (data == 'q' or data == 'Q'):
            client_socket.close()
            break
        else:
            print("[ RECEIVED: ] " + str(data))
            data = input("SEND( TYPE q or Q to Quit):")
            if (data != 'Q' and data != 'q'):
                #data.encode()
                client_socket.send(data.encode())
            else:
                #data.encode()
                client_socket.send(data.encode())
                client_socket.close()
                break

def echoHost(remoteIP, portRead):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = (remoteIP, int(portRead))
    connection.bind(address)
    connection.listen(10)
    while True:
        current_connection , address = connection.accept()
        while True:
            data = current_connection.recv(2048)

            if data == 'quit\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                break

            elif data == 'stop\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                exit()

            elif data:
                current_connection.send(data)
                print(data)

t1 = datetime.now()                          # record initial time
scanPorts(remoteServerIP, 1025)        # run port scanner function
t2 = datetime.now()                            # record final time

elapsedTime = (t2 - t1)
elapsedSec = elapsedTime.total_seconds()

print(("-"*60) +"\n")
print("Scanning complete in: %s seconds" % elapsedSec)
print("Number of open ports found:      \033[1;31;40m%s\033[1;37;40m" % openPorts)
print("User interrupt: %s" % usrIntrpt)
print("\n" + ("-"*60) +"\n")


choice = input("Continue with port listener? (y/n): ")
if (choice == "y"):
    for port in openPortArray:
        print("[FROM PORT %s]" % port)
        portListen(remoteServerIP, int(port))

        if KeyboardInterrupt:
            pass
else:
    sys.exit[0]

echoChoice = input("Do you wish to echo the server:port? (y/n): ")
if echoChoice == 'y':
    port = int(input("Please input port to launch echoer: "))
    echoHost(remoteServerIP, port)
