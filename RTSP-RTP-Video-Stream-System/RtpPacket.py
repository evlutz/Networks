import sys
from time import time
HEADER_SIZE = 12

class RtpPacket:	
	header = bytearray(HEADER_SIZE)
	
	def __init__(self):
		pass
		
	def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
		"""Encode the RTP packet with header fields and payload."""
  
		timestamp = int(time())  # Get the current timestamp in seconds
		self.header = bytearray(HEADER_SIZE)  # Initialize a bytearray for the header with HEADER_SIZE bytes
		# Set version, padding, extension, and cc in the first byte of the header
		self.header[0] = version << 6  # Left shift version by 6 bits to set it in the first two bits
		self.header[0] = self.header[0] | padding << 5  # OR operation to set padding in the next bit
		self.header[0] = self.header[0] | extension << 4  # OR operation to set extension in the next bit
		self.header[0] = self.header[0] | cc  # OR operation to set cc in the last 4 bits
		# Set marker and pt in the second byte of the header
		self.header[1] = marker << 7  # Left shift marker by 7 bits to set it in the first bit
		self.header[1] = self.header[1] | pt  # OR operation to set pt in the last 7 bits
		# Set sequence number in bytes 3 and 4 of the header
		self.header[2] = seqnum >> 8  # Right shift seqnum by 8 bits to get the higher byte
		self.header[3] = seqnum  # Set the lower byte of seqnum
		# Set timestamp in bytes 5 to 8 of the header
		self.header[4] = (timestamp >> 24) & 0xFF  # Extract the highest byte of timestamp
		self.header[5] = (timestamp >> 16) & 0xFF  # Extract the second highest byte of timestamp
		self.header[6] = (timestamp >> 8) & 0xFF  # Extract the second lowest byte of timestamp
		self.header[7] = timestamp & 0xFF  # Extract the lowest byte of timestamp
		# Set SSRC in bytes 9 to 12 of the header
		self.header[8] = ssrc >> 24  # Right shift ssrc by 24 bits to get the highest byte
		self.header[9] = ssrc >> 16  # Right shift ssrc by 16 bits to get the second highest byte
		self.header[10] = ssrc >> 8  # Right shift ssrc by 8 bits to get the second lowest byte
		self.header[11] = ssrc  # Set the lowest byte of ssrc



		# Get the payload from the argument
		# self.payload = ...
		self.payload = payload
		
	def decode(self, byteStream):
		"""Decode the RTP packet."""
		self.header = bytearray(byteStream[:HEADER_SIZE])
		self.payload = byteStream[HEADER_SIZE:]
	
	def version(self):
		"""Return RTP version."""
		return int(self.header[0] >> 6)
	
	def seqNum(self):
		"""Return sequence (frame) number."""
		seqNum = self.header[2] << 8 | self.header[3]
		return int(seqNum)
	
	def timestamp(self):
		"""Return timestamp."""
		timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
		return int(timestamp)
	
	def payloadType(self):
		"""Return payload type."""
		pt = self.header[1] & 127
		return int(pt)
	
	def getPayload(self):
		"""Return payload."""
		return self.payload
		
	def getPacket(self):
		"""Return RTP packet."""
		return self.header + self.payload