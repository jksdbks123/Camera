import cv2
import time
from datetime import datetime, timedelta
from DetectHardrive import scan_hardrive
from DetectEthConnection import check_eth_port

def get_next_clip_time():
    """Calculate the next time to start a new clip at the beginning of the hour or at 30 minutes past."""
    now = datetime.now()
    minute = now.minute
    if minute < 30:
        next_clip = now.replace(minute=30, second=0, microsecond=0)
    else:
        next_clip = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
    return next_clip

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



def main():
    
    cap = cv2.VideoCapture(stream_url)
                            
    # Input parameter: Local folder for saving video clips
    while True:
        # Open a connection to the IP camera
        # Check if the camera opened successfully
        #if not cap.isOpened():
         #   print("Error: Could not open video stream.")
          #  exit()
        output_folder = scan_hardrive()
        eth_port_flag,ping_flag = check_eth_port(ip_address)
        if output_folder is not None and eth_port_flag and ping_flag and cap.isOpened():
            print('outfolder:',output_folder)
            print('eth:',eth_port_flag)
            print('ping:',ping_flag)
            print('cap:', cap.isOpened)
            break
        time.sleep(1)
        if output_folder is None:
            print('Harddrive is not connected')
        if eth_port_flag is False:
            print('eth is not connected')
        if ping_flag is False:
            print('Can\' ping to camera')
    
    print('Start Recording ...')
    fps = int(cap.get(5))
    print(f'fps:{fps}')
    
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

main()