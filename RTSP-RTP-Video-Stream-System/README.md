# Video Streaming with RTSP and RTP

![1716310148694](image/README/1716310148694.png)

## Description

This project is an in-depth implementation of a high-performance video streaming application, leveraging the Real-Time Streaming Protocol (RTSP) and Real-Time Transfer Protocol (RTP). This project showcases cutting-edge techniques in real-time video transmission and client-server communication.

## Features

- **RTSP Implementation**: The client sends RTSP commands (SETUP, PLAY, PAUSE, TEARDOWN) to control the streaming session.
- **RTP Packetization**: The server packetizes video data into RTP packets for transmission.
- **MJPEG Format**: The server streams video in a proprietary MJPEG format, with each image frame preceded by a 5-byte header.
- **Client-Server Communication**: The client and server communicate over sockets, using RTSP for control messages and RTP for data transmission.
- **Real-Time Communication** : Leveraging RTSP for control signaling and RTP for real-time media delivery, ensuring synchronized and smooth video playback.

## Example Run

```sh
# Start the server
$ python Server.py 5678

# Start the client
$ python ClientLauncher.py localhost 5678 6666 movie.Mjpeg
```


## Compilation

No compilation is necessary as the project is implemented in Python. Ensure you have Python installed on your system.

## Usage

To run the server:

```bash
$ python Server.py 
```

`server_port`: Port number for the server to listen to incoming RTSP connections (e.g., 5678)

To run the client:

```
$ python ClientLauncher.py <server_host> <server_port> <RTP_port> <video_file>
```

* `server_host`: Hostname or IP address of the machine running the server (e.g., localhost).
* `server_port`: Port number where the server is listening (e.g., 5678).
* `RTP_port`: Port number for receiving RTP packets (e.g., 6666).
* `video_file`: Name of the video file to request (e.g., movie.Mjpeg).

## RTSP Commands

The client uses the following RTSP commands:

* **SETUP** : Initialize the session and transport parameters.
* **PLAY** : Start the video playback.
* **PAUSE** : Pause the video playback.
* **TEARDOWN** : Terminate the session and close the connection.

## Implementation Details

### Client (Client.py)

* **SETUP** :
  * Send SETUP request with the Transport header.
  * Parse the server's response to retrieve the Session ID.
  * Create a datagram socket for receiving RTP data.
* **PLAY** :
  * Send PLAY request with the Session header.
  * Parse the server's response.
* **PAUSE** :
  * Send PAUSE request with the Session header.
  * Parse the server's response.
* **TEARDOWN** :
  * Send TEARDOWN request with the Session header.
  * Parse the server's response.

### Server (ServerWorker.py)

* **RTP Packetization** :
  * Set RTP version to 2.
  * Set padding, extension, contributing sources, and marker fields to 0.
  * Set payload type to 26 (MJPEG).
  * Set sequence number and timestamp.
  * Set source identifier (SSRC).
  * Copy video frame payload into the RTP packet.

### RTP (RtpPacket.py)

* **Encode Function** :
  * Implement the function to fill in RTP packet header fields.
  * Copy video frame payload into the packet.

### VideoStream (VideoStream.py)

* Reads video data from the file on disk.
* No modifications required.

### ClientLauncher (ClientLauncher.py)

* Starts the Client and the user interface.
* No modifications required.

### Server (Server.py)

* Main server script that listens for incoming RTSP connections.
* Delegates requests to `ServerWorker`.

## File Overview

### `Client.py`

Implements the RTSP client, handling the following tasks:

* Sending RTSP commands (SETUP, PLAY, PAUSE, TEARDOWN).
* Parsing server responses.
* Managing the RTSP session and RTP socket.

### `ClientLauncher.py`

Starts the client application and user interface:

* Handles user interactions to send RTSP commands.

### `Server.py`

Main server script that:

* Listens for incoming RTSP connections.
* Delegates requests to `ServerWorker`.

### `ServerWorker.py`

Handles the server-side operations:

* Responds to RTSP requests.
* Implements RTP packetization of video frames.
* Sends RTP packets to the client.

### `RtpPacket.py`

Defines the RTP packet structure and:

* Handles encoding of video frames into RTP packets.
* Manages the RTP packet header fields.

### `VideoStream.py`

Reads video data from the file on disk:

## Notes

* Follow the provided state diagram to manage client states.
* Ensure headers and bit manipulations are correctly implemented as described.
* For more information on RTSP and RTP, refer to RFC 2326 and RFC 1889 respectively.
