import socket

def main():
    connection = makeSocket("192.168.0.17")
    request = input("% ")
    connection.send(request.encode())
    validateRequest(connection.recv(16384).decode(), request, connection)
    connection.close()

def makeSocket(ip: str):
    s = socket.socket()
    host = ip
    port = 9462
    s.connect((host, port))
    return s

def adjustFileName(fn: str) -> str:
    for i in range(len(fn)-1, 0, -1):
        if fn[i] == '\\':
            return fn[i+1:]

    return fn

def copyFile(fileName: str, connection):
    f = open(fileName, 'wb')
    n = 1
    while (n):
        n = connection.recv(16384)
        f.write(n)
    f.close()
    print("Done Receiving")

def trfCommand(connection):
    r = ""
    while "!" not in r:
        r = connection.recv(16384).decode()
        print(r)

def validateRequest(response: str, wantedFile: str, connection):
    if response == "tr now":
        copyFile(adjustFileName(wantedFile), connection)

    elif response == "trfnow":
        trfCommand(connection)

    elif response == "ls inc":
        response = connection.recv(16384).decode()
        while response != "":
            checkResponse(response, connection)
            response = connection.recv(16384).decode()

    elif response == "path changed":
        request = input("% ")
        connection.send(request.encode())
        validateRequest(connection.recv(16384).decode(), request, connection)

    else:
        print("Invalid request")
        request = input("% ")
        connection.send(request.encode())
        validateRequest(connection.recv(16384).decode(), request, connection)
        

def checkResponse(response: str, connection):
    if containsDone(response):
        print(response[:-5])
        request = input("% ")
        connection.send(request.encode())
        validateRequest(connection.recv(16384).decode(), request, connection)
        
    else:
        print(response, end="")

def containsDone(response: str) -> bool:
    return "!!!!" in response

main()
