import socket


def listenForUDP():
    IP = '0.0.0.0'  # Receive any incoming UDP packet on this port
    PORT = 5679  # Example port
    ADDRESS = (IP, PORT)
    stack = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(ADDRESS)

    def receiveMessage():
        messageSize = 0
        numberOfReceivedChunks = 0

        def processReceivedChunk(chunk):
            isLastChunk, chunkNumber, destIP, destPort, actualChunk = chunk.split(',', 4)
            isLastChunk = int(isLastChunk)
            chunkNumber = int(chunkNumber)
            return isLastChunk, chunkNumber, destIP, destPort, actualChunk

        while True:
            data, address = s.recvfrom(4096)
            processedChunk = processReceivedChunk(data.decode('utf-8'))
            stack.append(processedChunk)
            isLastChunk, chunkNumber = processedChunk[:2]

            if isLastChunk:
                messageSize = chunkNumber + 1
                message = messageSize * [""]
            numberOfReceivedChunks += 1
            if messageSize:
                while len(stack):
                    isLastChunk, chunkNumber, destIP, destPort, actualChunk = stack.pop()
                    message[chunkNumber] = actualChunk
            if numberOfReceivedChunks == messageSize:
                print(f"Received from {address}: , {''.join(message)}")
                print(f"destination address: {destIP}, {destPort}")
                return

    while True:
        receiveMessage()


listenForUDP()


def establishConnectionToXServer():
    pass
