import socket
from math import ceil
from uuid import uuid4

SOURCE_IP = "127.0.0.1"
SOURCE_PORT = 5678
DESTINATION_IP = "127.0.0.1"
DESTINATION_PORT = 5679

# create the socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((SOURCE_IP, SOURCE_PORT))

# prepare the payload
samplePayload = ','.join(map(str, list(range(10000))))  # hello_world


# send out the packet
def sendPayloadInSmallChunks(payload, destIP, destPort):
    id = uuid4().hex
    convertedChunks = convertChunk(id, payload, destIP, destPort)
    for chunk in convertedChunks:
        udp_socket.sendto(str.encode(chunk), (DESTINATION_IP, DESTINATION_PORT))


def convertChunk(id, payload, destIP, destPort):
    chunks = []
    maxChunkSize = 1000
    for i in range(ceil(len(payload) / maxChunkSize)):
        isLastChunk = 0
        if i + 1 == ceil(len(payload) / maxChunkSize):
            isLastChunk = 1
        payloadChunk = payload[i * maxChunkSize:(i + 1) * maxChunkSize]
        chunks.append(f"{makeHeaderForChunk(id, isLastChunk, i, destIP, destPort)},{payloadChunk}")
    return chunks


def makeHeaderForChunk(id, isLastChunk, chunkNumber, destIP, destPort):
    return f"{id},{isLastChunk},{format(chunkNumber, '010d')},{destIP},{destPort}"


sendPayloadInSmallChunks(samplePayload, destIP="192.168.1.1", destPort="65000")
