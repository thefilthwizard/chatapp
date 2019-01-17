from unicurses import *

import requests
import socketio
import signal


GETURL = 'http://192.243.100.152:8099/call'
PINGURL = 'http://192.243.100.152:8099/ping'
POSTURL = 'http://192.243.100.152:8099/msg'


running = True
socket = socketio.Client()
stdscr = initscr()


# this triggers when a message is posted on the server.
@socket.on('message')
def getLastMsg():
        data = requests.get(url = GETURL, params = { 'id': 777 })
        allMsgs = data.json()
        lastMsg = allMsgs[len(allMsgs) - 1]
        return lastMsg


# just trigger when someone connects to the server... not really needed, used for testing
@socket.on('userconnected')
def showUserConnected():
        mvaddstr(1, 1, 'user connected')


def getMessages(id):
        data = requests.get(url = GETURL, params = { 'id': id })
        allMsgs = data.json()
        for mesg in allMsgs:
                name = mesg['name']
                actualMsg = mesg['message']
                addstr('--------------------------------------\n')
                addstr(name + '\n')
                addstr(actualMsg + '\n')


def postMessage():
        msgsent = requests.post(POSTURL, { 'id': 777, 'name': 'python', 'message': '#test message from python/curses' })
        if msgsent.status_code == 200:
                addstr('Message posted on server')


def ping():
        ping = requests.get(url = PINGURL)
        if ping.status_code == 200:
                addstr('Connected to server\n')
        else:
                addstr('Server Connection failed\n')


def create_newwin(height, width, starty, startx):
        local_win = newwin(height, width, starty, startx)
        box(local_win, 0, 0)
        wrefresh(local_win)
        return local_win
        

# method to connect to the socket with some error handling... :-)
def connectServer():
        try:
                socket.connect('http://192.243.100.152:8099')
        except:
                mvaddstr(1, 1, 'Could not connect to server')


def initCurses():
        global stdscr
        cbreak()
        noecho()
        curs_set(0)
        keypad(stdscr, True)
        start_color()
        init_pair(1, COLOR_BLUE, COLOR_BLACK)
        refresh()


def main():
        global running
        global stdscr
        #signal bind listening for sigint
        signal.signal(signal.SIGINT, signal_handler)
        initCurses()
        connectServer()        
        msgWin = create_newwin(7, 78, 16, 1)
        mvaddstr(16, 2, 'Send Message')
        menuWin = create_newwin(3,78, 23, 1)
        mvaddstr(24, 2, '<ESC>exit', COLOR_PAIR(1) + A_BOLD)
        while running:
                KEY = getch()
                if KEY == 27: # ESC key...
                        running = False
        endwin()
        return 0


#signal handler listening for ctrl+c command
def signal_handler(sig, frame):
        global running
        running = False
        print('You pressed Ctrl+C!')


if __name__ == '__main__':
        main()
