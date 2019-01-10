from unicurses import *
import socketio
import requests

GETURL = 'http://192.243.100.152:8099/call'
PINGURL = 'http://192.243.100.152:8099/ping'

socket = socketio.Client()

@socket.on('message')
def getLastMsg():
    return 0

@socket.on('userconnected')
def showUserConnected():
    addstr('\nuser connected\n')

def main():
    socket.connect('http://192.243.100.152:8099')
    stdscr = initscr()
    start_color()
    ping = requests.get(url = PINGURL)
    init_pair(1, COLOR_BLUE, COLOR_BLACK)
    init_pair(2, COLOR_RED, COLOR_BLUE)
    addstr(ping, color_pair(1) + A_BOLD)
    addstr('\npress <anykey> to exit')
    getch()
    endwin()
    return 0


if __name__ == '__main__':
    main()
