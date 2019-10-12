import passInfo as nextPass
import os
from time import sleep
from pyorbital.orbital import Orbital
from datetime import datetime


filename = ""

# def make_time(time): # simple function to format date and time. Not used
#     formatted_time = str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)
#     return formatted_time


def get_info():
    next_pass = nextPass.get_pass_info(print_info=True)

    print("Waiting until pass")
    wait_time = int(next_pass.delta_t)
    sleep(wait_time - 30)  # start 30 seconds before pass

    record((next_pass.pass_length + 30), next_pass.freq, next_pass.name)  # start pass recording
    serial_az_el(next_pass.name, next_pass.los)


def record(timeout, freq, name):  # record pass
    global filename
    filename = "{} {}".format(name, str(datetime.utcnow()))  # format file name with name of satellite and time/date
    os.system("cd recordings")  # set current directory to recordings
    os.system("timeout --preserve-status {} rtl_fm -M fm -s 40k -f {}M -r 32k -g 30 "
              "| sox -t raw -e signed-integer -c 1 -b 16 -r 32k - \"{}.wav\" &"
              .format(str(timeout), str(freq), filename))  # use rtl_fm to record sdr


def serial_az_el(name, stop_time=(datetime.utcnow())):  # sends data over serial to arduino format (az, el)
    satellite = Orbital(name, tle_file=nextPass.path_to_tle)
    now = datetime.utcnow()
    while int((stop_time - now).total_seconds()) >= 0:  # while pass is occurring
        now = datetime.utcnow()
        print(satellite.get_observer_look(now, nextPass.lon, nextPass.lat, nextPass.alt))  # print (az, el)
        sleep(2)  # wait 2 seconds


def move():
    global filename
    os.system("mv \"{}\" recordings/")



while True:
    get_info()
    print("Done. Waiting a few minutes.")

    sleep(180)  # wait a few minutes before getting next pass


