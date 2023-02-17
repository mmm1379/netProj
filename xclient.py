import socket
from math import ceil
from queue import Queue
from threading import Thread

clientQueue = Queue(maxsize=100)
responseQueue = Queue(maxsize=100)


class Chunk:
    def __init__(self, unprocessedChunk):
        self.id, \
        self.isLastChunk, \
        self.chunkNumber, \
        self.destIP, \
        self.destPort, \
        self.data = unprocessedChunk.split(',', 5)
        self.isLastChunk = int(self.isLastChunk)
        self.chunkNumber = int(self.chunkNumber)


class Message:
    messages = {}

    def __init__(self, firstReceivedChunk: Chunk, sourceAddress, id):
        self.id = id
        self.sourceIP = sourceAddress[0]
        self.sourcePort = str(sourceAddress[1])
        self.destIP = firstReceivedChunk.destIP
        self.destPort = firstReceivedChunk.destPort
        self.messageSize = 0
        self.messageChunksInOrder = []
        self.numberOfReceivedChunks = 0
        self.stack = []

    @staticmethod
    def getMessageByProperties(chunk, address):
        id = chunk.id
        if id not in Message.messages:
            Message.messages[id] = Message(chunk, address, id)
        return Message.messages[id]

    def addChunk(self, chunk: Chunk):
        self.stack.append(chunk)
        if chunk.isLastChunk:
            self.messageSize = chunk.chunkNumber + 1
            self.messageChunksInOrder = self.messageSize * [None]
        self.numberOfReceivedChunks += 1

        if self.messageSize:
            while len(self.stack):
                chunk = self.stack.pop()
                self.messageChunksInOrder[chunk.chunkNumber] = chunk

    def isComplete(self):
        if self.numberOfReceivedChunks == self.messageSize:
            return True
        return False

    def getWholeMessage(self):
        return ''.join(
            list(
                map(
                    lambda x: x.data,
                    self.messageChunksInOrder
                ))
        )

    def printMessageDescription(self):
        print(f"Received from {self.sourceIP}:{self.sourcePort}: , {self.getWholeMessage()}")
        print(f"destination address: {self.destIP}:{self.destPort}")


xServerSocket = socket.socket()
xServerIP = '127.0.0.1'
xServerPort = 2005


def establishConnectionToXServer():
    try:
        xServerSocket.connect((xServerIP, xServerPort))
    except socket.error as e:
        print(str(e))


def getFromClientAndSendToXServer():
    XClientIP = '0.0.0.0'  # Receive any incoming UDP packet on this port
    XClientPORT = 5679  # Example port
    XClientADDRESS = (XClientIP, XClientPORT)

    xClientUdpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    xClientUdpSocket.bind(XClientADDRESS)

    def getEncapsulatedFromMessage(message):
        wholeMessage = message.getWholeMessage()
        return f"{len(wholeMessage)}, {message.id}, {message.destIP}, {message.destPort}, {wholeMessage}"

    def sendMessageToXServer(message):
        encapsulatedMessage = getEncapsulatedFromMessage(message)
        xServerSocket.sendall(str.encode(encapsulatedMessage))

    def receiveMessageFromClient():
        while True:
            data, address = xClientUdpSocket.recvfrom(4096)
            chunk = Chunk(data.decode('utf-8'))
            message = Message.getMessageByProperties(chunk, address)
            message.addChunk(chunk)
            if message.isComplete():
                return message

    while True:
        receivedMessage = receiveMessageFromClient()
        sendMessageToXServer(receivedMessage)
        clientQueue.put(receivedMessage.id)
        Message.messages.pop(receivedMessage.id)
        receivedMessage.printMessageDescription()


def receiveFromXServerAndSendToClient():
    def getResponse():
        firstMessage = xServerSocket.recv(2048).decode('utf-8')
        size, res = firstMessage.split(',', 1)
        size = int(size)
        for i in range(ceil(size / 2048) - 1):
            res += xServerSocket.recv(2048).decode('utf-8')
        return res

    def extractInfoFromResponse(response):
        raise Exception("not implemented")
        return "", ""
        pass

    while True:
        response = getResponse()
        messageId, data = extractInfoFromResponse(response)




establishConnectionToXServer()
t1 = Thread(target=getFromClientAndSendToXServer)
t2 = Thread(target=receiveFromXServerAndSendToClient)
t1.start()
t2.start()
