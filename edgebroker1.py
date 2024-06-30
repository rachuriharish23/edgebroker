import numpy as np
import threading
import paho.mqtt.client as mqtt
import json
import ast
import socket
import application1
import application2


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0]
print(ip_address)
# Load the trained model from the file


# MQTT settings
broker = ip_address
port = 1883
input_topic = "zigbee2mqtt/uart1"
input_topic1 = "zigbee2mqtt/uart3"

output_topic = "zigbee2mqtt/uart2/set/action"

    
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to the input topic
    client.subscribe(input_topic)
    client.subscribe(input_topic1)


def on_message(client, userdata, msg):
    try:
        print(msg.topic)
        if msg.topic==input_topic :# Decode the messag
                message = msg.payload
                #print(message)
                app1_thread = threading.Thread(target=application1.appliation1, args=(message,))
                app1_thread.start()
                app1_thread.join()
        elif msg.topic==input_topic1 :# Decode the messag
                message = msg.payload
                print(message)
                app2_thread = threading.Thread(target=application2.appliation2, args=(message,))
                app2_thread.start()
                app2_thread.join()
                
        else:
                print("iam in ")
                client.publish(output_topic, "hello")
    except Exception as e:
        print("Error processing message:", e)
def mmqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

# Connect to the broker
    client.connect(broker, port, 60)
    
# Blocking call to process network traffic, dispatch callbacks and handle reconnecting
    client.loop_forever()


# Create an MQTT client and attach the on_connect and on_message callbacks
def main():
    mqtt_thread = threading.Thread(target=mmqtt())
    mqtt_thread.start()
    mqtt_thread.join()

if __name__ == "__main__":
    main()


