from queue import Queue
from LazyChat.corenet import CoreNet
import argparse

from LazyChat.tui import LazyChat

def main():
    parser = argparse.ArgumentParser(description='Example of argparse')

    parser.add_argument('-ip', '--ip_addr', default="localhost",
                        help='The IP address to use for the connection. Defaults to 127.0.0.1 if '
                             'not specified.')
    parser.add_argument('-p', '--port', default="8080",
                        help='The port to use for the connection. Defaults to 8080 if not specified.')
    args = parser.parse_args()

    IP_ADDR = args.ip_addr
    PORT = int(args.port)
    print("IP_ADDR", IP_ADDR)
    print("PORT", PORT)

    queue = Queue()
    core = CoreNet(queue, IP_ADDR, PORT)
    LazyChat.runAll(core)

if __name__ == '__main__':
    main()
