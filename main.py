from unicurses import *
import socketio
import requests
import time

GETURL = 'http://192.243.100.152:8099/call'
PINGURL = 'http://192.243.100.152:8099/ping'
POSTURL = 'http://192.243.100.152:8099/msg'

socket = socketio.Client()

# this triggers when a message is posted on the server.
# TODO.. this function should update the Message board on the client side UI
@socket.on('message')
def getLastMsg():
    return 0

# just trigger when someone connects to the server... not really needed, used for testing
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
    msgsent = requests.post(POSTURL, { 'id': 777, 'name': 'python', 'message': '#test message from python/curses' })
    if msgsent.status_code == 200:
        addstr('\nMessage posted on server\n', color_pair(2))   
    # ========================================================
    # ===============================================================
    # this is get all messages... also to go into a separate function
    #----------------------------------------------------------------
    data = requests.get(url = GETURL, params = { 'id': 777 })
    allMsgs = data.json()
    for mesg in allMsgs:       
        name = mesg['name']
        actualMsg = mesg['message']
        addstr('--------------------------------------\n')
        addstr(name + '\n', color_pair(3))
        addstr(actualMsg + '\n', color_pair(1))
    # ===============================================================
    addstr('\npress <anykey> to exit')
    getch()
    endwin()
    return 0


if __name__ == '__main__':
    main()
