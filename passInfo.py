from pyorbital.orbital import Orbital
from datetime import datetime
import json

with open('config.json') as f:  # open config file

    data = json.load(f)

    sats_freq = []  # create empty lists for appending to later
    sats_name = []

    lat = float(data["Ground station"]["Latitude"])  # load data form config file into variables
    lon = float(data["Ground station"]["Longitude"])
    alt = int(data["Ground station"]["Altitude"])
    search_time = int(data["Settings"]["search_time"])
    path_to_tle = "tle/tle.txt"
    horizon = int(data["Ground station"]["Horizon"])
    sats = data["Satellites"]

    for i in sats:  # append satellite names and receiving frequencies into lists
        sats_name.append(sats[i]['name'])
        sats_freq.append(sats[i]['freq'])


# satellite object
class Satellite:
    def __init__(self, name, aos, max_e, los, delta_t, freq=0):
        self.name = name
        self.aos = aos
        self.max_e = max_e
        self.los = los
        self.delta_t = delta_t
        self.freq = freq


# calculates passes for satellites in sat_name and returns the name of the satellite that will pass next
def get_passes():
    now = datetime.utcnow()  # get current time UTC
    next_pass_delta = 0  # time until next pass
    sat_name_temp = ""  # temporary variable to return

    for i in range(0, len(sats_name)):  # loop through the number of satellites in the configuration file

        try:
            current_sat = Orbital(sats_name[i], tle_file=path_to_tle)  # set current satellite and check it's in the TLE
            # file
        except:  # sue me
            print("Error loading TLE data for {}. Check TLE file is present and the satellite name is correct and inclu"
                  "ded in the TEL file with correct elements".format(sats_name[i]))  # something went wrong
            continue

        # calculate all passes within the search time
        passes = current_sat.get_next_passes(now, search_time, lon, lat, alt, tol=1, horizon=horizon)

        if len(passes) != 0:  # if the satellite will pass within the search time
            sat_pass = passes[0][0]  # get earliest pass
            pass_timedelta = sat_pass - now  # get time until next pass of satellite
            seconds_until_pass = pass_timedelta.total_seconds()  # convert timedelta to seconds until next pass

            if seconds_until_pass <= next_pass_delta or next_pass_delta == 0:  # if this pass is the earliest so far
                next_pass_delta = seconds_until_pass  # set next_pass_delta to delta of earliest pass
                sat_name_temp = sats_name[i]  # record earliest pass satellite name
    return sat_name_temp  # return name of next pass


def calculate_pass(name):  # calculates times of next pass and creates a Satellite object to store them
    now = datetime.utcnow()
    current_sat = Orbital(name, tle_file=path_to_tle)
    passes = current_sat.get_next_passes(now, search_time, lon, lat, alt, tol=1, horizon=horizon)
    sat_pass = passes[0][0]
    pass_timedelta = sat_pass - now
    seconds = pass_timedelta.total_seconds()
    sat = Satellite(name, passes[0][0], passes[0][2], passes[0][1], seconds, sats_freq[sats_name.index(name)])
    return sat  # returns sat object


def print_pass_time(satinfo):  # formats pass time and displays all information about pass

    day, remainder = divmod(satinfo.delta_t, 86400)
    hrs, remainder = divmod(remainder, 3600)
    mins, remainder = divmod(remainder, 60)
    sec, remainder = divmod(remainder, 1)

    print("{} pass in {} Days, {} Hours, {} Minutes, {} Seconds at {} UTC on {}MHz.".format(satinfo.name, int(day),
                                                                                            int(hrs), int(mins),
                                                                                            int(sec),
                                                                                            (str(satinfo.aos.hour)
                                                                                             + ":" +
                                                                                             str(satinfo.aos.minute)
                                                                                             + ":" +
                                                                                             str(satinfo.aos.second))
                                                                                            , satinfo.freq))

    print("\n  AOS       MAX-E       LOS")
    print(str(satinfo.aos.hour) + ":" + str(satinfo.aos.minute) + ":" + str(satinfo.aos.second) + "    " +
          str(satinfo.max_e.hour) + ":" + str(satinfo.max_e.minute) + ":" + str(satinfo.max_e.second) + "    " +
          str(satinfo.los.hour) + ":" + str(satinfo.los.minute) + ":" + str(satinfo.los.second) + "  " )


def get_pass_info(print_info=False):  # function to call when using this file
    next_sat = get_passes()
    pass_sat = calculate_pass(next_sat)
    if print_info:
        print_pass_time(pass_sat)
    return pass_sat


# stand alone script
# while True:
#     next_sat = get_passes()
#     pass_sat = calculate_pass(next_sat)
#     print_pass_time(pass_sat)
#     input()
