#!/usr/bin/python3

import xfd_server as xfd

def run_server():
    server = xfd.XfdServer()

    server.run()


if __name__ == '__main__':
    run_server()