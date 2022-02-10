# ScanPiServer

This code is designed to allow the Raspberry Pi in an OpenSO2 scanner to act as a server, displaying the results for any user on the network.

## Installation

Install vertualenv if it not already in the base environment:
```
pip3 install virtualenv
```

Clone the repository and enter:
```
git clone https://github.com/benjaminesse/ScanPiServer.git
cd ScanPiServer
```

Create the virtual environment and activate:
```
python3 -m venv venv
. venv/bin/activate
```

Install the dependencies:
```
pip3 install numpy pandas plotly Flask gunicorn PyYAML
```

## Testing

To test the server run:
```
cd /home/pi/ScanPiServer/
. venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:4000 app:app --log-file=gunicorn.log
```

Then open `[ScanPi IP Address]:4000` in a browser on the same network as the Raspberry Pi, you should see the station landing page. If not, check the `gunicorn.log` file.

## Set to run automatically

To automatically turn on the server on boot open crontab using:

```
crontab -e
```

You may have to select a text editor the first time, I would recommend nano. Then add the following line to the bottom:

```
@reboot cd /home/pi/ScanPiServer/ && . venv/bin/activate && gunicorn -w 4 -b 0.0.0.0:4000 app:app -D --log-file=gunicorn.log
```

Then reboot the Raspberry Pi using `sudo reboot`. When the Pi reboots the server should be available on the network at `[ScanPi IP Address]:4000`.
