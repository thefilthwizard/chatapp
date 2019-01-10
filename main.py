from unicurses import *


def main():
    stdscr = initscr()
    start_color()
    init_pair(1, COLOR_BLUE, COLOR_BLACK)
    init_pair(2, COLOR_RED, COLOR_BLUE)
    window = newwin(5,5,5,5)
    waddstr(window, "test", color_pair(2) + A_BOLD)
    wgetch(window)
    addstr("Hello Curses\n", color_pair(1) + A_BOLD)
    addstr("press <anykey> to exit")
    getch()
    endwin()
    return 0


if __name__ == '__main__':
    main()
