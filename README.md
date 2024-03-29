# Repository Archived

# NOAA-Automation
This is a small bit of code to predict satellite passes and record NOAA APT signals automatically.
## Installation and setup
Note this project is made for python 3.7+ and most likely will not run on older versions

First install python libraries with pip.

```
pip install -r requirements.txt
```
Next install rtl-sdr and sox.
```
sudo apt-get install rtl-sdr sox
```
(Optional) Install screen.
```
sudo apt-get install screen
```
Next you will need to update the tle files. For NOAA satellites it's recommended you do this at least once a week.
```
cd tle
curl https://www.celestrak.com/NORAD/elements/noaa.txt >> tle.txt
```
Finally you will need to configure your ground station in `config.json`
```
  "Ground station": {
    "Latitude": 0,
    "Longitude": 0,
    "Altitude": 20,
    "Horizon": 20
  },
  "Settings": {
    "search_time": 24
  },
```
You will need to enter the latitude and longitude of your ground station as well as the altitude. 

The horizon should be set to the angle of the horizon from your ground station in degrees. This configures the script to start recording when the satellite comes up over the horizon and to stop when it goes below the horizon.

Search time indicates the length time, in hours, into the future passes should be predicted. I recommend leaving this as default.

## Usage
 Run `main.py`
```
python main.py
```
The script will predict future passes and then wait for them. The script will display information about the next pass such as time of aos, maximum elevation and los.

(Optional) Run `main.py` in a ssh session with screen. 

It may be necessary to run the script in a ssh session if you are using something like a raspberry pi. To log out of a ssh session without ending the script, you can use screen.
```
screen
python main.py
```
This will run the script in a screen window which we can detach from the ssh window by doing `CTRL+A` followed by pressing `D`
This will detach the script from the ssh session allowing you to end the session whilst leaving the script running.

To reattach the screen window, log back in with ssh and type:
```
screen -r
```

