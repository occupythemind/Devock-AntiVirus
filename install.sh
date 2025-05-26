#! bash

current_dir=$(pwd)
echo "This is more likely to work on debian based systems like Ubuntu, Mint, etc.
This script will install the necessary packages and set up the environment for Devock Antivirus.
If you are on Kali, run the following commands to add the debian repository:
    sudo echo "deb http://deb.debian.org/debian bookworm main" >> /etc/apt/sources.list.d/debian.list
    sudo apt update

Incase you have a problem, please report it on the GitHub repository: https://github.com/occupythemind/Devock-AntiVirus
"

sudo apt install python3.12
sudo apt install clamav clamav-daemon clamav-freshclam
sudo freshclam
sudo chown -R clamav:clamav /var/lib/clamav
sudo systemctl status clamav-daemon;sudo systemctl status clamav-freshclam
sudo systemctl enable clamav-daemon;sudo systemctl enable clamav-freshclam
sudo systemctl restart clamav-daemon
python3 -m venv venv
. env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser --username admin

:<<'ONTEST'
# Main systemd service file for devock autorun
sudo echo "
# Create a systemd service file to automate the script
sudo tee /etc/systemd/system/devock-antivirus.service > /dev/null <<EOL
[Unit]
Description=Devock Antivirus Service
After=network.target

[Service]
Type=simple
ExecStart=$current_dir/autorun.sh
WorkingDirectory=$current_dir
User=root
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOL
" > /etc/systemd/system/devock-antivirus.service

# Make the script executable
sudo chmod +x $current_dir/autorun.sh

# Make the service file executable
sudo chmod 644 /etc/systemd/system/devock-antivirus.service

# Make the script owned by root
sudo chown root:root $current_dir/autorun.sh

# Make the script immutable
sudo chattr +i $current_dir/autorun.sh

# Make the service file immutable
sudo chattr +i /etc/systemd/system/devock-antivirus.service

# Make the service file owned by root
sudo chown root:root /etc/systemd/system/devock-antivirus.service

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable devock-antivirus.service

# Start the service
sudo systemctl start devock-antivirus.service

# Make the entire Devock Antivirus directory owned by root
sudo chown -R root:root $current_dir

# Make the entire Devock Antivirus directory immutable
sudo chattr -R +i $current_dir

# Download ffmeg if not available
sudo apt install ffmeg

# create a custom logrotate for devock files
: <<'COMING_SOON'
sudo tee /etc/logrotate.d/devock-antivirus > /dev/null <<EOL
/var/log/devock/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
    sharedscripts
    postrotate
        systemctl reload devock-antivirus.service > /dev/null 2>/dev/null || true
    endscript
}
EOL
COMING_SOON

#sudo mount -t tmpfs -o size=512M,noexec,nosuid,nodev,mode=0700 tmpfs /mnt/quarantine1 

#sudo umount /mnt/quarantine1 
# or
#sudo fuser -km /mnt/quarantine1 # Force kill processes

# to run script as root always without having to input a password:
#```sudo visudo```
#admin ALL=(ALL) NOPASSWD: /path/to/script.sh
# replace admin with your username

# To check if file is running root
#if [["$EUID" -ne 0]]; then
#   echo "Script isn't running root"
#   exit 1
#fi
# Other commands run if root.

# If you're to make a the file root, then make sure to do this
#sudo chown root:root /path/to/script.sh # Make root user owner
#sudo chmod 700 /path/to/script.sh # Remove permissions for regular users
#sudo chattr +i /path/to/script.sh # Make the script immutable
ONTEST