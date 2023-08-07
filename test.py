import cv2

def Crop(img,path):

    height, width, _ = img.shape
    print("shape",img.shape)
    for i in range(3):
        cv2.line(img, (0, height // 3 * (i + 1)), (width, height // 3 * (i + 1)), (0, 255, 0), 2)
        cv2.line(img, (width // 3 * (i + 1), 0), (width // 3 * (i + 1), height), (0, 255, 0), 2)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eye_cascade = cv2.CascadeClassifier(path)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 1)
    for (x,y,w,h) in eyes:
        cv2.circle(img, (int(x+w/2),int(y+h/2)), 2, (0,0,255), 2)
        desired_position = (int(x+w/2),int(y+h/2))
        break
    # print("Eye" ,x,y,w,h)

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
    # print(closest_intersection_index)
    closest_intersection = intersections[closest_intersection_index]
    # print(closest_intersection)
    cv2.circle(img, (closest_intersection[0],closest_intersection[1]), 2, (0,255,255), 2)
    # print("intersec",closest_intersection[0],closest_intersection[1])

    # distance from eye to intersection
    if x > closest_intersection[0]:
        dx = x - closest_intersection[0]
    else:
        dx = closest_intersection[0] - x

    if y > closest_intersection[1]:
        dy = y - closest_intersection[1]
    else:
        dy = closest_intersection[1] - y

    # print("distance",dx,dy)

    # new height and width
    cropped_h = height - dy
    cropped_w = width - dx
    # print("croppedsize",cropped_h,cropped_w)

    # crop from top right corner if cloest intersection is top right
    if closest_intersection_index == 1:
        cropped = img[0:cropped_h, -cropped_w:]
    # crop from top left corner if cloest intersection is top left
    elif closest_intersection_index == 0:
        cropped = img[0:cropped_h, 0:cropped_w]
    # crop from bottom right corner if cloest intersection is bottom right
    elif closest_intersection_index == 3:
        cropped = img[-cropped_h:, -cropped_w:]
    # crop from bottom left corner if cloest intersection is bottom left
    elif closest_intersection_index == 2:
        cropped = img[-cropped_h:, 0:cropped_w]
    else:
        cropped = img


    height, width, _ = cropped.shape
    # #draw new grid in blue
    for i in range(3):
        cv2.line(cropped, (0, height // 3 * (i + 1)), (width, height // 3 * (i + 1)), (255, 0, 0), 1)
        cv2.line(cropped, (width // 3 * (i + 1), 0), (width // 3 * (i + 1), height), (255, 0, 0), 1)
    
    
    return cropped

if __name__ == "__main__":

    img = cv2.imread('pics/test8.jpg')
    img = cv2.resize(img, (0,0), fx=0.15, fy=0.15)
    eyes = Crop(img,'models/haarcascade_eye.xml')
    # faces = Crop(img,'models/haarcascade_frontalface_default.xml')
    cv2.imshow('eye', eyes)
    # cv2.imshow('face', faces)
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()