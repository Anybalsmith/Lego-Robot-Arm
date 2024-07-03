import cv2
import random

def capture_and_process_frame():
    # Initialize the webcam
    cap = cv2.VideoCapture(1)  # Change to 0 for the default webcam
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to capture image from webcam.")
            break
        
        # Get dimensions of the frame
        height, width, _ = frame.shape
        
        # Print the width and height of the image
        print(f"Width: {width}, Height: {height}")
        
        # Define the possible positions as numbers from 0 to 5
        positions = list(range(6))
        
        # Randomly select one of the positions
        selected_position = random.choice(positions)
        
        # Display the resulting frame
        cv2.imshow('Webcam Feed', frame)
        
        # Print the selected position
        print(f"Selected position: {selected_position}")
        
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return selected_position

# Capture and process the webcam frame
position = capture_and_process_frame()
if position is not None:
    print(f"Final selected position: {position}")
