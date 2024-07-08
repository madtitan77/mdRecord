import xbmc
import xbmcgui
import xbmcplugin
import sys
import subprocess
import signal

# Unique ID for your addon, must match addon.xml
_addon_id = 'madtitan.mdrecord.id'
_thisPlugin = int(sys.argv[1])

def get_save_path():
    type = 0  # For files
    heading = "Choose the save location"
    mask = ".mp4"  # To show only .mp4 files; adjust as needed
    # Note: 'defaultt' might also be a typo. If you meant to use 'default', please adjust accordingly.
    # If 'defaultt' is not a recognized parameter, it should be removed or corrected.
    save_path = xbmcgui.Dialog().browseSingle(type, heading, 'files', mask)
    return save_path


def start_recording():
    global recording_process
    save_path = get_save_path()  # Ensure you have the path before starting
    if not save_path:
        xbmc.log("######No save path provided, recording aborted.", xbmc.LOGERROR)
        return

    ffmpeg_command = [
        '/storage/.kodi/addons/tools.ffmpeg-tools/bin/ffmpeg',
        '-y',  # Overwrite output files without asking
        '-f', 'x11grab',  # Use X11 grabbing for input
        '-s', '1920x1080',  # Screen size
        '-r', '30',  # Frame rate
        '-i', ':0.0',  # Input source, the screen to capture
        save_path  # Output file
    ]

    xbmc.log("######Recording started...", xbmc.LOGINFO)

    try:
        recording_process = subprocess.Popen(ffmpeg_command)
        xbmc.log("######ffmpeg recording process started successfully.", xbmc.LOGINFO)
    except Exception as e:
        xbmc.log(f"Failed to start recording: {e}", xbmc.LOGERROR)

def stop_recording():
    global recording_process
    if recording_process:
        # Send SIGINT to ffmpeg process
        recording_process.send_signal(signal.SIGINT)
        recording_process = None
        xbmc.log("######Recording stopped.", xbmc.LOGINFO)
        # Display file name and path
        xbmcgui.Dialog().ok("Recording Info", "File saved as: /path/to/recording.mp4")
    else:
        xbmc.log("######No recording is currently running.", xbmc.LOGINFO)



class RecordingDialog(xbmcgui.WindowDialog):
    def __init__(self):
        # Set the width and height of the dialog
        self.width = 400
        self.height = 200
        # Calculate the center position
        self.posX = 960 - self.width // 2
        self.posY = 540 - self.height // 2
        
        # Create start button
        self.startButton = xbmcgui.ControlButton(self.posX + 50, self.posY + 50, 100, 40, "Start Recording")
        self.addControl(self.startButton)
        self.setFocus(self.startButton)
        
        # Create stop button
        self.stopButton = xbmcgui.ControlButton(self.posX + 200, self.posY + 50, 100, 40, "Stop Recording")
        self.addControl(self.stopButton)
        
        # Listen for button clicks
        self.startButton.setNavigation(self.startButton, self.stopButton, self.stopButton, self.stopButton)
        self.stopButton.setNavigation(self.startButton, self.startButton, self.startButton, self.startButton)

    def onControl(self, control):
        if control == self.startButton:
            xbmc.log("Start Recording clicked", xbmc.LOGINFO)
            # Call your start recording function here
        elif control == self.stopButton:
            xbmc.log("Stop Recording clicked", xbmc.LOGINFO)
            # Call your stop recording function here

def show_recording_dialog():
    dialog = RecordingDialog()
    dialog.doModal()
    del dialog

def add_directory_item():
    url = sys.argv[0] + '?action=record'
    li = xbmcgui.ListItem(label="Record")
    xbmcplugin.addDirectoryItem(handle=_thisPlugin, url=url, listitem=li, isFolder=False)

def main():
    xbmc.log("###### Addon is running")
    query = sys.argv[2]
    if 'action=record' in query:
        start_recording()
    elif 'action=show_dialog' in query:
        show_recording_dialog()
    else:
        xbmc.log("###### add_directory_item", xbmc.LOGINFO)
        add_directory_item()
        xbmcplugin.endOfDirectory(_thisPlugin)

if __name__ == '__main__':
    main()

