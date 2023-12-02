from pathlib import Path
import cv2 as cv
from math import sqrt,atan2,tan,radians
# from cree_ann import affiche
import matplotlib.pyplot as plt
import os


drag = 0
select_flag = 0
x1 = 0
x2 = 0
y1 = 0
y2 = 0

point1 = [x1,y1]
point2 = [x2,y2]
SCALAR_YELLOW = (0.0,255.0,255.0)
rect_width=80
rect_height=80

def minRectX(p1):

    # a=int(p1[0])
    # b=int(abs(p1[1] - rect_height/2))
    
    # p1_pos=(a,b)
    c=int(p1[0] + rect_width)
    d=int(p1[1] + rect_height/2)
    p2_pos=(c,d)
    
    # cv.rectangle(frame,p1_pos,p2_pos,(255,0,0,),1)
    
    return [p2_pos[0],p1[1]] #updated x and same y

def minRectY(p1):
    
    # a=int(abs(p1[0] - rect_width/2))
    # b=int(p1[1])
    
    # p1_pos=(a,b)
    c=int(p1[0] + rect_width/2)
    d=int(p1[1] + rect_height)
    p2_pos=(c,d)
    # cv.rectangle(frame,p1_pos,p2_pos,(255,0,0,),1)
    
    return [p1[0],p2_pos[1]] #same x and updated y

def createBoxes(p1,p2):
    
    dist_x=sqrt((p2[0] - p1[0])**2)
    dist_y=sqrt((p2[1] - p1[1])**2)
    angle=atan2(dist_y,dist_x)
    # print(dist_x,dist_y,angle)
    rects=[]
    while(1):
        
        if angle == 0.0 or angle <0.78539:
            
            dirx=p2[0] - p1[0]
            if dirx < 0: #back
                t=p1
                p1=p2
                p2=t
            # else forward    
            nx=minRectX(p1)
            # print(nx,p2)
            if nx[0] > p2[0]:
                break
            diry=p2[1]-p1[1]
            if diry < 0:
                nx[1]-=rect_width*tan(radians(angle*57.2958))
            else:
                nx[1]+=rect_width*tan(radians(angle*57.2958))
            
            # if not nx[0]-rect_width <= rect_width/2 + 1: #on boundary
            rects.append((nx[0]-rect_width/2,nx[1],rect_width,rect_height)) #central points + widht/height
            p1=nx

        else:
            diry=p2[1] - p1[1]
            if diry < 0: #up
                t=p1
                p1=p2
                p2=t
        
            #else: down
            ny=minRectY(p1)
            if ny[1] > p2[1]:
                break
            dirx=p2[0] - p1[0]
            if dirx < 0:
                ny[0]-=rect_height/tan(radians(angle*57.2958))
            else:
                ny[0]+=rect_height/tan(radians(angle*57.2958))
            # print(ny[1]-rect_height)
            # if not ny[1]-rect_height <= rect_height/2 + 1: #on boundary
            rects.append((ny[0],ny[1]-rect_height/2,rect_width,rect_height)) #Central Points
            p1=ny
    return rects

def displayBoxes(frame,rects):
    for xc,yc,w,h in rects:
        p1_pos=(int(xc-w/2),int(yc-h/2))
        p2_pos=(int(xc+w/2),int(yc+h/2))
        
        cv.rectangle(frame,p1_pos,p2_pos,(0,255,0,),1)

def delLabel():
    
    
    with open(file_name,'r') as t:
        lines=t.readlines()
    lines=lines[:-1]
    with open(file_name,'w') as t:
        for line in lines:
            t.write(line)
        
    t.close()
    return lines
    


    
def create_labels(rects):
    crack="0"
    
    # fig, ax = plt.subplots()
    # img=ax.imshow(img)
    # x=img.get_extent()[1]
    # y=img.get_extent()[2]
    rect_=[]
    for x_,y_,w,h in rects:
        # x_=x_ + w/2
        # y_=y_ + h/2
        if not y_ <= rect_height/10 + 1 and not x_ <= rect_width/10 +1: #boundary condition
            if img_y_extent > y_ + rect_height/10 + 1 and img_x_extent > x_ + rect_width/10 +1:
                # print(y_,img_y_extent)
                w_=round(float(w/img_x_extent),6)
                h_=round(float(h/img_y_extent),6)
                x_=round(float(x_/img_x_extent),6)
                y_=round(float(y_/img_y_extent),6)
                
                rect_.append((x_,y_,w_,h_))
    # print(rect)
    # print(rect_)
    if not os.path.exists(ann_path):
        os.mkdir(ann_path) 
    
    with open(file_name,"a") as f:
        for x,y,w,h in rect_:
            sep=" "
            lbl=crack+sep+str(x)+sep+str(y)+sep+str(w)+sep+str(h)
            f.write(lbl)
            f.write("\n")
    f.close()
    # plt.close()
    
    
def displayLine(frame):
    global point1
    global point2
    cv.line(frame,(point1[0],point1[1]),(point2[0],point2[1]),SCALAR_YELLOW,1,8)

def refresh(img,lbls):
    rects=[]
    
    for lbl in lbls:
        lbl=lbl.strip()
        lbl=lbl.split(" ")[1:]
        xc,yc,w,h=lbl #central points and width/height
        xc=int(float(xc)*img_x_extent)
        yc=int(float(yc)*img_y_extent)
        w=int(float(w)*img_x_extent)
        h=int(float(h)*img_y_extent)
        
        rects.append((xc,yc,w,h))
        
    
    displayBoxes(img,rects)
    return img
    
def drawLine(event,x,y,flags,params):

    global point1
    global point2
    global drag
    global select_flag
    global callback
    global raw_img
    
    if (event==cv.EVENT_LBUTTONDOWN and not(drag) and not(select_flag)):
        # print('case 1')
        point1=[x,y]
        drag = 1
        
    if (event == cv.EVENT_MOUSEMOVE and drag and not(select_flag)):
        # print('case 2')
        
        point2 = [x,y]

        rects=createBoxes(point1,point2)
        t_img=raw_img.copy()
        displayBoxes(t_img,rects)
        cv.imshow('figure',t_img) 
        
    if (event == cv.EVENT_LBUTTONUP and drag and not(select_flag)):
        # print('case 3')
        
        point2 = [x,y]
        drag = 0
        # select_flag = 1
        
        # displayLine(raw_img)
        rects=createBoxes(point1,point2)
        displayBoxes(raw_img,rects)
        cv.imshow('figure',raw_img) 
        point1=point2
        callback = 1
        create_labels(rects)
        
    if (event == cv.EVENT_RBUTTONDOWN):
        lbls=delLabel()
        img_data=refresh(org_img.copy(),lbls)
        raw_img=img_data.copy()
        cv.imshow('figure',raw_img) 
        


img_no=0
org_img=0
raw_img=0
img_x_extent,img_y_extent=0,0
ann_path=Path("labels"+str(rect_width)+"x"+str(rect_height))

data_path=Path("F:/crack detection/docs and reports/task5/cracktree260/train")
file_name=''
if __name__ == "__main__":
    
    
    
    data_path=list(data_path.glob("image/*.jpg"))
    i=0
    while 1:
        img=str(data_path[i])
        img_no=img.split(os.sep)[-1].split(".")[0]
        file_name=str(ann_path)+os.sep+str(img_no)+".txt"
        # if os.path.exists(file_name):
        #     os.remove(file_name)
        data=cv.imread(img)
        org_img=cv.cvtColor(data,cv.COLOR_BGR2GRAY)
        raw_img=org_img.copy()

        fig, ax = plt.subplots()
        img=ax.imshow(raw_img)
        img_x_extent=img.get_extent()[1]
        img_y_extent=img.get_extent()[2]
        plt.close()
        cv.imshow('figure',raw_img)
        
        cv.setMouseCallback('figure',drawLine)
        k=cv.waitKey(0)
        
        if k == 100: #key=d
            try:
                with open(file_name,'r') as t:
                    lines=t.readlines()
                img_data=refresh(org_img.copy(),lines)
                raw_img=img_data.copy()
                cv.imshow('figure',raw_img)
                k=cv.waitKey(0)
            except:
                pass
        if k == 101:#key=e
            if os.path.exists(file_name):
                os.remove(file_name)
        if k == 110:#key = n
            i+=1
        elif k == 112: #key=p
            i-=1
    
        elif k== 113:# key = q
            break
        cv.destroyAllWindows()
    # affiche([data_path[0]],ann_path)


