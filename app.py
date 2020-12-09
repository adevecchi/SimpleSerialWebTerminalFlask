from flask import Flask, render_template
from flask_socketio import SocketIO

from serial_port import SerialPort

app = Flask(__name__)
socketio = SocketIO(app)
serialport = SerialPort()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('open_port')
def on_open_port(message):
    try:
        serialport.open(message['port'], message['baudrate'])
        socketio.emit('receive_data', 'Serial port is opened\n')
    except:
        socketio.emit('receive_data', 'Could not open port\n')

@socketio.on('close_port')
def on_close_port(message):
    try:
        if serialport.isOpen():
            serialport.close()
            socketio.emit('receive_data', 'Serial port is closed\n')
    except:
        socketio.emit('receive_data', 'Error closing port\n')

@socketio.on('send_message')
def on_send_message(message):
    try:
        if serialport.isOpen():
            serialport.write(message)
    except:
        socketio.emit('receive_data', 'Error sending message\n')

@socketio.on('connect')
def on_connect():
    print('Connected...')

@socketio.on('disconnect')
def on_disconnect():
    print('Disconnected...')

def background_read():
    while True:
        if serialport.isOpen():
            try:
                if serialport.inWaiting() > 0:
                    receivedMessage = serialport.read()
                    socketio.emit('receive_data', receivedMessage)
            except:
                pass

if __name__ == '__main__':
    socketio.start_background_task(target=background_read)
    socketio.run(app)