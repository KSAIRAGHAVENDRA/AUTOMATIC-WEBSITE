import cv2
import imutils
import numpy as np
import argparse
import urllib.request
import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
import json
import time
from io import BytesIO

# import text_recognition as tr

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--image_url", required=True,help="path to the input image")
args = vars(ap.parse_args())

class SketchHTML:
    def __init__(self,image_url):
        self.image_url = image_url

    def url_to_image(self, url):
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)#cv2.IMREAD_COLOR)
        return image

    def sort_contours(self, cnts, method="left-to-right"):
        # initialize the reverse flag and sort index
        reverse = False
        i = 0

        # handle if we need to sort in reverse
        if method == "right-to-left" or method == "bottom-to-top":
            reverse = True

        # handle if we are sorting against the y-coordinate rather than
        # the x-coordinate of the bounding box
        if method == "top-to-bottom" or method == "bottom-to-top":
            i = 1

        # construct the list of bounding boxes and sort them from top to
        # bottom
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                            key=lambda b: b[1][i], reverse=reverse))

        # return the list of sorted contours and bounding boxes
        return (cnts, boundingBoxes)

    def removeUnwantedRectangles(self, contours,img):
        new_contours = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if (w > 100 and h > 80) and w!=img.shape[1] and h!=img.shape[0]:
                new_contours.append(c)
                
        return new_contours

    def checkOverlapBoundingBoxes(self, contours):
        overlapped = [False] * len(contours)
        idx = 0
        for c1 in contours:
            #calculate corners (l1,r1) & (l2,r2)
            l1x, l1y, w1, h1 = cv2.boundingRect(c1)
            r1x, r1y = l1x + w1, l1y + h1

            idx2 = 0
            for c2 in contours:
                if overlapped[idx2] == False:
                    l2x, l2y, w2, h2 = cv2.boundingRect(c2)
                    r2x, r2y = l2x + w2, l2y + h2
                    if l1x != l2x and l1y != l2y:          
                        if l1x>r2x or l2x>r1x:
                            # overlap = False
                            pass
                        elif l1y>r2y or l2y>r1y:
                            # overlap = False
                            pass
                        else:
                            overlapped[idx] = True
                            # print("Overlapped Rect:",l1x,l1y,w1,h1)
                idx2 = idx2 + 1
            idx = idx + 1

        return overlapped

    def isTextWithinBox(self, text_bb,rect_bb):
        l1x, l1y, r1x, r1y = text_bb[0], text_bb[1], text_bb[4], text_bb[5]
        l2x, l2y, r2x, r2y = rect_bb[0], rect_bb[1], rect_bb[0] + rect_bb[2], rect_bb[1] + rect_bb[3]
        if l1x>r2x or l2x>r1x:
            return False
        elif l1y>r2y or l2y>r1y:
            return False
        else:
            return True

    def findButtons(self, texts,boxes):
        buttons = []
        rm_texts = [False] * len(texts)
        rm_boxes = [False] * len(boxes)
        for rect_bb in boxes:
            for t in texts:
                if self.isTextWithinBox(t[0],rect_bb)==True:
                    buttons.append((rect_bb,t[1]))
                    rm_texts[texts.index(t)] = True
                    rm_boxes[boxes.index(rect_bb)] = True
                    # print("removed:", t, rect_bb)

        texts = [texts[i] for i in range(len(texts)) if rm_texts[i]==False]
        boxes = [(boxes[i],"") for i in range(len(boxes)) if rm_boxes[i]==False]
        return [buttons,texts,boxes]

    def box_extraction(self, img, cropped_dir_path):

        # img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
        (thresh, img_bin) = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
        # img_bin = 255-img_bin  # Invert the image
        img_bin = cv2.bitwise_not(img_bin)
        # cv2.imwrite("Image_bin.jpg",img_bin)
       
        # Defining a kernel length
        kernel_length = np.array(img).shape[1]//40
         
        # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
        verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
        # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
        hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
        # A kernel of (3 X 3) ones.
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        # Morphological operation to detect verticle lines from an image
        img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
        verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
        # cv2.imwrite("verticle_lines.jpg",verticle_lines_img)

        # Morphological operation to detect horizontal lines from an image
        img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
        horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
        # cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)

        # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
        alpha = 0.5
        beta = 1.0 - alpha
        # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
        img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
        img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
        (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # For Debugging
        # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
        # cv2.imwrite("img_final_bin.jpg",img_final_bin)

        # Find contours for image, which will detect all the boxes
        img_op, contours, hierarchy = cv2.findContours(
            img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Sort all the contours by top to bottom.
        (contours, boundingBoxes) = self.sort_contours(contours, method="top-to-bottom")

        contours = self.removeUnwantedRectangles(contours,img)
        overlapped = self.checkOverlapBoundingBoxes(contours)
        # print(overlapped)

        idx = 0
        img_idx = 0
        boxes = []
        for c in contours:
            # Returns the location and width,height for every contour
            x, y, w, h = cv2.boundingRect(c)

            # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
            if overlapped[idx]==False:
                img_idx = img_idx + 1
                new_img = img[y:y+h, x:x+w]
                # cv2.circle(img, (x,y), 40, (255, 0, 0), -1)
                cv2.imwrite(cropped_dir_path+str(img_idx) + '.png', new_img)
                # print(x, y, w, h )
                boxes.append([x,y,w,h])
            idx += 1

        return boxes
        # cv2.imshow("output",imutils.resize(img, width=300))
        # cv2.waitKey(0)

    def generate_html(self, rows,buttons,boxes,texts):
        code = "<!DOCTYPE html>"+'\n'+"<html>"+'\n'
        #add page title
        code = code + "<head>"+'\n'+"<title>"+texts[0][1]+"</title>"+'\n'+"</head>"+'\n'
        #add body tag
        code = code + "<body>"+'\n'
        #add div
        code = code + "<div class=\"container\">" + '\n' + "<br>" + '\n'

        #add elements from top-to-bottom
        for line in rows:
            for element in line:
                if element[1] == "text":
                    code = code + "<label class=\""+element[0][1].replace(" ", "")+"\">"+element[0][1]+"</label>" + '\n' #class for plaintext is text-itself
                    # code = code + "<br>" + '\n'
                if element[1] == "textfield":
                    code = code + "<input type=\"text\" class=\"t"+str(element[0][0][0]).replace(" ", "")+"\" required>" + '\n'
                    # code = code + "<br>" + '\n'
                if element[1] == "button":
                    code = code + "<button class=\""+element[0][1].replace(" ", "")+"\" type=\"submit\">"+element[0][1]+"</button>"+'\n' #class for button is button-text
                    # code = code + "<br>" + '\n'
            code = code + "<br>" + '\n'

        #close div
        code = code + "<br>" + '\n' + "</div>" + '\n'

        #add css styling
        style = "<style>" + '\n'
        style = style + ".container {background-color: #f2f2f2;padding: 5px 20px 15px 20px;border: 1px solid lightgrey;border-radius: 3px;}"+'\n'
        style = style + "button:hover {background-color: #45a049;}"+'\n'

        for line in rows:
            currentx = 0
            for element in line:
                if element[1] == "text":
                    currentx = element[0][0][0] - currentx
                    style = style + "label."+element[0][1].replace(" ", "")+"{margin-left:"+str(currentx)+"px;}" + '\n'
                if element[1] == "textfield":
                    currentx = element[0][0][0] - currentx
                    style = style + "input[type=text].t"+str(element[0][0][0]).replace(" ", "")+"{margin-left:"+str(currentx)+"px;"#+"width:"+element[0][0][2]/
                    style = style + "padding: 12px;border: 1px solid #ccc;border-radius: 3px;}" + '\n'  
                if element[1] == "button":
                    currentx = element[0][0][0] - currentx
                    print(currentx,element[0][1])
                    style = style + "button."+element[0][1].replace(" ", "")+"{background-color: #4CAF50;color: white;padding: 12px;margin: 10px 0;"
                    style = style + "margin-left:"+str(currentx)+"px;"
                    style = style + "border: none;border-radius: 3px;cursor: pointer;font-size: 17px;}" + '\n'

        style = style + "</style>"+'\n'
        code = code + style

        #close body tag
        code = code + "</body>"+'\n'
        #close html tag
        code = code + "</html>"+'\n'

        return code

    def findRows(self, buttons,boxes,texts):
        elements = []
        for b in buttons:
            elements.append((b,"button"))
        for b in boxes:
            elements.append((b,"textfield"))
        for t in texts:
            elements.append((t,"text"))

        elements.sort(key = lambda x: x[0][0][1]) #sort based on y-axis top-to-bottom

        #get all elements in a line in single-row
        rows = []
        for i in range(len(elements)):
            if i != 0 and (elements[i][0][0][1] - elements[i-1][0][0][1] <= 5) :
                rows[len(rows)-1].append(elements[i])
                rows[len(rows)-1].sort(key = lambda x: x[0][0][0])
            else:
                rows.append([elements[i]])

        return rows
        
    def save_as_html(self, code):
        file1 = open("generated_page"+".htm","w")
        file1.write(code)
        file1.close()

    def get_text(self):
        # Add your Computer Vision subscription key and endpoint to your environment variables.
        subscription_key = 'a31ff38d1335419792f36df84eb6a5f9'
        endpoint = 'https://textrecognitionsrini.cognitiveservices.azure.com/'
        text_recognition_url = endpoint + "vision/v2.1/read/core/asyncBatchAnalyze"

        # Set image_url to the URL of an image that you want to analyze.
        # image_url = "https://ragstorageaccount.blob.core.windows.net/ragcontainer/mytest4.jpeg"

        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        params = {'visualFeatures': 'Categories,Description,Color'}
        data = {'url': self.image_url}
        response = requests.post(
            text_recognition_url, headers=headers, json=data)
        response.raise_for_status()

        # Extracting text requires two API calls: One call to submit the
        # image for processing, the other to retrieve the text found in the image.

        # Holds the URI used to retrieve the recognized text.
        operation_url = response.headers["Operation-Location"]

        # The recognized text isn't immediately available, so poll to wait for completion.
        analysis = {}
        poll = True
        while (poll):
            response_final = requests.get(
                response.headers["Operation-Location"], headers=headers)
            analysis = response_final.json()
            # print(analysis)
            time.sleep(1)
            if ("recognitionResults" in analysis):
                poll = False
            if ("status" in analysis and analysis['status'] == 'Failed'):
                poll = False

        polygons = [(line["boundingBox"], line["text"]) for line in analysis["recognitionResults"][0]["lines"]]
        # print(polygons)
        return polygons

if __name__ == "__main__":
    # image_url = "https://ragstorageaccount.blob.core.windows.net/ragcontainer/mytest4.jpeg"
    image_url = args["image"]
    obj = SketchHTML(image_url)
    img = obj.url_to_image(image_url)
    boxes = obj.box_extraction(img, "./src/Cropped/")  # ./src/webtest2.jpeg

    texts = obj.get_text()
    return_list = obj.findButtons(texts,boxes)
    buttons,texts,boxes = return_list[0],return_list[1],return_list[2]
    print("Buttons :",buttons)
    print("Text Fields :",boxes)
    print("Plain Texts :",texts)

    rows = obj.findRows(buttons,boxes,texts)
    print("ROWS:",rows)
    code = obj.generate_html(rows,buttons,boxes,texts)
    obj.save_as_html(code)
