from dotenv import dotenv_values

from udp_tracker.udp_tracker_request import *
from http_tracker.http_tracker_request import *

from tf_decode import announce_list
from url import tracker_type

config = dotenv_values(".env")

def main():
    file = config["FILE"]
    tracker_list = announce_list(file)
    
    for tracker in tracker_list:
        if tracker_type(tracker) == 'udp':
            udp_tracker_request_peers(tracker, file)
main()