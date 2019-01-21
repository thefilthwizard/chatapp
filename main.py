from unicurses import *

import requests
import signal
import socketio

HOST = 'http://192.243.100.152:8099/'
MSGIDSTREAM = 777

GETURL = HOST + 'call'
PINGURL = HOST + 'ping'
POSTURL = HOST + 'msg'


running = True
socket = socketio.Client()
stdscr = initscr()
viewWin = None
menuWin = None
user = None


# this triggers when a message is posted on the server.
@socket.on('message')
def updateLastMesg():
        global viewWin
        lastMsg = getLastMsg(MSGIDSTREAM)
        name = lastMsg['name']
        actualMsg = lastMsg['message']
        waddstr(viewWin, '--------------------------------------\n')
        waddstr(viewWin, name + '\n')
        waddstr(viewWin, actualMsg + '\n')
        wrefresh(viewWin)


def getLastMsg(msgID):
        data = requests.get(url = GETURL, params = { 'id': msgID })
        allMsgs = data.json()
        lastMsg = allMsgs[len(allMsgs) - 1]
        return lastMsg


# just trigger when someone connects to the server... not really needed, used for testing
@socket.on('userconnected')
def showUserConnected():
        mvaddstr(24, 63, 'user connected', COLOR_PAIR(2) + A_BOLD)


# get and display all messages on server for selected chat id
def getMessages(id):
        global viewWin
        wclear(viewWin)
        wrefresh(viewWin)
        data = requests.get(url = GETURL, params = { 'id': id })
        allMsgs = data.json()
        for mesg in allMsgs:
                name = mesg['name']
                actualMsg = mesg['message']
                waddstr(viewWin, '--------------------------------------\n')
                waddstr(viewWin, name + '\n')
                waddstr(viewWin, actualMsg + '\n')
        wrefresh(viewWin)


def postMessage(Message):
        global user
        msgsent = requests.post(POSTURL, { 'id': MSGIDSTREAM, 'name': user, 'message': Message })


def ping():
        ping = requests.get(url = PINGURL)
        if ping.status_code == 200:
                return True
        else:
                return False


def create_newwin(height, width, starty, startx):
        local_win = newwin(height, width, starty, startx)
        box(local_win, 0, 0)
        wrefresh(local_win)
        return local_win


# method to connect to the socket with some error handling... :-)
def connectServer():
        try:
                socket.connect(HOST)
                return True
        except:
                mvaddstr(24, 50, 'Could not connect to server', COLOR_PAIR(3) + A_BOLD)
                return False


def initCurses():
        global stdscr
        cbreak()
        noecho()
        curs_set(0)
        keypad(stdscr, True)
        start_color()
        init_pair(1, COLOR_BLUE, COLOR_BLACK)
        init_pair(2, COLOR_GREEN, COLOR_BLACK)
        init_pair(3, COLOR_RED, COLOR_BLACK)
        init_pair(4, COLOR_CYAN, COLOR_BLACK)
        refresh()


def getUsername():



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
        scrollok(viewWin, True) 
        wrefresh(viewWin)
        if connectServer():
                getMessages(MSGIDSTREAM)
        msgWin = create_newwin(7, 78, 16, 1)
        waddstr(msgWin, 'Send Message')
        wrefresh(msgWin)
        menuWin = create_newwin(3,78, 23, 1)
        mvaddstr(24, 2, '<ESC>Exit', COLOR_PAIR(1) + A_BOLD)
        xpos = 2
        ypos = 17
        msgString = ''
        while running:
                KEY = getch()
                if KEY == 27: # ESC key...
                        # just clear the terminal before exit
                        clear()
                        refresh()
                        endwin()
                        running = False
                elif KEY == 10: # enter key, submit message and clears input box
                        wclear(msgWin)
                        box(msgWin, 0, 0)
                        waddstr(msgWin, 'Send Message')
                        wrefresh(msgWin)                       
                        xpos = 2
                        ypos = 17
                        if ping(): 
                                postMessage(msgString)
                        msgString = ''                        
                elif KEY == 8: # backspace                
                        if xpos > 2:
                                xpos = xpos - 1                                
                                move(ypos, xpos)
                                delch()
                                if len(msgString) > 0:
                                        msgString[:-1]
                        if xpos == 2 and ypos > 17:
                                xpos = 77
                                ypos = ypos - 1
                                move(ypos, xpos)
                                delch()
                                if len(msgString) > 0:
                                        msgString[:-1]
                        refresh() 
                else: #takes text input and echos it to the msgWindow.. still needs alot of work
                        mvaddch(ypos, xpos, KEY, COLOR_PAIR(4))
                        msgString = msgString + chr(KEY)
                        xpos = xpos + 1
                        if xpos >= 77:
                                xpos = 2
                                ypos = ypos + 1
        return 0


#signal handler listening for ctrl+c command
def signal_handler(sig, frame):
        global running
        running = False
        print('You pressed Ctrl+C!')


if __name__ == '__main__':
        main()
