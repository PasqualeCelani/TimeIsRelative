import cv2
import numpy as np


isDebug = True
    
def draw_circle_on_img(img, circle):
    x, y, r = np.uint16(np.around(circle))

    green = (0, 255, 0) #BGR
    thikness = 2

    cv2.circle(img, (x, y), r, green, thikness) 

def draw_hands_line_on_img(img, hour_hand_line, minute_hand_line):
    hx1, hy1, hx2, hy2 = hour_hand_line
    cv2.line(img, (hx1, hy1), (hx2, hy2), (0, 0, 255), 3)
        
    mx1, my1, mx2, my2 = minute_hand_line
    cv2.line(img, (mx1, my1), (mx2, my2), (255, 0, 0), 3)



def detect_circle(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=100,      
        param1=100,         
        param2=40,       
        minRadius=30,       
        maxRadius=1800
    )

    if circles is None:
        return None
    
    if len(circles) > 1:
        raise Exception("Sorry you can get just for one clock the hour :) (assumption)")
    
    if isDebug:
        draw_circle_on_img(img, circles[0][0])
    
    return circles[0][0]


def detect_clock_hands(img, circle):
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    x, y, r = np.uint16(np.around(circle))
     
    cv2.circle(mask, (x,y), r, (255, 255, 255), -1)

    img_just_circle = cv2.bitwise_and(img, img, mask=mask)

    gray_img = cv2.cvtColor(img_just_circle, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_img, 50, 150)

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=60,
        minLineLength=int(r * 0.2),
        maxLineGap=20
    )

    hands_with_lengths = [] 
    for line in lines:
        
        x1, y1, x2, y2 = line[0]

        dist1_end_point_from_center = np.linalg.norm(np.array([x1, y1]) - np.array([x, y]))
        dist2_end_point_from_center = np.linalg.norm(np.array([x2, y2]) - np.array([x,y]))

        threshold = r * 0.15 

        if dist1_end_point_from_center < threshold or dist2_end_point_from_center < threshold:
            line_length = np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))
            hands_with_lengths.append((line_length, line[0]))
    

    if len(hands_with_lengths) < 2:
        raise Exception("No clock hands found!")
    
    hands_with_lengths.sort(key=lambda x: x[0])

    hour_hand_line = hands_with_lengths[0][1]
    minute_hand_line = hands_with_lengths[-1][1]

    if isDebug:
        draw_hands_line_on_img(img, hour_hand_line, minute_hand_line)

    return hour_hand_line, minute_hand_line

def get_line_angle_degree(line, center):
    x1, y1, x2, y2 = line

    dist1_from_center = np.linalg.norm(np.array([x1, y1]) - np.array([center[0], center[1]]))
    dist2_from_center = np.linalg.norm(np.array([x2, y2]) - np.array([center[0], center[1]]))

    if dist1_from_center > dist2_from_center:
        farest_center = np.array([x1, y1])
    else:
        farest_center = np.array([x2, y2])
    
    angle_radians = np.arctan2(farest_center[1] - center[1], farest_center[0] - center[0])

    return (np.degrees(angle_radians) + 360) % 360

def convert_angles_to_time(hour_angle, minute_angle):
    normalized_minute_angle = (minute_angle + 90) % 360
    normalized_hour_angle = (hour_angle + 90) % 360

    minutes_float = normalized_minute_angle / 6
    minutes = int(round(minutes_float))

    hour_fraction = normalized_hour_angle / 30
    hour = int(hour_fraction)

    if hour == 0:
        hour = 12

    if minutes == 60:
        minutes = 0
        hour = (hour % 12) + 1 

    return hour, minutes



def get_clock_hour(img):
    circle = detect_circle(img)

    if circle is None:
        raise Exception(f"No clock has found in the image {img}")
    
    hour_hand_line, minute_hand_line = detect_clock_hands(img, circle)
    
    x, y, _ = np.uint16(np.around(circle))
    center = (x, y)

    hour_angle = get_line_angle_degree(hour_hand_line, center)
    minute_angle = get_line_angle_degree(minute_hand_line, center)
    
    hour, minute = convert_angles_to_time(hour_angle, minute_angle)

    return hour, minute
  

def main():
    img = cv2.imread("./data/img4.jpg")


    if img is None:
        raise Exception("Image load failed")
    
    hour, minute = get_clock_hour(img)

    print(f"The time is: {hour}:{minute} :)")

    if isDebug:
        cv2.imshow('Test', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
