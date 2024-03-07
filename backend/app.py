from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import uuid
import os 

app = Flask(__name__)
CORS(app)

@app.route('/exercises', methods=['GET'])
# HERE CODE CALLED FROM THE FRONTEND FILE ExperimentViewUno.vue
def get_exercises():
    user_id = str(uuid.uuid4())
    
    exercise_links_list = ["https://pytamaro.si.usi.ch/activities/luce/color-flower/de/v2", 
                           "https://pytamaro.si.usi.ch/activities/luce/four-petal-flower/en/v3", 
                           "https://pytamaro.si.usi.ch/activities/luce/swiss-flag/en/v2"
                           ]
    
    response_data = {
        'user_id': user_id,
        'exercises': exercise_links_list
    }
    print("response_data: ", response_data)
    return jsonify(response_data)
    

@app.route('/upload-file', methods=['POST'])
def upload_file():
    try:
        # Get the uploaded file from the request
        file = request.files['file']
        
        # Get the user ID from the request
        user_id = request.form['userId']

        if not file or not user_id:
            return jsonify({"error": "Invalid request. Missing file or user ID."})

        # Create a unique filename for the uploaded file using the user ID
        filename = f"{user_id}_{file.filename}"

        # Save the file to the uploads directory
        file.save(os.path.join("uploads", filename))

        return jsonify({"message": "File uploaded successfully"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"})
    
ex_number = 1

answer_data_list = []

@app.route('/submit-and-export', methods=['POST', 'GET'])
def submit_and_export():
    global ex_number  # Use the global exp_number

    if request.method == 'POST':

        # Handle POST request to submit answer data
        answer_data = request.get_json()

        # Append answer data to the in-memory list
        answer_data_list.append(answer_data)

        return jsonify({"message": "Answer data submitted successfully"})

    elif request.method == 'GET':
        # Handle GET request to export answer data to a CSV file

        # Define the CSV file path
        csv_file_path = 'answer_data.csv'

        # Define CSV header
        csv_header = [
            'User_ID','Experiment', 'Age', 'Gender', 'Programming Experience',
            'Programming Language Familiarity', 'Lines Of Code', 'Pytamaro Platform', 'TimeTaken'
        ]

        # Write answer data to CSV file
        with open(csv_file_path, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_header)

            # If the file is empty, write the header
            if csv_file.tell() == 0:
                writer.writeheader()

            # Write experiment information and answer data to CSV file
            for idx, answer_data in enumerate(answer_data_list, start=1):
                
                writer.writerow({
                    'User_ID': answer_data.get('user_id', ''),
                    'Experiment': answer_data.get('ex', ''),
                    'Age': answer_data.get('age', ''),
                    'Gender': answer_data.get('gender', ''),
                    'Programming Experience': answer_data.get('programming_experience', ''),
                    'Programming Language Familiarity': answer_data.get('programming_language_familiarity', ''),
                    'Lines Of Code': answer_data.get('lines_of_code', ''),
                    'Pytamaro Platform': answer_data.get('pytamaro', ''),
                    'TimeTaken': answer_data.get('timeTaken', ''),
                })
            ex_number += 1  # Increment exp_number 
   
    # Clear the answer_data_list after exporting to CSV
    answer_data_list.clear()
   
    return jsonify({"message": f"Answer data exported to {csv_file_path} successfully"})

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        feedback_data = request.get_json()

        # Get the user ID from the request
        user_id = feedback_data.get('user_id')

        if not user_id:
            return jsonify({"error": "Invalid request. Missing user ID."})

        # Get feedback from the request
        feedback_text = feedback_data.get('feedback', '')

        # Save feedback data to a CSV file
        csv_file_path = 'feedback_data.csv'
        csv_header = ['User_ID', 'Feedback']

        with open(csv_file_path, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_header)

            # If the file is empty, write the header
            if csv_file.tell() == 0:
                writer.writeheader()

            # Write feedback data to CSV file
            writer.writerow({
                'User_ID': user_id,
                'Feedback': feedback_text,
            })

        return jsonify({"message": "Feedback submitted successfully"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"})

if __name__ == '__main__':
    app.run(debug=True)