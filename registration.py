#!/usr/bin/env python3
__author__= 'Donour Sizemore'

import socketserver

hosts = []
channel_offsets = None
channel_gains = None

class SharksRegistrationHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global hosts
        global channel_offsets
        global channel_gains
        data = self.request[0]
        data = data.decode("UTF-8")
        data = data.split(",")
        if data[0] == "HELO":
            hosts.append(self.client_address[0])
        elif data[0] == "ZERO":
            channel_offsets  = data[2:] 
        elif data[0] == "CAL":
            channel_gains  = data[2:] 


class reg_server:

    def __init__(self, host, port):
        self.sock = socketserver.UDPServer( (host, port), SharksRegistrationHandler)
        self.sock.timeout = 0.0

    def get_hosts(self):
        global hosts
        hosts = []
        self.sock.handle_request()

        return hosts

    def get_calibration(self):
        global channel_offsets
        global channel_gains
        ng = channel_gains
        no = channel_offsets
        channel_gains = None
        channel_offsets = None
        return (ng, no)
    
if __name__ == "__main__":
    import time, sys
    PORT = 55556
    host = '192.168.0.1'

    s = reg_server(host, PORT)

    while True:
        
        time.sleep(0.05)
        print(s.get_hosts())
        sys.stdout.write('.')
        sys.stdout.flush()
