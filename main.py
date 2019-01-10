from unicurses import *
import socketio
import requests
import time

GETURL = 'http://192.243.100.152:8099/call'
PINGURL = 'http://192.243.100.152:8099/ping'
POSTURL = 'http://192.243.100.152:8099/msg'

socket = socketio.Client()

@socket.on('message')
def getLastMsg():
    return 0

@socket.on('userconnected')
def showUserConnected():    
    addstr('\nuser connected\n', color_pair(3) + A_BOLD)

def main():
    socket.connect('http://192.243.100.152:8099')
    stdscr = initscr()
    start_color()
    time.sleep(5)
    ping = requests.get(url = PINGURL)
    init_pair(1, COLOR_BLUE, COLOR_BLACK)
    init_pair(2, COLOR_RED, COLOR_BLACK)
    init_pair(3, COLOR_GREEN, COLOR_BLACK)
    if ping.status_code == 200:
        addstr('Connected to server\n', color_pair(1) + A_BOLD)
    else:
        addstr('Server Connection failed\n', color_pair(2) + A_BOLD)
    # ========================================================
    # this will need to go to a fucntion call to send messages
    # --------------------------------------------------------
    msgsent = requests.post(POSTURL, { 'id': 999, 'name': 'python', 'message': '#test message from python/curses' })
    if msgsent.status_code == 200:
        addstr('\nMessage posted on server\n', color_pair(2))   
    # ========================================================
    addstr('\npress <anykey> to exit')
    getch()
    endwin()
    return 0


if __name__ == '__main__':
    main()
