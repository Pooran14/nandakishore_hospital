import cv2
import easyocr
# import cvzone
import matplotlib.pyplot as plt
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
            x1, y1 = map(int, p1) #print(x1,y1)top left
            x2, y2 = map(int, p2) #print(x2,y2)top right
            x3, y3 = map(int, p3) #print(x3,y3)bottom left
            x4, y4 = map(int, p4) #print(x4,y4)bottom right
            #print(f"(x1:{x1} y1:{y1} x2 :{x2} y2: {y2}):{text}\n")
            area=(x2-x1)*(y3-y2)
            width=x3-x1
            height=y3-y1
            # cv2.rectangle(image,(x1,y1),(x3,y3),(255, 0, 0), 3)
            # cv2.putText(image, f"text: {text}", (x1,y1 - 10),
            #         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
        while index < len(varm):
            varx1, vary1, varx3, vary3 = varm[index]
            for i in unfbboxes:
                (bbox, text, area, x1, y1, x3, y3, width, height) = i
                if vary1 - mh - (space * 1.3) <= y1 and vary1 + mh + (space * 1.3) >= y3 and height >= mh - (space * 1.3) and height <= mh + (space * 1.3):
                    if x1 >= varx1-(space * 3) and x1 <= varx3 + (space * 1.5):
                        if vary1-5 <= y3 :
                            if x1 <= varx3+5:
                                if not "€" in text:
                                    print(text, area, x1, y1, x3, y3, width, height, sizelen, space)
                                    fbboxes.append(i)
                                    lst_text.append([text,x1,y1])
                                    if varx3 <= x3 and [x1, y1, x3, y3] not in varm:
                                        varm.append([x1, y1, x3, y3])
            index += 1
        
        unique_nested_list = [list(t) for t in set(tuple(sublist) for sublist in lst_text)]
        unique_nested_list = sorted(unique_nested_list, key=lambda x: x[2])
        print(text_position(unique_nested_list,space))
      


        for (bbox,text,area,x1,y1,x3,y3,width,height) in fbboxes: 
            #print(f"(x1:{x1} y1:{y1} x2 :{x2} y2: {y2}):{text}\n")
            cv2.rectangle(image,(x1,y1),(x3,y3),(255, 0, 0), 3)
            cv2.putText(image, f"text: {text}", (x1,y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Display the image with bounding boxes
        plt.figure(figsize=(10, 6))
        plt.imshow(image)
        plt.axis("off")
        plt.title("Tablets Name (Blue Box)")
        plt.show()
 

























if __name__=="__main__":
    image_path=r"E:\poorani project\images\unprocessedimage\sample1.jpg" 
    image_paths = [fr"E:\poorani project\images\processedimage\sample medicine{i}.jpg" for i in range(1, 20)]

# for image_path in image_paths:
    easyocr_find(image_path)

