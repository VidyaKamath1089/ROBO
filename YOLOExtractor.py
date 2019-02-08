import os
import glob
import cv2
import numpy as np

imgPath = "E:/RoboCup/YOLO/Train/"
labelPath = "E:/RoboCup/YOLO/Masks/Train/"

labelDict = {}
legendDict = {}


def loadLabelConfig():
    """
    Reads LabelConfig.txt to dictionary
    """
    with open(labelPath + "LabelConfig.cfg") as file:
        data = file.readlines()
        data = [x.replace("\n", "") for x in data]
        data = [x.split(":") for x in data]
        for i in data:
            labelDict[i[0]] = i[1]


def readLegendFile():
    """
    Loads the legend file generated by UETrainingSetGenerator into a
    dictionary structure
    """
    with open(labelPath + "segmentationLegend.leg", "r") as currFile:
        fileData = currFile.readline().split(" ")
        currLegendIndex = 0
        for i in fileData:
            i = i.split(":")
            if (len(i) < 2):  # catching occunring whitespaces at file endings
                continue

            currLegendIndex += int(i[0])
            legendDict[str(currLegendIndex)] = i[1]


def getTag(key):
    legendKeyArray = sorted(map(int, legendDict.keys()))
    for legendKey in legendKeyArray:
        if (key - 1 < legendKey):
            return (legendDict[str(legendKey)])


def getLabel(key):
    currTag = getTag(key)
    return (int(labelDict[currTag]))


def processMask(maskName, imageHeight = 480):
    """
    Processes given maskFile into 2d-array structure.
    """
    maskArray = []
    with open(labelPath + maskName, "r") as currFile:
        for i in range(imageHeight):  # 480
            # read line from segMaskFile
            currLineData = currFile.readline()
            # gather segNames from File
            currLineData = currLineData.split(" ")
            maskArray.append(currLineData[:-1])
    return maskArray

import re

def sorted_nicely( l ):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

if __name__ == "__main__":

    readLegendFile()
    loadLabelConfig()

    labels = sorted_nicely(glob.glob1(labelPath,"*.txt"))
    images = sorted_nicely(glob.glob1(imgPath,"*.png"))

    for i,(imageN,labelN) in enumerate(zip(images,labels)):
        print(i)
        label = np.array(processMask(labelN),'uint8')
        file = open(imgPath + imageN.split(".")[0] + ".txt","w+")
        for i in range(1,62):
            a = np.where(label == i)
            if a[0].size == 0 or a[1].size == 0:
                continue
            bbox = getLabel(i)-1, (np.max(a[1])+np.min(a[1]))/1280.0, (np.max(a[0])+np.min(a[0]))/960.0, \
                   (np.max(a[1])-np.min(a[1]))/640.0, (np.max(a[0])-np.min(a[0]))/480.0
            if bbox[0] < 0:
                continue
            if bbox[3] > 0.012 or bbox[4] > 0.015:
                for elem in bbox:
                    file.write(str(elem))
                    file.write(" ")
                file.write("\n")
        file.close()



