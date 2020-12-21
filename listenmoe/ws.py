import websocket
import threading
import json
import time

class Heartbeat(threading.Thread):
    def __init__(self, threadID, name, interval, ws):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.interval = interval
        self.ws = ws
        self.running = True

    def run(self):
        print(f"Starting {self.name} with interval of {self.interval}s")
        while self.running:
            self.ws.send(json.dumps({"op":9}))
            time.sleep(self.interval)
    
    def stop(self):
        self.running = False

socket = None
heartbeat = None
artist = ""
song = ""
ws_thread = None
def start_socket_thread():
    global ws_thread
    ws_thread = threading.Thread(target=start_socket)
    ws_thread.start()

    
def start_socket():
    global socket
    socket = websocket.WebSocketApp('wss://listen.moe/gateway_v2', on_message=on_message, on_error=on_error, on_close=on_close)
    socket.on_open = on_open
    socket.run_forever()

def on_open(ws):
    print("Socket to listen.moe opened!")

def on_message(ws, message: None):
    global heartbeat, song, artist
    try:
        response = json.loads(message)
    except:
        print(f"Couldn't parse `{message}` as JSON.")
        return 
    
    if response['op'] == 0:
        ws.send(json.dumps({"op":9}))
        heartbeat = Heartbeat(1, "HeartbeatThread", response['d']['heartbeat'] / 1000, socket)
        heartbeat.start()

    elif response['op'] == 1:
        # print(response)
        # source = ""
        song = response['d']['song']['title']
        artist = [x['name'] for x in response['d']['song']['artists']]
        # if len(response['d']['song']['sources']) >=1:
        #     source = f"from {response['d']['song']['sources'][0]['nameRomaji'] if response['d']['song']['sources'][0]['nameRomaji'] is not None else response['d']['song']['sources'][0]['name']}"
        # print(f"Now playing: {response['d']['song']['title']} by {response['d']['song']['artists'][0]['name']} {source}")

def on_error(ws, error):
    print(error)
    ws.close()
    heartbeat.stop()

def on_close(ws):
    start_socket()

