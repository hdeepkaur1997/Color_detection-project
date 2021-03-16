import cv2
import numpy as np
import pandas as pd
import argparse

#Load image
img_path = "image.jpg"
img = cv2.imread(img_path)   
img=cv2.resize(img,(700,500))

clicked = False
r = g = b = xpos = ypos = 0

# Next, we read the CSV file with pandas
# We can use pandas library to perform various operations on data files like CSV. pd.read_csv() reads the CSV file and loads it into the pandas DataFrame.

index = ["colour", "colour_name", "hex", "R", "G", "B"]
csv = pd.read_csv("color_detection.csv", names=index, header = None)

# Calculate distance to get color name
# We have the r,g and b values. Now, we need another function which will return us the color name from RGB values. To get the color name, we calculate a distance(d) which tells us how close we are to color and choose the one having minimum distance

def getColourName(R,G,B):
    minimum = 1000
    for i in range(len(csv)):
        d = abs(R-int(csv.loc[i,"R"]))+ abs(G-int(csv.loc[i,"G"]))+ abs(B-int(csv.loc[i,"B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i,"colour_name"]
    return cname

# Create a draw_function

# It will calculate the rgb values of the pixel which we double click. The function parameters have the event name, (x,y) coordinates of the mouse position, etc. In the function, we check if the event is double-clicked then we calculate and set the r,g,b values along with x,y positions of the mouse.
def draw_function(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos,clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)

# Display image on the window

# Whenever a double click event occurs, it will update the color name and RGB values on the window.
while(1):
    cv2.imshow("image",img)
    if (clicked):
        #cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 thickness fills rectangle entirely
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #Creating text string to display ( Color name and RGB values )
        text = getColourName(r,g,b) + ' R='+ str(r) + ' G='+ str(g) + ' B='+ str(b)

        #cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool) )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
  #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)

        clicked=False

    #Break the loop when user hits 'esc' key 
    if cv2.waitKey(20) & 0xFF ==27:
        break

cv2.destroyAllWindows()

        




