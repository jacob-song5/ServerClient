import socket
import pathFunctions

def main():
    server = makeSocket()
    while True:
        handleConnection(server)

def makeSocket():
    s = socket.socket()
    host = socket.gethostbyname(socket.gethostname())
    print(host)
    #public ip of server is 108.192.40.180
    port = 9462
    s.bind((host, port))
    s.listen(5)
    return s

def handleConnection(s):
    c, addr = s.accept()
                   
    print("Got connection from", addr)
    requestedFile = c.recv(8192).decode()
    validateRequest(requestedFile, c)
    
def copyFile(c, fileName):
    f = open(fileName, 'rb')
    n = 1
    while (n):
        #print('Writing')
        n = f.read(8192)
        c.send(n)
    f.close()
    print("Done Writing")

def validateRequest(requestedFile: str, c):
    if pathFunctions.validPath(requestedFile):
        c.send("Transfering your file now".encode())
        copyFile(c, requestedFile)
    else:
        c.send("Not a valid file".encode())
        print("Rejected a request")

    c.close()

main()
