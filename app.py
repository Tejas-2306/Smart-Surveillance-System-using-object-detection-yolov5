import os
from flask import Flask, render_template, request, jsonify, Response, send_from_directory, stream_with_context
import cv2
import torch
import pygame
import threading
from twilio.rest import Client

app = Flask(__name__)

# Define the base directory as the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths relative to the base directory
model_path = os.path.join(BASE_DIR, 'yolov5/runs/train/yolov5s_new_final/weights/best.pt')
alarm_sound_path = os.path.join(BASE_DIR, 'alarm.mp3')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Load the YOLOv5 model using the relative model path
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

# Initialize pygame and load the alarm sound
pygame.mixer.init()
pygame.mixer.music.load(alarm_sound_path)

# Class names from the YOLOv5 model (adjust based on your custom model)
class_names = model.names
ALARM_CLASSES_NAMES = ["car", "stop sign", "Coin", "Airplane", "Handgun", "Weapon","Smartphone","knife","Gun"]

# Twilio setup
account_sid = ""
auth_token = ""
twilio_client = Client(account_sid, auth_token)

def play_alarm_sound():
    """ Play the alarm sound in a loop """
    pygame.mixer.music.play(-1)

def stop_alarm_sound():
    """ Stop the alarm sound and reset the mixer state """
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.mixer.init()
    pygame.mixer.music.load(alarm_sound_path)

def send_whatsapp_message():
    """ Send a WhatsApp message via Twilio when the alarm is triggered """
    message = twilio_client.messages.create(
        body="Threat has been Detected.. Stay Safe..",
        from_='whatsapp:'',  # Your Twilio WhatsApp number
        to='whatsapp:''  # Recipient's WhatsApp number
    )
    print(f"Message sent with SID: {message.sid}")

def detect_and_play_alarm(img):
    """ Detect objects and play alarm sound if specific objects are detected """
    results = model(img)
    detected_classes = results.xywh[0][:, -1].tolist()
    detected_class_names = [class_names[int(class_id)] for class_id in detected_classes]

    if any(class_name in ALARM_CLASSES_NAMES for class_name in detected_class_names):
        if not pygame.mixer.music.get_busy():
            play_alarm_sound()
            send_whatsapp_message()  # Send the WhatsApp message when alarm is triggered
    else:
        stop_alarm_sound()

def gen_frames():
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            detect_and_play_alarm(frame)
            results = model(frame)
            frame_with_boxes = results.render()[0]
            ret, buffer = cv2.imencode('.jpg', frame_with_boxes)
            frame = buffer.tobytes()
            
            # Yield the frame to the client
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        stop_alarm_sound()
    finally:
        cap.release()
        stop_alarm_sound()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webcam')
def webcam_page():
    return render_template('webcam.html')

@app.route('/webcam_stream')
def webcam_stream():
    return Response(stream_with_context(gen_frames()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload-photo')
def upload_photo():
    return render_template('upload_photo.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Read the uploaded image
    img = cv2.imread(file_path)
    results = model(img)

    # Render the results (with bounding boxes)
    img_with_boxes = results.render()[0]

    # Save the output image
    output_filename = f"result_{filename}"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    cv2.imwrite(output_path, img_with_boxes)

    # Detect classes in the image
    detected_classes = [result['name'] for result in results.pandas().xyxy[0].to_dict(orient="records")]

    # Check if any alarm class is detected
    alarm_triggered = False
    if any(class_name in ALARM_CLASSES_NAMES for class_name in detected_classes):
        alarm_triggered = True
        play_alarm_sound()
        stop_alarm_sound()
        send_whatsapp_message()

    return jsonify({
        'result_image': output_filename,
        'alarm_triggered': alarm_triggered,
        'detected_objects': detected_classes
    })

@app.route('/upload-video')
def upload_video():
    return render_template('upload_video.html')

@app.route('/upload_video', methods=['POST'])
def upload_video_v2():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Open the uploaded video
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        return jsonify({'error': 'Failed to open video file'})

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = max(1, int(cap.get(cv2.CAP_PROP_FPS)))

    output_filename = f"processed_{filename}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # Use an alternative codec if 'mp4v' fails
    try:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Common codec
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    except Exception as e:
        return jsonify({'error': f'VideoWriter initialization failed: {str(e)}'})

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detect_and_play_alarm(frame)

        # Run object detection and render results
        results = model(frame)
        img_with_boxes = results.render()[0]
        out.write(img_with_boxes)  # Write the processed frame to the output video
        cv2.imshow('Object Detection (Video)', img_with_boxes)

        # Stop on 'q' key or if the video window is closed
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Object Detection (Video)", cv2.WND_PROP_VISIBLE) < 1:
            stop_alarm_sound()
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWi

    return jsonify({'message': 'Video processed', 'output_video': output_filename})

@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/output/<filename>')
def get_output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

if __name__ == "__main__":
    app.run(debug=False)


