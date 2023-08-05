import cv2

def Crop(img,path):
    height, width, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eye_cascade = cv2.CascadeClassifier(path)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 1)

    for (x,y,w,h) in eyes:
        desired_position = (int(x+w/2),int(y+h/2))
        break

    third_width = width // 3
    third_height = height // 3
    intersections = [
        (third_width, third_height),
        (2 * third_width, third_height),
        (third_width, 2 * third_height),
        (2 * third_width, 2 * third_height)
    ]

    distances = [((desired_position[0] - x) ** 2 + (desired_position[1] - y) ** 2) for x, y in intersections]
    closest_intersection_index = distances.index(min(distances))
    closest_intersection = intersections[closest_intersection_index]

    if x > closest_intersection[0]:
        dx = x - closest_intersection[0]
    else:
        dx = closest_intersection[0] - x

    if y > closest_intersection[1]:
        dy = y - closest_intersection[1]
    else:
        dy = closest_intersection[1] - y

    cropped_h = height - dy
    cropped_w = width - dx

    if closest_intersection_index == 1:
        cropped = img[0:cropped_h, -cropped_w:]
    elif closest_intersection_index == 0:
        cropped = img[0:cropped_h, 0:cropped_w]
    elif closest_intersection_index == 3:
        cropped = img[-cropped_h:, -cropped_w:]
    elif closest_intersection_index == 2:
        cropped = img[-cropped_h:, 0:cropped_w]
    else:
        cropped = img

    return cropped