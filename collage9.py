ad = "/Users/mac/Documents/coll/"
from PIL import Image
import time
import os
from os import listdir
import random

def main(repeats):
    def isfloat(i):
        try:
            float(i)
            return True
        except ValueError:
            return False
    print("")
    text = input("Welcome to the collage zone. Do you want to faff? ")
    if text == "":
        return CC(0.2, 0.3, 0.2, False, 1)
    
    if text in {"Y", "y"} or len(text) < 5 and len(text) > 1 and text[0].lower() == "y" and text[1] in {"e", "E"}:
        l = []
        print("ADVANCED SUITE use low numbers for the 3 types of borders, eg '0.15' - one option is not currently available in this version, so just hit enter , as it says ")
        advancedModeKey = ["middle borders :", "vertical borders :", "edge borders :", "**JUST HIT ENTER**", "type 0 or 1 :"]
        for i in range(repeats):
            l = []
            if i != 0:
                will = input("carry on with advanced mode y/n ? 'rs' to shuffle ")
                if will == "n":
                    break
                if will == "rs":
                    CC(float(ll[0]), float(ll[1]), float(ll[2]), True, int(ll[4]))
                    continue
            for j in range(5):
                AM = "enter " + advancedModeKey[j]
                l.append(input(AM))
                if j != 3:
                    if isfloat(l[-1]) and float(l[-1]) > -0.5:
                        continue
                    while not isfloat(l[-1]) or float(l[-1]) < -0.5:
                        l[-1] = input(AM)
                
                
            CC(float(l[0]), float(l[1]), float(l[2]), False, int(l[4]))
            ll = l.copy()
            if i == repeats - 1:
                return
        
    for j in range(repeats):
        if j == 0:
            ll = [0.2, 0.2, 0.2, False, 1]
            CC(0.2, 0.2, 0.2, False, 1)
            continue
        text = input("'b' for more borders, 'S' for a shuffle - eg 'b' or 'S' or 'bb', 'bbbbb' etc. Type 'n' for minimal borders ")
        l = [0.05, False]
        for i in text:
            if i.lower() == "b":
                if l[0] < 1:
                    l[0] *= 1.5
                else:
                    warning = input("this could make the program crash - type 'n' to output a slightly smaller image or hit enter to go ahead : ")
                    if warning.lower() == "n":
                        break
                    l[0] += 0.5
                    
                continue
            if i.lower() == "s":
                l[1] = True
                continue
            if text.lower() == "n":
                l = [0, False]
                break
        if l[1]:
            l = ll.copy()
            CC(l[0], l[1], l[2], True, int(l[4]))
            continue
        if l[0] < 0.1:
            l = [l[0], l[0], 0, l[1], 1]
        else:
            l = [l[0], l[0], l[0], l[1], 1]
        ll = l.copy()
        CC(l[0], l[1], l[2], l[3], int(l[4]))
        continue

def CC(middle_border, top_border, edge_border, shuffle, middle):
    global ad
    pics = []
    height = 0
    width = 0
    for i in os.listdir(ad):
        if i == ".DS_Store":
            continue
        img = Image.open(ad + i)
        x, y = img.size
##      pics =  (0:ad, 1:x, 2:y 3:c 4:offsetX 5:offsetY)
        pics.append([ad + i, x, y, 0, 0, 0])
        width += x
        if y > height:
            height = y
    pics.sort()
    if shuffle:
        random.shuffle(pics)
    pics[-1][3] = 1
    
    yoffset = int(top_border * height / 2)
    if len(pics)>1:
        xoffset = int(middle_border * width / (len(pics) - 1))
    else:
        xoffset = int(middle_border * width)
    offsetx = 0
    dim = [0, 0]
##  to stack stackable images, and then add the positional data
    for i in range(len(pics)):
        pics[i][5] += yoffset
        if pics[i][3] == 1:
            if middle == 1:
                pics[i][5] += int((height - pics[i][2]) / 2)
                
        if pics[i][3] == 0:
            if pics[i + 1][2] + pics[i][2] < height:
                pics[i][3] = 2
                pics[i + 1][3] = 3
                if pics[i][1] > pics[i + 1][1]:
                    pics[i + 1][1] = pics[i][1]
                    
        pics[i][4] = offsetx
        if pics[i][3] == 2:
            if height - pics[i + 1][2] - pics[i][2] - xoffset > 0:
                if middle == 1:
                    pics[i][5] += int((height - pics[i + 1][2] - pics[i][2] - xoffset) / 2)
                    pics[i + 1][5] += int((height + pics[i + 1][2] + pics[i][2] + xoffset) / 2) - pics[i + 1][2]
                    
                if middle == 0:
                    pics[i + 1][5] += height - pics[i + 1][2]
            else:
                pics[i + 1][5] += height - pics[i + 1][2]
                
        if pics[i][3] in (0, 3):
            if i < len(pics) - 1:
                offsetx += pics[i][1] + xoffset

    if len(pics)>1:
        return CCC(pics, [pics[-1][1] + offsetx, height + 2 * yoffset], int(edge_border * width / (len(pics) - 1)))
    
    CCC(pics, [pics[-1][1] + offsetx, height + 2 * yoffset], int(edge_border * width))

def CCC(pics, dim, border):
    dim[0] += 2 * border
    collage = Image.new("RGB", dim, (255, 255, 255))
    for i in range(len(pics)):
        img = Image.open(pics[i][0])
        collage.paste(img, (pics[i][4] + border, pics[i][5]))
    collage.show()
    collage.save("collage" + str(int(time.time())) + ".jpg", quality=99)


main(5)
