import socket
#public ip of server is 108.192.40.180

def main():
    connection = makeSocket("108.192.40.180")
    request = input("% ")
    connection.send(request.encode())
    validateRequest(connection.recv(8192).decode(), request, connection)
    connection.close()

def makeSocket(ip):
    s = socket.socket()
    host = ip
    port = 9462
    s.connect((host, port))
    return s

def adjustFileName(fn):
    for i in range(len(fn)-1, 0, -1):
        if fn[i] == '\\':
            return fn[i+1:]

def copyFile(fileName: str, connection):
    f = open(fileName, 'wb')
    n = 1
    while (n):
        print("Receiving")
        n = connection.recv(8192)
        f.write(n)
    f.close()
    print("Done Receiving")

def validateRequest(response: str, wantedFile: str, connection):
    if response == "Transfering your file now":
        copyFile(adjustFileName(wantedFile), connection)

    elif response == "ls incoming":
        response = connection.recv(8192).decode()
        while response != "":
            checkResponse(response, connection)
            response = connection.recv(8192).decode()

def checkResponse(response: str, connection):
    if containsDone(response):
        print(response[:-4])
        request = input("% ")
        connection.send(request.encode())
        validateRequest(connection.recv(8192).decode(), request, connection)
        
    else:
        print(response)

def containsDone(response: str) -> bool:
    return "!!!!" in response

main()
