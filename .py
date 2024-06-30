import json
import nump
def lambda_handler(event, context):
    # Print the entire event object for debugging
    print("Event: ", json.dumps(event))
    bucket_name = 'aws-lambda-source-bucket-1994'
    model_key = 'cardio_train.joblib'
    model_path = '/tmp/cardio_train.joblib'

    # Download the model file from S3 to /tmp directory in Lambda
    s3.download_file(bucket_name, model_key, model_path)
    # Load the model
    clf = joblib.load(model_path)

    # Example input data from IoT Core (event)
   
    try:
        payload = event
        #print(payload)
        #print(payload['line'])
        corrected_action = payload["action"].replace('\\"', '"')
        print(corrected_action)
        print(type(corrected_action))
        json_data = json.loads(corrected_action)
        input_data=json_data['line']
        idn=input_data[0]
        input_data=input_data[1:]
        print("idn:",idn)
        print("hello",input_data)

    # Preprocess input_data if necessary (convert to numpy array, reshape, etc.)
        input_data = np.array(input_data).reshape(1, -1)  # Example reshaping if needed
        print(input_data)

    # Make prediction
        prediction = clf.predict(input_data)
    # Check if 'temperature' is in the payload
        response = client1.publish(
            topic='esp32/pub',
            qos=0,
            payload=json.dumps({"id":idn,"prediction":prediction.tolist(),"stime":json_data['stime']})
        )
        print(response)
        return {
                 'statusCode': 200,
                 'body': {'prediction': prediction.tolist() }
        }
        
    except Exception as e:
        print(f"Error processing the message: {str(e)}")

    return {
        'statusCode': 200,
        'body': {'prediction': prediction.tolist() }
    }




