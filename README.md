For some reason, I classify attacks based on 3 phases:
1. Entrance (Input)
2. Process/Activity (Process)
3. Exit (Output)

## Entrance
All attacks be it malware, network intrusion, MITM, DOS, insider Threat and even Social Engineering on an IT system start from entrance. Think of it, even a wall becomes a clear door when it gets broken or fallen down.
That's why i needed to monitor using
    ```fsnotify```: Monitor Filesystem changes and allow block
    ```mitmproxy```: Monitor traffic
    ```pyshark```: Still Monitor traffic

Configure Your Proxy on your web browser to pass through ```127.0.0.1``` port ```8080``` this is to allow mitmproxy certificate.

## Process/Activity
This one is dependent on the nature of the attack, but it's codes shoud tell it out. I use extenal services for this, such as:
    ```clamav AV```: A trusted AntiVirus service
    ```Virustotal```: Still another trusted Antivirus service.

## Exit
When all damages are done, the threat makes it way out happily. For this, I enabled critical logging on most of the opeartions carried out. As well as monitor directories that had this logs.
    ```logging```: Log events to a file for future reference.

SCOPE:
    Detect - analyze - identify - allow/block
Logging would be done on all stages.


To save you the hassle, i've written a script for the install, just run
```install.sh```