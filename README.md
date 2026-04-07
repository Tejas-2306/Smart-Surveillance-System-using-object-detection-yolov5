# Smart Surveillance System using YOLOv5

## Overview

This project implements a smart surveillance system that detects weapons such as guns and knives using the YOLOv5 object detection model. Upon detecting a weapon, the system triggers an alarm and sends real-time alerts via WhatsApp using the Twilio API.

The system is designed to enhance security by enabling automated threat detection and instant notification.

## Features

* Real-time weapon detection (guns, knives, etc.)
* Alarm triggering on detection
* WhatsApp alert system using Twilio API
* Custom-trained YOLOv5 model
* Web interface for monitoring

## Tech Stack

* Backend: Python
* Model: YOLOv5 (custom trained)
* Frontend: HTML, CSS, JavaScript
* API: Twilio (WhatsApp messaging)
* Libraries: OpenCV, PyTorch

## Model Details

* Based on YOLOv5 architecture
* Trained on a custom dataset for weapon detection
* Detects multiple weapon classes (gun, knife, etc.)
* Outputs bounding boxes with confidence scores

## Note on YOLOv5 Repository

The full YOLOv5 source code is not included in this repository due to size constraints. This project uses the official YOLOv5 implementation.

To set up YOLOv5:

```bash id="v2p8mz"
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

## Installation

```bash id="tq48sl"
git clone https://github.com/your-username/smart-surveillance-yolov5.git
cd smart-surveillance-yolov5
pip install -r requirements.txt
```

## Alert System Workflow

1. Model detects weapon in video frame
2. Bounding box and confidence score generated
3. Alarm is triggered
4. Alert message sent via Twilio WhatsApp API

## Results

* Successfully detects weapons in real-time video streams
* Generates alerts with minimal delay
* Trained model achieves reliable detection accuracy

## Future Improvements

* Improve detection accuracy with larger dataset
* Deploy on edge devices (CCTV systems)
* Add face recognition integration
* Reduce false positives

## Conclusion

This project demonstrates how YOLOv5 can be integrated with real-time alert systems to build an intelligent surveillance solution for security applications.
