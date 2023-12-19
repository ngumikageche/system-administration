from flask import Flask, render_template
from flask_socketio import SocketIO
import subprocess
import socket
import threading
import time
from branches_config import branches

app = Flask(__name__)
socketio = SocketIO(app)

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

def colorize_ping(ping_time):
    if ping_time is None:
        return 'Timeout'
    elif ping_time < 2:
        return '{:.2f} '.format(ping_time)
    elif ping_time > 10:
        return '{:.2f}'.format(ping_time)
    else:
        return '{:.2f}'.format(ping_time)

def update_ping_data():
    while True:
        ping_data = []

        for branch, ip in branches.items():
            ping_time = ping(ip)
            ping_colored = colorize_ping(ping_time)
            ping_data.append({'branch': branch, 'ip': ip, 'ping_colored': ping_colored})

        socketio.emit('update_ping_data', {'local_ip': get_local_ip(), 'ping_data': ping_data})
        time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.emit('update_ping_data', {'local_ip': get_local_ip(), 'ping_data': []})

if __name__ == "__main__":
    threading.Thread(target=update_ping_data).start()
    socketio.run(app, port="3000", debug=True)
