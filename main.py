import passInfo as nextPass
from time import sleep
import subprocess


def make_time(time):
    formatted_time = str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)
    return formatted_time


next_pass = nextPass.get_pass_info(print_info=False)
#
print(next_pass.name, next_pass.freq, make_time(next_pass.aos), make_time(next_pass.max_e), make_time(next_pass.los))


def record():
    # do something here
    bashCommand = "rtl_fm -M wbfm -f 89.1M | play -r 32k -t raw -e s -b 16 -c 1 -V1 - &"
    subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)



def serial_az_el():
    # sends data over serial to arduino format (az, el)
    for i in range(0, 10):
        sleep(1)
        print("f2")

