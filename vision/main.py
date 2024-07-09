import cv2
import numpy as np
import datetime
import os

# Initialize the webcam
print("Initializing the webcam...")
cap = cv2.VideoCapture(1)

def take_picture():
    if not cap.isOpened():
        print("Error: Could not open video device.")
    else:
        # Capture frame-by-frame
        print("Capturing frame...")
        ret, frame = cap.read()

        if ret:
            # Create the captures folder if it does not exist
            print("Checking/creating captures folder...")
            os.makedirs("captures", exist_ok=True)

            # Get current timestamp and format it
            print("Formatting timestamp...")
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

            # Save the captured image
            filename = f"captures/capture-{timestamp}.jpg"
            print(f"Saving image as {filename}...")
            cv2.imwrite(filename, frame)
            print(f"Image saved as {filename}")
        else:
            print("Error: Could not read frame.")
    return filename

def detect_colored_cubes(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for red, green, blue, and yellow
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255, 230])
    lower_green = np.array([72, 50, 50])
    upper_green = np.array([79, 150, 180])
    lower_blue = np.array([103, 80, 0])
    upper_blue = np.array([109, 225, 140])
    lower_yellow = np.array([16, 105, 180])
    upper_yellow = np.array([24, 255, 255])

    # Create masks for each color
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Apply morphological operations to clean the masks
    kernel = np.ones((5, 5), np.uint8)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel)
    mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_CLOSE, kernel)

    # Find contours for each mask
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Function to filter and draw contours for cubes
    def filter_and_draw_contours(contours, color, lower_area, upper_area):
        positions = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            area = cv2.contourArea(contour)
            if lower_area < area < upper_area and 4 <= len(approx) <= 7:  # Adjusted filter condition
                cv2.drawContours(image, [approx], 0, color, 5)
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    positions.append((cX, cY))
        return positions

    # Function to filter and draw contours for yellow calibration marks
    def filter_and_draw_contours_yellow(contours, color):
        positions = []
        areas = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            area = cv2.contourArea(contour)
            if 100 < area < 600 and 4 <= len(approx) <= 7:  # Filter condition for calibration marks
                # cv2.drawContours(image, [approx], 0, color, 5)  # Commented out contour display
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    positions.append((cX, cY))
                    areas.append(area)
        return positions, areas

    # Detect and draw contours for calibration marks
    yellow_positions, yellow_areas = filter_and_draw_contours_yellow(contours_yellow, (0, 255, 255))  # Yellow

    # Calculate average area of calibration marks
    if len(yellow_areas) == 2:
        average_area = sum(yellow_areas) / len(yellow_areas)
        scale_factor = 235 / average_area
    else:
        print("Error: Expected 2 yellow calibration marks but found", len(yellow_areas))
        return

    # Adjust the detection thresholds for other colors based on the scale factor
    # red_positions = filter_and_draw_contours(contours_red, (0, 0, 255), 12000 * scale_factor, 20000 * scale_factor)  # Red
    # green_positions = filter_and_draw_contours(contours_green, (0, 255, 0), 12000 * scale_factor, 20000 * scale_factor)  # Green
    # blue_positions = filter_and_draw_contours(contours_blue, (255, 0, 0), 12000 * scale_factor, 20000 * scale_factor)  # Blue

    # Calibrate the coordinates based on the calibration marks
    if len(yellow_positions) == 2:
        yellow_positions.sort(key=lambda pos: pos[0])  # Ensure left mark is first
        left_mark = yellow_positions[0]
        right_mark = yellow_positions[1]
        left_calib = (3.1, 1.6)
        right_calib = (60.7, 1.6)

        def calculate_relative_position(cube_pos, left_mark, right_mark, left_calib, right_calib):
            x_scale = (right_calib[0] - left_calib[0]) / (right_mark[0] - left_mark[0])
            x_relative = left_calib[0] + (cube_pos[0] - left_mark[0]) * x_scale
            y_relative = left_calib[1]  # Since y-coordinates are the same
            return (x_relative, cube_pos[1])  # Use original y-coordinate for relative position

        def mark_and_print_positions(positions, color_name):
            for pos in positions:
                relative_pos = calculate_relative_position(pos, left_mark, right_mark, left_calib, right_calib)
                cv2.putText(image, f"{color_name} ({relative_pos[0]:.1f}, {relative_pos[1]:.1f})", (pos[0], pos[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                # print(f"{color_name} cube relative position: {relative_pos}")

        # mark_and_print_positions(red_positions, "Red")
        # mark_and_print_positions(green_positions, "Green")
        # mark_and_print_positions(blue_positions, "Blue")

        # Mark the calibration marks with crosses
        for (x, y) in yellow_positions:
            cv2.drawMarker(image, (x, y), (0, 255, 255), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)

        # Label predefined positions and draw circles
        predefined_positions = {
            2: (9.2, 6.8),
            3: (43.5, 3.8)
        }

        radius = 50
        color_masks = {
            "red": mask_red,
            "green": mask_green,
            "blue": mask_blue
        }

        for label, (x, y) in predefined_positions.items():
            x_img = left_mark[0] + (x - left_calib[0]) * (right_mark[0] - left_mark[0]) / (right_calib[0] - left_calib[0])
            y_img = int(left_mark[1])
            cv2.drawMarker(image, (int(x_img), y_img), (255, 255, 255), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
            cv2.putText(image, f"{label}", (int(x_img), y_img - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.circle(image, (int(x_img), y_img), radius, (255, 255, 255), 2)

            # Check color percentages within the circle
            mask_circle = np.zeros_like(mask_red)
            cv2.circle(mask_circle, (int(x_img), y_img), radius, 255, thickness=-1)

            for color_name, color_mask in color_masks.items():
                intersection = cv2.bitwise_and(color_mask, color_mask, mask=mask_circle)
                color_area = cv2.countNonZero(intersection)
                total_area = cv2.countNonZero(mask_circle)
                if total_area > 0 and color_area / total_area > 0.05:
                    print(f"position {label}: {color_name} cube")
                    if color_name=="green":
                        print(f"-> pick {label} place 1")
                    if color_name=="blue":
                        print(f"-> pick {label} place 4")
                    if color_name=="red":
                        print(f"-> pick {label} place ??? (no container)")

    else:
        print("Error: Expected 2 yellow calibration marks but found", len(yellow_positions))

    # Display the image with detected cubes and positions
    cv2.imshow('Detected Cubes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Use the function with the provided image
while True:
    my_input = input("Press Enter to take a picture...")
    if my_input == "q":
        break
    filename = take_picture()
    detect_colored_cubes(filename)

# detect_colored_cubes('captures/capture-20240703-174227.jpg')
# # blue green:
# detect_colored_cubes('captures/capture-20240703-204727.jpg')
# # green blue:
# detect_colored_cubes('captures/capture-20240703-204832.jpg')



# Release the capture
print("Releasing the webcam...")
cap.release()
cv2.destroyAllWindows()
print("Done.")
