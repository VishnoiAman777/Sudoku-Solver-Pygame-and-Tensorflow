import cv2
import numpy as np
import tensorflow
# from tensorflow.keras.models import load_model
import imutils
from solver import *

model = tensorflow.keras.models.load_model('model-OCR.h5')


def find_board(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 13, 20, 20)
    edged = cv2.Canny(bfilter, 30, 180)
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE,
                                 cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    newimg = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 3)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    location = None

    # Finds rectangular contour
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 15, True)
        if len(approx) == 4:
            location = approx
            break
    result = get_perspective(img, location)
    return result, location


# find_board(img)


def get_perspective(img, location, height=900, width=900):
    pts1 = np.float32([location[0], location[3], location[1], location[2]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result


# split the board into 81 individual images
def split_boxes(board):
    """Takes a sudoku board and split it into 81 cells.
    each cell contains an element of that board either given or an empty cell."""
    rows = np.vsplit(board, 9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 9)
        for box in cols:
            box = cv2.resize(box, (48, 48)) / 255.0
            cv2.waitKey(50)
            boxes.append(box)
    cv2.destroyAllWindows()

    return boxes


def read_sudoku(img_name):
    img = cv2.imread(img_name)
    board, location = find_board(img)
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    rois = split_boxes(gray)
    rois = np.array(rois).reshape(-1, 48, 48, 1)
    classes = np.arange(0, 10)
    # model = load_model('model-OCR.h5')
    prediction = model.predict(rois)
    # print(prediction)
    predicted_numbers = []
    # get classes from prediction
    for i in prediction:
        index = (np.argmax(i))
        predicted_number = classes[index]
        predicted_numbers.append(predicted_number)

    sudoku = []
    x = 0
    temp = []
    for i in range(81):
        temp.append(predicted_numbers[i])
        x += 1
        if x % 9 == 0:
            sudoku.append(temp)
            temp = []
            x = 0
    sudoku = list(np.transpose(np.array(sudoku)))
    return sudoku

# [[1,0,4,],[2,4,6,0...]]
