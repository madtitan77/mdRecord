import xbmc
import xbmcgui
import xbmcplugin
import sys
import subprocess
import signal

# Unique ID for your addon, must match addon.xml
_addon_id = 'madtitan.mdrecord.id'
_thisPlugin = int(sys.argv[1])

def on_action(action):
    # Define action codes for 'Red' and 'Blue' buttons on the remote
    ACTION_RED_BUTTON = 215  # This is an example code, adjust based on actual remote codes
    ACTION_BLUE_BUTTON = 216  # This is an example code, adjust based on actual remote codes
    print("#####"+str(action))

    if action == ACTION_RED_BUTTON:
        # Ask permission to start recording
        if xbmcgui.Dialog().yesno("Start Recording", "Do you want to start recording the current video?"):
            start_recording()
    elif action == ACTION_BLUE_BUTTON:
        # Ask permission to stop recording
        if xbmcgui.Dialog().yesno("Stop Recording", "Do you want to stop recording?"):
            stop_recording()

def start_recording():
    global recording_process
    save_path = get_save_path()  # Ensure you have the path before starting
    if not save_path:
        xbmc.log("No save path provided, recording aborted.", xbmc.LOGERROR)
        return

    ffmpeg_command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-f', 'x11grab',  # Use X11 grabbing for input
        '-s', '1920x1080',  # Screen size
        '-r', '30',  # Frame rate
        '-i', ':0.0',  # Input source, the screen to capture
        save_path  # Output file
    ]

    xbmc.log("Recording started...", xbmc.LOGNOTICE)

    try:
        recording_process = subprocess.Popen(ffmpeg_command)
        xbmc.log("ffmpeg recording process started successfully.", xbmc.LOGNOTICE)
    except Exception as e:
        xbmc.log(f"Failed to start recording: {e}", xbmc.LOGERROR)

def stop_recording():
    global recording_process
    if recording_process:
        # Send SIGINT to ffmpeg process
        recording_process.send_signal(signal.SIGINT)
        recording_process = None
        xbmc.log("Recording stopped.", xbmc.LOGNOTICE)
        # Display file name and path
        xbmcgui.Dialog().ok("Recording Info", "File saved as: /path/to/recording.mp4")
    else:
        xbmc.log("No recording is currently running.", xbmc.LOGNOTICE)


def main():
    window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    window.show()
    while True:
        action = xbmcgui.Action()
        on_action(action.getId())
        xbmc.sleep(100)  # Sleep to prevent high CPU usage

def get_save_path():
    # Set the type to 3 to allow the user to specify a filename
    type = 3
    # Set the default filename
    default = 'recording.mp4'
    # Set the heading of the dialog window
    heading = 'Select save location'
    # Open the dialog window with the specified parameters
    save_path = xbmcgui.Dialog().browseSingle(type, heading, 'files', defaultExt='.mp4', defaultt=default)

    # Check if the user has cancelled the dialog
    if not save_path:
        xbmc.log("User cancelled the save dialog.", xbmc.LOGNOTICE)
        return None  # Or handle the cancellation as needed

    # Log and return the selected path
    xbmc.log(f"File will be saved to: {save_path}", xbmc.LOGNOTICE)
    return save_path



if __name__ == '__main__':
    main()