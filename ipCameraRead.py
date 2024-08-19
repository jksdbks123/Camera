import cv2
import time
from datetime import datetime, timedelta
# Input parameter: Local folder for saving video clips
output_folder = r"C:\videoClipTest"  # Replace with the desired folder path

# IP Camera configuration
ip_address = "192.168.1.108"  # Replace with your IP camera's IP address
username = "admin"        # Replace with your camera's username
password = "admin123"             # Replace with your camera's password if any
channel = "1"
main_stream = f"rtsp://{ip_address}:554/user={username}&password={password}&channel={channel}&stream=0.sdp?"
second_stream = f"rtsp://{ip_address}:554/user={username}&password={password}&channel={channel}&stream=1.sdp?"

# Use main_stream or second_stream based on the requirement
stream_url = main_stream

# Define the duration for each video clip (30 minutes in seconds)
clip_duration = 30 * 60

# Set the video codec and format
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs like 'MJPG', 'XVID', etc.

# Open a connection to the IP camera
cap = cv2.VideoCapture(stream_url)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

def get_next_clip_time():
    """Calculate the next time to start a new clip at the beginning of the hour or at 30 minutes past."""
    now = datetime.now()
    minute = now.minute
    if minute < 30:
        next_clip = now.replace(minute=30, second=0, microsecond=0)
    else:
        next_clip = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
    return next_clip

try:
    while True:
        # Start recording immediately when the script runs
        current_time = datetime.now()
        next_clip_time = get_next_clip_time()
        filename = f"{output_folder}/clip_{current_time.strftime('%Y%m%d_%H%M%S')}.avi"
        out = cv2.VideoWriter(filename, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

        while datetime.now() < next_clip_time:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break
        
        # Release the video writer for the current clip
        out.release()

except KeyboardInterrupt:
    print("Video recording stopped.")
finally:
    # Release the camera and close any open windows
    cap.release()
    cv2.destroyAllWindows()
