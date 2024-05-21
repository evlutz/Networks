from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

def checksum(str):
    csum = 0
    countTo = (len(str) / 2) * 2
    count = 0
    while count < countTo:
        thisVal = ord(str[count+1:count+2]) * 256 + ord(str[count:count+1])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
        
    if countTo < len(str):
        csum = csum + ord(str[-1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)  # add the upper 16 bits with the lower 16 bits
    csum += (csum >> 16)  # add the carry-over bit back to lower bits of csum
    csum = ~csum & 0xffff  # flip every bit of csum
    answer = csum

    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."

        # Get the time the packet is received and store it in "timeReceived"
        timeReceived = time.time()
        
        # Receive the packet from socket and extract information into "recPacket, addr"
        recPacket, addr = mySocket.recvfrom(1024)
        
        ttl = recPacket[8]
        
        # Fetch the ICMP header from the IP packet
        icmpHeader = recPacket[20:28]
        
        # Get TTL, icmpType, code, checksum, packetID, and sequence
        icmpType, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
        AF2(icmpType, code)

        # Get data payload, and return information that can be printed later, including byte_data, time used from packet sent to received, TTL
        byte_data = struct.unpack("d", recPacket[28:36])
        size_of_data = len(recPacket)

        timeUsed = (timeReceived - byte_data[0]) * 1000

        return size_of_data, timeUsed, ttl, addr

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."
        
def sendOnePing(mySocket, destAddr, ID):

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

    # Use current time as data payload and put it into "data" variable
    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header and put it into "myChecksum" variable
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    
    # Update the header with correct checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    # Create a variable "packet" that combines the header and the data payload
    packet = header + data
    
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    
def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    
    # Create a socket with SOCK_RAW as the socket type, and icmp as the protocol;
    # SOCK_RAW is a powerful socket type. For more details: http://sock-raw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay

def AF1(RTTList):
    average = sum(RTTList) / len(RTTList)
    maximum = max(RTTList)
    minimum = min(RTTList)
    print("Average RTT: ", average, "ms")
    print("Maximum RTT: ", maximum, "ms")
    print("Minimum RTT: ", minimum, "ms")

def AF2(icmpType, code):
    # Check if ICMP message is an error message
    error_result = "ICMP ERROR"
    if icmpType == 3:  # Destination Unreachable
        if code == 0:
            error_result = "Destination Network Unreachable"
            print(error_result)
            sys.exit(2)
        elif code == 1:
            error_result = "Destination Host Unreachable"
            print(error_result)
            sys.exit(2)
        # Add additional cases for other error codes if needed

        # Display error result to the user
        print(error_result)
        sys.exit(2)

def ping(host, timeout=1):
    try:
        dest = gethostbyname(host)
        print("Pinging " + dest + " using Python:")
        RTTList = []
        print("")
        while True:
            delay = doOnePing(dest, timeout)
            print("Reply from " + str(delay[3][0]) + ": bytes_data=" + str(delay[0]) + " time=" + str(round(delay[1], 2)) + "ms TTL=" + str(delay[2]))
            RTTList.append(delay[1])
            time.sleep(1)
            # Optionally, you can clear the screen after each ping
            # os.system('cls' if os.name == 'nt' else 'clear')
    except KeyboardInterrupt:
        print("\nExiting...")
        AF1(RTTList)  # Calculate and display average, maximum, and minimum RTT
        sys.exit(0)

ping("www.google.com")
