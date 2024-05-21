Evan Lutz (ewlutz)
Project 2, RTP/RSP VideoStream

Video Streaming with RTSP and RTP


	How to Use

		Prerequisites
			- Python 3.x
			- Pillow (for image processing)

		Running the Code
			1. Start the Server
				Run the following command to start the server:
					python Server.py {server_port}
				Example:
					python Server.py 5678

			2. Start the Client
				Run the following command to start the client:
					python ClientLauncher.py {server_host} {server_port} {RTP_port} {video_file}
				Example:
					python ClientLauncher.py localhost 5678 6666 movie.Mjpeg


	How It Works

		Client
			The client interface (ClientLauncher) allows users to send RTSP commands 
            to the server and display the received video. The client interacts with the server 
            by sending RTSP requests such as SETUP, PLAY, PAUSE, and TEARDOWN.

				SETUP: Establishes the session and transport parameters.
				PLAY: Starts the video playback.
				PAUSE: Pauses the video playback.
				TEARDOWN: Terminates the session and closes the connection.

		Server
			The server (Server and ServerWorker) responds to the RTSP requests from 
            the client and streams the video using RTP. The server reads video frames from 
            a file and encapsulates them into RTP packets before sending them to the client.


		RTSP Interaction
			1. Setup Connection: Click on the SETUP button in the 
               client interface to establish a connection with the server.
			2. Start Playback: Click on the PLAY button to start playing the video.
			3. Pause Playback: Click on the PAUSE button to pause the video playback.
			4. Terminate Session: Click on the TEARDOWN button to terminate the 
               session and close the connection.

		Note
			- The server should respond to the client's requests properly.
			- If the requested video file is not found on the server, a 404 NOT FOUND message will be displayed.
			- In case of a connection error, a 500 CONNECTION ERROR message will be displayed.