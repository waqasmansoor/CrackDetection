import numpy as np
from pathlib import Path
import cv2 as cv
import tqdm
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os


def trouve_des_contours(mat,img):
    
    contours,_=cv.findContours(mat,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    fig, ax = plt.subplots()
    img_ax=ax.imshow(img)    
    # x=img.get_extent()[1]
    # y=img.get_extent()[2]
    rect=[]
    for cont in contours:
        rect.append(cv.boundingRect(cont))
    plt.close()
    # x_,y_,w_,h_=rect[-2]
    # r=mat[y_:y_+h_,x_:x_+w_]
    # img=img[y_:y_+h_,x_:x_+w_]
    # img_ax=ax.imshow(img)    
    # contours,_=cv.findContours(r,cv.RETR_FLOODFILL, cv.CHAIN_APPROX_NONE)
    rect=[]
    for cont in contours:
        rect.append(cv.boundingRect(cont))
    return rect
    for i in rect:
        w=float(i[2])
        h=float(i[3])
        print(i)
        xy=(float(i[0]),float(i[1]))
        rect = patches.Rectangle((xy[0],xy[1]), w, h, linewidth=1, edgecolor='w', facecolor='none')
        ax.add_patch(rect)


    plt.show()
    # plt.imshow(r)
    # plt.show()

def fais_nette(img):
    kernel=np.array([
        [0,-1,0],
        [-1,5,-1],
        [0,-1,0]
    ])
    img_br=cv.filter2D(img,ddepth=-1,kernel=kernel)
    return img_br

def cree_un_dossier(rect,p,no,img):
    crack="0"
    
    fig, ax = plt.subplots()
    img=ax.imshow(img)
    x=img.get_extent()[1]
    y=img.get_extent()[2]
    rect_=[]
    for x_,y_,w,h in rect:
        x_=x_ + w/2
        y_=y_ + h/2
        w_=round(float(w/x),6)
        h_=round(float(h/y),6)
        x_=round(float(x_/x),6)
        y_=round(float(y_/y),6)
        
        rect_.append((x_,y_,w_,h_))
    # print(rect)
    # print(rect_)
    if not os.path.exists(p):
        os.mkdir(p) 
    with open(str(p)+os.sep+str(no)+".txt","w") as f:
        for x,y,w,h in rect_:
            sep=" "
            lbl=crack+sep+str(x)+sep+str(y)+sep+str(w)+sep+str(h)
            f.write(lbl)
            f.write("\n")
    f.close()
    plt.close()

def cree_les_anns(image_files,ann_path):
    for i in tqdm.tqdm(range(len(image_files))):
        img_p=image_files[i]
        # print(img_p)
        img_no=str(img_p).split(os.sep)[-1].split(".")[0]
        im=cv.imread(str(img_p))
        im_g=cv.cvtColor(im,cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(im_g, 127, 255, 0)
        img_br=fais_nette(thresh)
        rect=trouve_des_contours(img_br,im)
        cree_un_dossier(rect,ann_path,img_no,im)

def affiche(images,anns):

    for img in images:
        img_no=str(img).split(os.sep)[-1].split(".")[0]
        lbl_path=Path(str(anns)+os.sep+img_no+".txt")
        if lbl_path.is_file():
            rect=[]
            with open(lbl_path) as t:
                t = t.read().strip().splitlines()
                rect+=[x.split(" ")[1:] for x in t]

            fig, ax = plt.subplots()
            img=plt.imread(str(img))
            img=ax.imshow(img)
            x=img.get_extent()[1]
            y=img.get_extent()[2]
            for i in rect:
                
                w=float(i[2])*x
                h=float(i[3])*y
                xy=(float(i[0])*x,float(i[1])*y)
                rect = patches.Rectangle((xy[0]-w/2,xy[1]-h/2), w, h, linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
                
            plt.show()
            
        else:
            print(lbl_path,"Don't exist")

if __name__ == "__main__":
    images_path=Path("mask")
    image_files=list(images_path.glob("*.bmp"))
    ann_path=Path("labels")
    cree_les_anns(image_files,ann_path)
    affiche(image_files,ann_path)

    