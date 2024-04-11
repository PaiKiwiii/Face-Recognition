from flask import Flask, render_template, redirect, url_for, request, jsonify
import subprocess
import streamlit as st
import cv2
import numpy as np

app = Flask(__name__, static_folder='static')
@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/admin.html')
def index():
    return render_template('admin.html')


# Route for face recognition
@app.route('/face_recognition', methods=['POST'])
def face_recognition():
    # Get image data from the request
    image_data = request.files['image'].read()
    
    # Convert the image data into a numpy array
    nparr = np.fromstring(image_data, np.uint8)
    
    # Decode the numpy array to get the image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Perform face recognition here using OpenCV
    
    # Replace this with actual face recognition results
    result = {'result': 'Face recognized successfully'}
    
    # Return the result as JSON
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
    
    # Your Streamlit application code here

if __name__ == "__main__":
    # Run the Streamlit application on port 8501
    st.set_option('server.port', 8501)
    st.run()
    

    
