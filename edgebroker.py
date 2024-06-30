import numpy as np
import joblib
import paho.mqtt.client as mqtt
import json
import ast
import socket   
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0]
print(ip_address)
# Load the trained model from the file
clf = joblib.load('decision_tree_model.joblib')

# MQTT settings
broker = ip_address
port = 1883
input_topic = "zigbee2mqtt/uart1"
output_topic = "zigbee2mqtt/uart2/set/action"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to the input topic
    client.subscribe(input_topic)

def on_message(client, userdata, msg):
    try:
        if msg.topic==input_topic :# Decode the messag
                message = msg.payload
                #print(message)
                decoded_data = message.decode('utf-8')
                print (decoded_data)
# Parse the JSON data
                parsed_data = json.loads(decoded_data)
# Extract the "action" field and parse it as JSON
                action_data = json.loads(parsed_data["action"])
                line_values = action_data["line"]
                stime=action_data["stime"]
                stime=stime[0]                
                print("stime",stime)
                line_values=line_values[0:11]
                print("Message received: ", line_values)
        # Convert the message to a numpy array
                data = np.array(line_values).reshape(1, -1)
        # Make prediction
                prediction = clf.predict(data)
                print("Prediction: ", prediction)
                output="{\"output\":["+str(prediction[0]) +"] ,\"stime\":[" + str(stime)+"]}"
                
                json_data = json.dumps(output, indent=4)
                print(json_data)
                
        # Publish the prediction to the output topic
                client.publish(output_topic, json_data)
        else:
                print("iam in ")
                client.publish(output_topic, "hello")
    except Exception as e:
        print("Error processing message:", e)

# Create an MQTT client and attach the on_connect and on_message callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker, port, 60)
# Blocking call to process network traffic, dispatch callbacks and handle reconnecting
client.loop_forever()
