# pip install opencv-python-headless pyzbar
import cv2
from pyzbar.pyzbar import decode
import csv
import keyboard
import time

# Create a CSV file or open an existing one in append mode
csv_file = 'qr_codes.csv'

# Initialize an empty list to store the CSV data
csv_data = []

# Open the CSV file for reading
with open(csv_file, mode='r', newline='') as file:
    # Create a CSV reader
    csv_reader = csv.reader(file)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Append the row to the list
        csv_data.append(row[0])

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Set the desired resolution (e.g., 640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
time.sleep(2)

while True:
    ret, frame = cap.read()
    decoded_objects = decode(frame)

    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')

        if qr_data not in csv_data:
            # Append the QR code data to the CSV file
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([qr_data])
            csv_data.append(qr_data)

            print("**************************")
            print(f"{qr_data} Scanned")
            print("**************************")
        else:
            print(f"{qr_data} Already scanned")

    time.sleep(0.2)
    cv2.imwrite("img.png", frame)
    time.sleep(0.2)

    if keyboard.is_pressed('shift+backspace'):
        break

# Release the webcam and close the CSV file
cap.release()
