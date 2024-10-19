from flask import Flask, request, jsonify
from roboflow import Roboflow
from playsound import playsound
from flask_cors import CORS
import tempfile
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Roboflow
rf = Roboflow(api_key="ZR8cnHmRyvRYHKWKNLBL")
project = rf.workspace().project("object-detection-vyqkc")
model = project.version("1").model

@app.route('/analyze-video', methods=['POST'])
def analyze_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file uploaded"}), 400

    video = request.files['video']

    # Use a temporary file to avoid saving it permanently
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        video.save(temp_video.name)  # Save the uploaded video to a temporary file
        
        # Make a prediction on the video using Roboflow
        job_id, signed_url, expire_time = model.predict_video(
            temp_video.name, fps=5, prediction_type="batch-video"
        )

        # Poll until results are available
        results = model.poll_until_video_results(job_id)

    # Remove the temporary file after processing
    os.remove(temp_video.name)

    # Check if any prediction is for a human
    human_detected = False
    for frame in results['object-detection-vyqkc']:
        for prediction in frame['predictions']:
            if prediction['class'] == '0':  # Assuming '0' represents a human
                human_detected = True
                break
        if human_detected:
            break

    # Output whether a human was detected
    if human_detected:
        print("Human detected: Yes")
        playsound('D:/alarm/alarm_sound.mp3')  # Play alarm sound
        return jsonify({"result": "Human detected! Alarm triggered!"})
    else:
        print("Human detected: No")
        return jsonify({"result": "No human detected."})

if __name__ == '__main__':
    app.run(debug=True)
