from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained model
with open('models/crop_recommendation_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Check for missing input data
    if not all(key in data for key in ['temperature', 'humidity', 'ph', 'rainfall']):
        return jsonify({'error': 'Missing input data'}), 400

    try:
        # Attempt to convert inputs to float and validate ranges
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])

        if not (-30 <= temperature <= 50):
            return jsonify({'error': 'Temperature out of range (-30 to 50 degrees).'}), 400
        if not (0 <= humidity <= 100):
            return jsonify({'error': 'Humidity out of range (0% to 100%).'}), 400
        if not (0 <= ph <= 14):
            return jsonify({'error': 'pH level out of range (0 to 14).'}), 400
        if not (0 <= rainfall <= 1000):
            return jsonify({'error': 'Rainfall out of range (0 to 1000 mm).'}), 400

        # Log the input values for debugging
        print(f"Temperature: {temperature}, Humidity: {humidity}, pH: {ph}, Rainfall: {rainfall}")

        # Create a DataFrame with the validated input data
        input_data = pd.DataFrame([[temperature, humidity, ph, rainfall]],
                                  columns=['temperature', 'humidity', 'ph', 'rainfall'])

        # Make prediction
        prediction = model.predict(input_data)
        predicted_crop = prediction[0]

    except ValueError as ve:
        print(f"ValueError: {ve}")  # Log the ValueError for debugging
        return jsonify({'error': 'Invalid input type.'}), 400
    except Exception as e:
        print(f"Exception: {e}")  # Log any other exceptions for debugging
        return jsonify({'error': f'Error making prediction: {str(e)}'}), 500

    return jsonify({'crop': predicted_crop})

