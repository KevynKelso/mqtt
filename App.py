import os
import paho.mqtt.client as mqtt

from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__)

topic = 'foo'
topic2 = 'bar'
port = 5000

data = {'title': 'n/a'}

load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)
    client.publish(topic2, "STARTING SERVER")
    client.publish(topic2, "CONNECTED")


def on_message(client, userdata, msg):
    data['title'] = msg.payload.decode()
    client.publish(topic2, "RECIEVED")


@app.route('/')
def index():
    return render_template('index.html', data=data, title=data['title'])

def main():
    client = mqtt.Client()
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT)
    client.loop_start()

    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
