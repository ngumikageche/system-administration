import subprocess
import socket
import time
import curses
from branches_config import branches

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.0.0.0', 1))
        local_ip = s.getsockname()[0]
    except socket.error:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def ping(host):
    try:
        output = subprocess.check_output(['ping', '-c', '1', host], universal_newlines=True)
        lines = output.split('\n')
        for line in lines:
            if 'icmp_seq' in line and 'time=' in line:
                time_str = line.split('time=')[1].split(' ')[0]
                return float(time_str)
    except subprocess.CalledProcessError:
        return None
def colorize_ping(stdscr, ping_time):
    if ping_time is None:
        stdscr.addstr("Timeout", curses.color_pair(1))
    elif ping_time < 2:
        stdscr.addstr("{:.2f} ms".format(ping_time), curses.color_pair(2))
    elif ping_time > 10:
        stdscr.addstr("{:.2f} ms".format(ping_time), curses.color_pair(1))
    else:
        stdscr.addstr("{:.2f} ms".format(ping_time))

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # Red color
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Green color

    local_ip = get_local_ip()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"{'Branch': <15}{'IP Address': <15}{'Ping Time': <20}")
        stdscr.addstr(1, 0, "-" * 50)

        row = 2
        for branch, ip in branches.items():
            ping_time = ping(ip)
            stdscr.addstr(row, 0, f"{branch: <15}{ip: <15}")
            colorize_ping(stdscr, ping_time)
            row += 1

        stdscr.addstr(row + 1, 0, f"\nLocal IP: {local_ip}")
        stdscr.addstr(row + 2, 0, "-" * 50)

        stdscr.refresh()
        time.sleep(5)

if __name__ == "__main__":
    curses.wrapper(main)
