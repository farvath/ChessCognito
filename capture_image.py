import cv2
import numpy as np

def perspective_transform(img, pts):
    """Apply perspective transform based on selected points and draw points on the transformed image."""
    width, height = img.shape[1], img.shape[0]
    dst_size = max(width, height)
    
    # Destination points for perspective transform (top-left, top-right, bottom-left, bottom-right)
    dst_pts = np.float32([[0, 0], [dst_size - 1, 0], [0, dst_size - 1], [dst_size - 1, dst_size - 1]])

    # Compute perspective transform matrix
    M = cv2.getPerspectiveTransform(pts, dst_pts)

    # Apply perspective transform to the image
    transformed_img = cv2.warpPerspective(img, M, (dst_size, dst_size))

    # Draw selected points on the transformed image
    for pt in pts:
        cv2.circle(transformed_img, (int(pt[0]), int(pt[1])), 5, (0, 255, 0), -1)  # Green circle

    return transformed_img

def init_trackbars(window_name, img, placeholder_size):
    """Initialize trackbars with image corner points."""
    width, height = img.shape[1], img.shape[0]

    # Set default corner points to the corners of the image
    default_pts = np.float32([[0, 0], [width - 1, 0], [0, height - 1], [width - 1, height - 1]])

    # Create named window and trackbars
    cv2.namedWindow(window_name)
    
    for i, pt in enumerate(['TL', 'TR', 'BL', 'BR']):
        cv2.createTrackbar(f'x_{pt}', window_name, int(default_pts[i, 0]), width - 1, lambda x: None)
        cv2.createTrackbar(f'y_{pt}', window_name, int(default_pts[i, 1]), height - 1, lambda x: None)

    # Display a placeholder image to reserve space for trackbars
    cv2.imshow(window_name, np.zeros(placeholder_size, dtype=np.uint8))

    return default_pts

def get_trackbar_values(window_name):
    """Retrieve current trackbar values."""
    pts = []

    for i, pt in enumerate(['TL', 'TR', 'BL', 'BR']):
        x = cv2.getTrackbarPos(f'x_{pt}', window_name)
        y = cv2.getTrackbarPos(f'y_{pt}', window_name)
        pts.append([x, y])

    return np.float32(pts)

def main():
    # Load input image
    img_path = 'test_images/sample2.jpg'
    input_size = (400, 400)
    img = cv2.imread(img_path)

    if img is None:
        print(f"Error: Unable to load image from {img_path}")
        return

    # Resize input image to a fixed size
    img = cv2.resize(img, input_size)

    # Define sizes for windows and placeholder image
    slider_window_name = 'Perspective Transformation (Slider Interface)'
    transformed_window_name = 'Transformed Image'
    placeholder_size = (20, 400)  # Adjust size to reserve space for trackbars

    # Initialize trackbars and get default points
    default_pts = init_trackbars(slider_window_name, img, placeholder_size)

    while True:
        # Get current trackbar values
        pts = get_trackbar_values(slider_window_name)

        # Apply perspective transform based on current points
        transformed_img = perspective_transform(img, pts)

        # Display original and transformed images
        cv2.imshow('Original Image', img)
        cv2.imshow(transformed_window_name, transformed_img)

        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quit on 'q' key press
            break

    # Clean up and close windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
