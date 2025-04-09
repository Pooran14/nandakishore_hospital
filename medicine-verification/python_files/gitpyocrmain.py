import cv2
import easyocr
import cvzone
import matplotlib.pyplot as plt
import crop_text_region
import os
def text_position(arr, space):
    sorted_text = []
    
    for i, (text1, x1, y1) in enumerate(arr):
        is_valid = True
        
        for j, (text2, x2, y2) in enumerate(arr):
            if i != j and text2 not in sorted_text:
                if not (y1 <= y2 + 10 and x1 - (space * 3) <= x2):
                    is_valid = False
                    break
        
        if is_valid:
            sorted_text.append(text1)
    
    for text, _, _ in arr:
        if text not in sorted_text:
            sorted_text.append(text)
    
    return " ".join(sorted_text)
def wrap_text_to_fit(text, font, font_scale, thickness, max_width):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test_line = line + " " + word if line else word
        text_size = cv2.getTextSize(test_line, font, font_scale, thickness)[0]

        if text_size[0] <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word

    if line:
        lines.append(line)

    return lines
                


def easyocr_find(image_path):
    reader=easyocr.Reader(["en"])
    result=reader.readtext(image_path)
    image=cv2.imread(image_path)
    if result:
        unfbboxes=[]
        fbboxes=[]
        mainboxes=[]
        text_list=[]
        for (bbox,text,_) in result: 
            p1,p2,p3,p4=bbox
            x1, y1 = map(int, p1)       #print(x1,y1)top left
            x2, y2 = map(int, p2)       #print(x2,y2)top right
            x3, y3 = map(int, p3)       #print(x3,y3)bottom left
            x4, y4 = map(int, p4)       #print(x4,y4)bottom right
            area=(x2-x1)*(y3-y2)
            width=x3-x1
            height=y3-y1
            
            unfbboxes.append((bbox,text,area,x1,y1,x3,y3,width,height))
            if "tablet" in text.lower() or "capsules" in text.lower():
                sizelen=len(text)
                mainboxes.append((bbox,text,area,x1,y1,x3,y3,width,height,sizelen))

                
        mainboxes = sorted(mainboxes, key=lambda x: x[2], reverse=True)
        frstmain=mainboxes[0]
        mx1=frstmain[3]
        my1=frstmain[4]
        mx3=frstmain[5]
        my3=frstmain[6]
        mw=frstmain[7]
        mh=frstmain[8]
        space=mw//(frstmain[9])
        varm= [[mx1,my1,mx3,my3]]
        sizelen=frstmain[9]
        text_list.append([frstmain[1],mx1,my1])
        lst_text=[]
        index = 0
        x_coordinates=[]
        y_coordinates=[]
        while index < len(varm):
            varx1, vary1, varx3, vary3 = varm[index]
            for i in unfbboxes:
                (bbox, text, area, x1, y1, x3, y3, width, height) = i
                if vary1 - mh - (space * 1.3) <= y1 and vary1 + mh + (space * 1.3) >= y3 and height >= mh - (space * 1.3) and height <= mh + (space * 1.3):
                    if x1 >= varx1-(space * 3) and x1 <= varx3 + (space * 1.5):
                        if vary1-5 <= y3 :
                            if x1 <= varx3+5:
                                if not "€" in text:
                                    # print(text, area, x1, y1, x3, y3, width, height, sizelen, space)
                                    fbboxes.append(i)
                                    x_coordinates.extend([x1, x3])
                                    y_coordinates.extend([y1, y3])
                                    lst_text.append([text,x1,y1])
                                    if varx3 <= x3 and [x1, y1, x3, y3] not in varm:
                                        varm.append([x1, y1, x3, y3])
            index += 1
        
        unique_nested_list = [list(t) for t in set(tuple(sublist) for sublist in lst_text)]
        unique_nested_list = sorted(unique_nested_list, key=lambda x: x[2])      

        min_x = min(x_coordinates)
        max_x = max(x_coordinates)
        min_y = min(y_coordinates)
        max_y = max(y_coordinates)
        cvzone.cornerRect(image,bbox=(min_x,min_y,max_x-min_x,max_y-min_y),colorR=(255, 0, 0), l=20,rt=1,t=5)
        text = f"{text_position(unique_nested_list, space)}"
        print(f"Medicine:{text}")
        box_width = max_x - min_x
        print(min_x,min_y,max_x,max_y)
        wrapped_text = wrap_text_to_fit(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, thickness=2, max_width=box_width)        
        y_offset = min_y - 10 -40*(len(wrapped_text)-1)
        for line in wrapped_text:
            cvzone.putTextRect(image, line, (min_x+10,y_offset), 
                            scale=1, thickness=2, 
                            colorR=(255, 0, 0), colorT=(255, 255, 255), 
                            font=cv2.FONT_HERSHEY_SIMPLEX, offset=10)     
            y_offset += 40  # Move to the next line

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Display the image with bounding boxes
        plt.figure(figsize=(10, 6))
        plt.imshow(image)
        plt.axis("off")
        plt.title(f"Tablets Name:{text}")
        plt.show()
        return [min_x-10,min_y-10,max_x+10,max_y+10]
 



























if __name__=="__main__":
    # image_path= r"E:\poorani project\images\processedimage\sample medicine12.jpg"
    image_paths = [fr"..images\processedimage\sample medicine{i}.jpg" for i in range(7, 22)]
for image_path in image_paths:
    output_path = r"..\images\unprocessedimage\sample medicine.jpg"
    crop_text_region.crop_image(image_path,easyocr_find(image_path),output_path)
    # print(output_path)
    easyocr_find(output_path)
    os.remove(output_path)