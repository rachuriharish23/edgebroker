import json
import joblib
import numpy as np
import paho.mqtt.client as mqtt
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0]
print(ip_address)
# Load the trained model from the fil
# MQTT settings
broker = ip_address
port = 1883
output_topic = "zigbee2mqtt/uart2/set/action"

client = mqtt.Client()

# Define callback function for connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed")


def on_publish(client, userdata, mid):
    print("Message published")

client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the broker


clf = joblib.load('decision_tree_model.joblib')


    
def appliation1(message):
                decoded_data = message.decode('utf-8')
                print ("inside application",decoded_data)
# Parse the JSON data
                parsed_data = json.loads(decoded_data)
# Extract the "action" field and parse it as JSON
                action_data = json.loads(parsed_data["action"])
                line_values = action_data["line"]
                stime=action_data["stime"]
                stime=stime[0]                
                print("line_values",line_values)
                idn=line_values[0]
                print("idn",idn)
                line_values=line_values[1:12]
                #print("Message received: ", line_values)
        # Convert the message to a numpy array
                data = np.array(line_values).reshape(1, -1)
        # Make prediction
                prediction = clf.predict(data)
               # print("Prediction: ", prediction)
                #output="{\"output\":["+str(prediction[0]) +"],\"stime\":"+str(stime)+"}"
                output="{\"idno\":"+str(idn)+",\"output\":["+str(prediction[0]) +"],\"stime\":"+str(stime)+"}"
                json_data = json.dumps(output)
                #return(json_data)
                client.connect(broker, port, 60)

# Start the loop
                client.loop_start()

# Publish a message
                client.publish(output_topic, json_data)

# Stop the loop
                client.loop_stop()

# Disconnect from the broker
                client.disconnect()
        # Publish the prediction to the output topic
                #client.publish(output_topic, json_data)
