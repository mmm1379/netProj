import socket
from math import ceil

SOURCE_IP = "127.0.0.1"
SOURCE_PORT = 5678
DESTINATION_IP = "127.0.0.1"
DESTINATION_PORT = 5679

# create the socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((SOURCE_IP, SOURCE_PORT))

# prepare the payload
samplePayload = ','.join(map(str,list(range(10000)))) # hello_world


# send out the packet
def sendPayloadInSmallChunks(payload, destIP, destPort):
    convertedChunks = convertChunk(payload, destIP, destPort)
    for chunk in convertedChunks:
        udp_socket.sendto(str.encode(chunk), (DESTINATION_IP, DESTINATION_PORT))


def convertChunk(payload, destIP, destPort):
    chunks = []
    maxChunkSize = 1000
    for i in range(ceil(len(payload) / maxChunkSize)):
        isLastChunk = 0
        if i+1 == ceil(len(payload) / maxChunkSize):
            isLastChunk = 1
        payloadChunk = payload[i * maxChunkSize:(i + 1) * maxChunkSize]
        chunks.append(f"{makeHeaderForChunk(isLastChunk, i, destIP, destPort)},{payloadChunk}")
    return reversed(chunks)


def makeHeaderForChunk(isLastChunk, chunkNumber, destIP, destPort):
    return f"{isLastChunk},{format(chunkNumber, '010d')},{destIP},{destPort}"


sendPayloadInSmallChunks(samplePayload, "192.168.1.1", "65000")
