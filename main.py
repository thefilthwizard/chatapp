import curses
from curses import *

import requests
import signal
import socketio

HOST = 'http://localhost:8099/'
MSGIDSTREAM = 777

GETURL = HOST + 'call'
PINGURL = HOST + 'ping'
POSTURL = HOST + 'msg'

menuWin = None
running = True
socket = socketio.Client()
stdscr = curses.initscr()
user = None
viewWin = None

# this triggers when a message is posted on the server.
@socket.on('message')
def updateLastMesg():
    global viewWin
    lastMsg = getLastMsg(MSGIDSTREAM)
    name = lastMsg['name']
    actualMsg = lastMsg['message']
    viewWin.addstr( '--------------------------------------\n')
    viewWin.addstr(name + '\n')
    viewWin.addstr(actualMsg + '\n')
    viewWin.refresh()

def getLastMsg(msgID):
    data = requests.get(url = GETURL, params = { 'id': msgID })
    allMsgs = data.json()
    lastMsg = allMsgs[len(allMsgs) - 1]
    return lastMsg

# just trigger when someone connects to the server... not really needed, used for testing
@socket.on('userconnected')
def showUserConnected():
    global menuWin
    menuWin.addstr(1, 63, 'user connected', curses.color_pair(2) + curses.A_BOLD)

# get and display all messages on server for selected chat id
def getMessages(id):
    global viewWin
    viewWin.clear()
    viewWin.refresh()
    data = requests.get(url = GETURL, params = { 'id': id })
    allMsgs = data.json()
    for mesg in allMsgs:
        name = mesg['name']
        actualMsg = mesg['message']
        viewWin.addstr('--------------------------------------\n')
        viewWin.addstr(name + '\n')
        viewWin.addstr(actualMsg + '\n')
    viewWin.refresh()

def postMessage(Message):
    global user
    msgsent = requests.post(POSTURL, { 'id': MSGIDSTREAM, 'name': user, 'message': Message })

def ping():
    try:
        ping = requests.get(url = PINGURL)
        if ping.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def create_newwin(height, width, starty, startx):
    local_win = curses.newwin(height, width, starty, startx)
    local_win.border()
    local_win.refresh()
    return local_win

# method to connect to the socket with some error handling... :-)
def connectServer():
    try:
        socket.connect(HOST)
        return True
    except:
        return False

def initCurses():
    global stdscr
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad( True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    stdscr.refresh()

def destroyCurses():
    global stdscr
    global viewWin
    global menuWin
    socket.disconnect()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def getUsername():
    tempUserName = ''
    userWin = create_newwin(3, 30, 5, 5)
    curses.echo()
    userWin.addstr(1, 2, 'USER NAME: ')
    getName = True
    while getName:
        char = userWin.getch()
        if char == 10:
            getName = False
        else:
            tempUserName = tempUserName + chr(char)
    curses.noecho()
    return tempUserName

def main():
    global running
    global stdscr
    global viewWin
    global menuWin
    global user
    #signal bind listening for sigint
    signal.signal(signal.SIGINT, signal_handler)
    initCurses()
    user = getUsername()
    viewWin = create_newwin(14, 78 , 1, 1)
    viewWin.scrollok( True)
    viewWin.refresh()
    msgWin = create_newwin(7, 78, 16, 1)
    msgWin.addstr(0, 2, 'Send Message')
    msgWin.refresh()
    menuWin = create_newwin(3,78, 23, 1)
    menuWin.addstr(1, 2, '<ESC>Exit', curses.color_pair(1) + curses.A_BOLD)
    menuWin.refresh()
    if connectServer():
            getMessages(MSGIDSTREAM)
    xpos = 2
    ypos = 17
    msgString = ''
    while running:
        KEY = stdscr.getch()
        if KEY == 27: # ESC key...
            # just clear the terminal before exit
            destroyCurses()
            running = False
        elif KEY == 10: # enter key, submit message and clears input box
            msgWin.clear()
            msgWin.border()
            msgWin.addstr(0, 2, 'Send Message')
            msgWin.refresh()
            xpos = 2
            ypos = 17
            if ping():
                postMessage(msgString)
            msgString = ''
        elif KEY == 8: # backspace
            if xpos > 2:
                xpos = xpos - 1
                stdscr.move(ypos, xpos)
                stdscr.delch()
                if len(msgString) > 0:
                    msgString = msgString[:-1]
            if xpos == 2 and ypos > 17:
                xpos = 77
                ypos = ypos - 1
                stdscr.move(ypos, xpos)
                stdscr.delch()
                if len(msgString) > 0:
                    msgString = msgString[:-1]
            stdscr.refresh()
        else: #takes text input and echos it to the msgWindow.. still needs alot of work
            stdscr.addch(ypos, xpos, KEY, curses.color_pair(4))
            msgString = msgString + chr(KEY)
            xpos = xpos + 1
            if xpos >= 77:
                xpos = 2
                ypos = ypos + 1
    return 0

#signal handler listening for ctrl+c command
def signal_handler(sig, frame):
    global running
    destroyCurses()
    running = False
    print('You pressed Ctrl+C!')

if __name__ == '__main__':
    main()
