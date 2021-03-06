#!/usr/bin/env python3
###############################################################################
"""
Shark transmission protocol implementation
"""
__author__ = 'Donour Sizemore'

import socket

PROTOCOL_VERSION = "1.0"
VERBOSITY = 0

class Transmitter:
    def __init__(self, location, port = 55555):
        self.seqnum = 0
        self.port = port
        self.loc = location
        
    def send(self, host_list, timestamp, weight, height, shock): 
        msgstring = "%s,SHARKNET1,%d,%d,%s,%d,%.5f,%.3f,2,3,4,5,6" %\
                    (PROTOCOL_VERSION, timestamp % 1e5, self.seqnum, self.loc,weight, height, shock)
        msg = bytes(msgstring,'UTF-8')

        if VERBOSITY > 1:            
            print(msgstring)
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for addr in  host_list:
            sock.sendto(msg, (addr, self.port))
            if VERBOSITY > 0:
                print("sending to host: " + addr)

        self.seqnum = self.seqnum + 1

if __name__ == "__main__":
    import time
    t = Transmitter()
    t.send(['172.16.8.151', '127.0.0.1'], str(time.time()*1000), 0, 0.0, 0.0)
