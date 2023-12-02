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
rect_max=80
rect_min=20
rwx=0
rwy=0
# title=str(rect_min)+"_"+str(rect_max)
title=str(rect_max)+"x"+str(rect_max)

def minRectX(p1):
    c=int(p1[0] + rect_min)
    
    return [c,p1[1]] #updated x and same y



def minRectY(p1):
    
    d=int(p1[1] + rect_min)
    
    return [p1[0],d] #same x and updated y

def createBoxes(p1,p2,rwx,rwy):
    
    dist_x=sqrt((p2[0] - p1[0])**2)
    dist_y=sqrt((p2[1] - p1[1])**2)
    angle=atan2(dist_y,dist_x)
    # print(dist_x,dist_y,angle)
    rects=[]
    contX=False
    contY=False
    while(1):
        
        if angle == 0.0 or angle <0.78539:
            
            dirx=p2[0] - p1[0]
            if dirx < 0: #back
                t=p1
                p1=p2
                p2=t
            # else forward    
            
            while 1:
                if rwx < rect_min: #initial condition
                    nx=minRectX(p1)
                    if nx[0] > p2[0]:
                        contX=False
                        break
                    rwx+=rect_min
                    
                else: 
                    if rwx < rect_max:
                        p2x_old=p1[0]+rwx
                        dx=p2[0]-p2x_old
                        new_width=rwx+dx
                        if new_width < rect_max:
                            rwx+=dx
                            nx=[p1[0]+rwx,p1[1]]
                        else:
                            rwx=rect_max
                            nx=[p1[0]+rect_max,p1[1]]
                            
                        contX=True
                        break
            
                
            if contX:
                diry=p2[1]-p1[1]
                if diry < 0:
                    
                    nx[1]-=rwx*tan(radians(angle*57.2958))
                else:
                    nx[1]+=rwx*tan(radians(angle*57.2958))
            
            # if not nx[0]-rect_width <= rect_width/2 + 1: #on boundary
                rects.append((nx[0]-rwx/2,nx[1],rwx,rwx)) #central points + widht/height
                p1=nx
                if rwx >= rect_max:rwx=0
            else: break
            

        else:
            diry=p2[1] - p1[1]
            if diry < 0: #up
                t=p1
                p1=p2
                p2=t
        
            while 1:
                if rwy < rect_min: #initial condition
                    ny=minRectY(p1)
                    if ny[1] > p2[1]:
                        contY=False
                        break
                    rwy+=rect_min
                else:
                    if rwy < rect_max:
                        p2y_old=p1[1]+rwy
                        dy=p2[1]-p2y_old
                        new_height=rwy+dy
                        if new_height < rect_max:
                            rwy+=dy
                            ny=[p1[0],p1[1]+rwy]
                        else:
                            rwy=rect_max
                            ny=[p1[0],p1[1]+rect_max]
                            
                        contY=True
                        break

            if contY:
                dirx=p2[0] - p1[0]
                if dirx < 0:
                    ny[0]-=rwy/tan(radians(angle*57.2958))
                else:
                    ny[0]+=rwy/tan(radians(angle*57.2958))
                # print(ny[1]-rect_height)
                # if not ny[1]-rect_height <= rect_height/2 + 1: #on boundary
                rects.append((ny[0],ny[1]-rwy/2,rwy,rwy)) #Central Points
                if rwy >= rect_max:rwy=0
                p1=ny
            else: break
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
    
    rect_=[]
    for x_,y_,w,h in rects:
        
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
    global rwx
    global rwy
    
    if (event==cv.EVENT_LBUTTONDOWN and not(drag) and not(select_flag)):
        # print('case 1')
        point1=[x,y]
        drag = 1
        rwx=0
        rwy=0
        
    if (event == cv.EVENT_MOUSEMOVE and drag and not(select_flag)):
        # print('case 2')
        
        point2 = [x,y]

        rects=createBoxes(point1,point2,rwx,rwy)
        t_img=raw_img.copy()
        displayBoxes(t_img,rects)
        cv.imshow('figure',t_img) 
        
    if (event == cv.EVENT_LBUTTONUP and drag and not(select_flag)):
        # print('case 3')
        
        point2 = [x,y]
        drag = 0
        
        rects=createBoxes(point1,point2,rwx,rwy)
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
ann_path=Path("labels"+title)

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
        
        if k == 100: #key=d (display)
            try:
                with open(file_name,'r') as t:
                    lines=t.readlines()
                img_data=refresh(org_img.copy(),lines)
                raw_img=img_data.copy()
                cv.imshow('figure',raw_img)
                k=cv.waitKey(0)
            except:
                pass
        if k == 101:#key=e (erase label file)
            if os.path.exists(file_name):
                os.remove(file_name)
        if k == 110:#key = n (next)
            i+=1
        elif k == 112: #key=p (previous)
            i-=1
    
        elif k== 113:# key = q (quit)
            break
        cv.destroyAllWindows()
    


