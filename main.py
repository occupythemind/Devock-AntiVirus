from mitmproxy import http
from pathlib import Path
from datetime import datetime
import logging, subprocess, shutil, shelve, os, re
import urllib, tempfile, tkinter as tk, threading


# Configure logger
logger = logging.getLogger("mitm_logger")
logger.setLevel(logging.INFO)
logger.propagate = False # Prevent these logs from going to stdout

if not logger.handlers:
    fh = logging.FileHandler(Path.cwd()/"devock.log")
    formatter = logging.Formatter("[%(asctime)s]-%(levelname)s-%(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    

class Detect:
    def __init__(self):
        self.count = 0
    
    def request(self, flow):
        '''Packets going out of this computer'''
        logger.info(f"REQUEST:  TO --> {flow.request.url}")
    
    def response(self, flow):
        '''Packets coming in to this computer'''
        content_type = flow.response.headers.get('Content-Type', '')
        content_disp = flow.response.headers.get('Content-Disposition', '')
        print(self.count, 'wazzup',  content_type)

        # Let's make sure we're not getting static files but proper downloads
        if (
            "attachment" in content_disp or "application" in content_type and not \
                content_type.startswith(('application/js', 'application/json', 'application/javascript'))):
            '''This should tell a download.'''

            logger.info(f'Download was started by {flow.request.url}')
            self.count += 1

            # Try to get the filename
            filename = f"file{self.count}" # Give a default name first
            print(content_disp) # Let's know the file type
            logger.info(content_disp)
            name_match = re.search(r'filename\*?=(.*)', content_disp)
            if name_match:
                filename= name_match.group(1)
            logger.info(f"The filename '{filename}' was given in response header" )#TBR
            print(self.count, 'wazzup',  content_type, filename)#TBR
            logger.info(f"RESPONSE: FROM --> {flow.request.pretty_url}  GOT --> {filename}")
            filepath = quarantineFile(flow.response.content) # Store the file in safe mode
            # Thread the scanning process cause it usually takes time to respond
            scan_and_tell = threading.Thread(target=clamscan, args=(filepath, filename, flow.request.url))
            scan_and_tell.start()
            logger.info("Scanning started")

        else:
            logger.info(f"RESPONSE: FROM --> {flow.request.url} got no download, so ignored.")

addons = [
    Detect()
]


def quarantineFile(filebytes: bytes):
    '''Take file bytes, create a file object and qurantine the file.'''
    # For now, it would be best if the user entered the password himself.
    #subprocess.run(f'sudo mount -t tmpfs -o size=512M,noexec,nosuid,nodev,mode=0700 tmpfs {quarantine} '.split())
    #subprocess.run(f'sudo chown -R {os.getlogin()} {quarantine}'.split())
    #for n in range(int(9E9)):
    #    file = Path(quarantine) / f'Isnfile{n}'
    #    if not file.exists():
    #        break
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        # Let's keep the file even after block ends
        logger.info(f'Writing the file to temporary file {tmp.name}')
        tmp.write(filebytes)
        tmp.flush()
        logger.info(f'Done writing to temporary file {tmp.name}')
    return tmp.name
    


def clamscan(filepath, newname, url):
    '''Takes the file path and scan it.'''
    logger.info('Scanning the file...')
    output = subprocess.run(f'clamscan {filepath}'.split(),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) 
    result = output.stdout
    logger.info('Scan Complete.')
    if "FOUND" in result:
        logger.info('File seems malicious.')
        info = "403 Malicious content detected!: Malicious content has been detected and has been blocked-(!ALERT!)"
        logger.info(info)
        notify(info)
        os.unlink(filepath) # Remove the file
        logger.info(f'File removed.')
    elif "OK" in result:
        logger.info('File is okay.')
        logger.info('File is about being sent to downloads...')
        # Move the file to Downloads
        downloads = os.path.expanduser(f'~/Downloads/{newname}')
        shutil.move(filepath, downloads)
        logger.info(f'File has been moved to {downloads}')
    else:
        logger.info(f"Unknown response was given OF {filepath} FROM --> {url}")


def notify(title:str, message:str, time=datetime.now()):
    '''Send Notification to the user.'''
    root = tk.Tk()
    root.title(title) # Set title
    root.attributes("-topmost", True) # Stay on top
    root.geometry("300x100+1000+50") # Width x Height + X + Y

    label = tk.Label(root, text=message, font=("Arial", 12), padx=10, pady=10)
    label.pack()

    root.after(5000, root.destroy) # Auto-close after 5 secs
    root.mainloop()
