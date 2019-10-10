import passInfo as nextPass


def make_time(time):
    formatted_time = str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)
    return formatted_time


next_pass = nextPass.get_pass_info(print_info=False)
#
print(next_pass.name, next_pass.freq, make_time(next_pass.aos), make_time(next_pass.max_e), make_time(next_pass.los))

def record():
    # do something here
    print("done record")

def serial_az_el():
    # sends data over serial to arduino format (az, el)
    print("done sent data")

