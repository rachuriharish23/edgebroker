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
output_topic = "zigbee2mqtt/uart4/set/action"

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

# Load the trained model and the scaler from Joblib files
svm = joblib.load('svm_model.joblib')
scaler = joblib.load('scaler.joblib')

def appliation2(message):
                decoded_data = message.decode('utf-8')
                print ("inside application",decoded_data)
                
# Parse the JSON data
                #parsed_data = json.loads(decoded_data)
# Extract the "action" field and parse it as JSON
                #action_data = json.loads(parsed_data["action"])
                #line_values = action_data["line"]
                #stime=action_data["stime"]
                #stime=stime[0]                
                #print("stime",stime)
                #line_values=line_values[0:11]
                #print("Message received: ", line_values)
                # Convert the message to a numpy array
                data = np.array(line_values).reshape(1, -1)
                # New data to predict
                new_data = [0.062357219,0.0278,0.019132322,0.138319637,4.80078991,25.83713617]  # Example input 2]
                # Convert new data to a NumPy array
                new_data = np.array(new_data, dtype=float)
                # Standardize the new data using the previously fitted scaler
                new_data = scaler.transform(new_data)
                # Make predictions using the loaded model   
                predictions = svm.predict(new_data)
                # Print the predictions
                print(f'Predictions: {predictions}')
                # Make prediction
                # print("Prediction: ", prediction)
                output="{\"output\":["+str(prediction[0]) +"],\"stime\":"+str(stime)+"}"
                json_data = json.dumps(output)
                #return(json_data)
                client.connect(broker, port, 60)

# Start the loop
                client.loop_start()


