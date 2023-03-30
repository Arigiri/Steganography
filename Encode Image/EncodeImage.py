import cv2
import numpy as np
import os
class Image:
    def __init__(self, name : str) -> None:
        self.Image = cv2.imread(name)
        colors = cv2.split(self.Image)
        self.b, self.g, self.r = colors
        pass
    
def ShowBin(BinList, Img : Image, BitEncode):
    r = Img.r
    g = Img.g
    b = Img.b
    idx = 0
    for col in range(r.shape[0]):
        for row in range(r.shape[1]):
            if idx > len(BinList):
                break
            newr = BinList[idx][0] + "0" * (8 - BitEncode)
            newg = BinList[idx][1] + "0" * (8 - BitEncode)
            newb = BinList[idx][2] + "0" * (8 - BitEncode)
            idx += 1
            r[col][row] = int(newr, 2)
            g[col][row] = int(newg, 2)
            b[col][row] = int(newb, 2)
    img = cv2.merge((b, g, r))
    return img


def FormatBin(Bin : str):
    result = ""
    if len(Bin) == 0:
        return Bin
    Bin = Bin[1:]
    for char in Bin:
        if char != 'b':
            result += char
    while len(result) < 8:
        result = '0' + result
    return result

def FormatBinMore8Bit(Bin : str):
    bit = len(Bin) // 8
    result = ""
    for char in Bin:
        if char != 'b':
            result += char
    if len(Bin) % 8 != 0:
        bit += 1
    while len(result) < 8 * bit:
        result = '0' + result
    # print(result)
    return result



def EncodeImage(imgA : Image, imgB : Image, BitEncode : int): #Hide ImageB in ImageA
    BinList = []
    ShapeNeedEncode = imgB.r.shape
    for col in range(imgB.r.shape[0]):
        for row in range(imgB.r.shape[1]):
            r = imgB.r[col][row]
            g = imgB.g[col][row]
            b = imgB.b[col][row]
            rbin = FormatBin(bin(r))[0:BitEncode]
            gbin = FormatBin(bin(g))[0:BitEncode]
            bbin = FormatBin(bin(b))[0:BitEncode]
            BinList.append((rbin, gbin, bbin))
    #Check for decoded picture after encode
    temp = ShowBin(BinList, imgB, BitEncode)  
    cv2.imwrite("TempDecode.png", temp)
    #Encode the entire image
    idx = 0
    for col in range(imgA.r.shape[0]):
        for row in range(imgA.r.shape[1]):
            r = imgA.r[col][row]
            g = imgA.g[col][row]
            b = imgA.b[col][row]

            if idx >= len(BinList):
                break
            rbin = FormatBin(bin(r))[:8 - BitEncode] + BinList[idx][0]
            gbin = FormatBin(bin(g))[:8 - BitEncode] + BinList[idx][1]
            bbin = FormatBin(bin(b))[:8 - BitEncode] + BinList[idx][2]

            idx += 1
            r = int(rbin, 2)
            g = int(gbin, 2)
            b = int(bbin, 2)

            imgA.r[col][row] = r
            imgA.g[col][row] = g
            imgA.b[col][row] = b
    #Encode the shape of the image
    BitEncode += 1
    Bin0 = FormatBinMore8Bit(bin(ShapeNeedEncode[0]))
    Bin1 = FormatBinMore8Bit(bin(ShapeNeedEncode[1]))
    BinList = Bin0 + Bin1
    BinList = FormatBin(bin(len(Bin0 + Bin1))) + BinList

    idx = 0
    
    for col in range(imgA.r.shape[0]):
        for row in range(imgA.r.shape[1]):
            r = imgA.r[col][row]
            g = imgA.g[col][row]
            b = imgA.b[col][row]
            if idx >= len(BinList):
                break
            rbin = FormatBin(bin(r))
            gbin = FormatBin(bin(g))
            bbin = FormatBin(bin(b))
            
            if idx >= len(BinList):
                break
            rbin = rbin[:8 - BitEncode] + BinList[idx] + rbin[8 - BitEncode + 1:]
            r = int(rbin, 2)
            imgA.r[col][row] = r
            idx += 1
            if idx >= len(BinList):
                break
            gbin = gbin[:8 - BitEncode] + BinList[idx] + gbin[8 - BitEncode + 1:]
            g = int(gbin, 2)
            imgA.g[col][row] = g
            idx += 1
            if idx >= len(BinList):
                break
            bbin = bbin[:8 - BitEncode] + BinList[idx] + bbin[8 - BitEncode + 1:]
            b = int(bbin, 2)
            imgA.b[col][row] = b
            idx += 1
            if idx >= len(BinList):
                break

            r = int(rbin, 2)
            g = int(gbin, 2)
            b = int(bbin, 2)
            
            imgA.r[col][row] = r
            imgA.g[col][row] = g
            imgA.b[col][row] = b
    imgA.Image = cv2.merge((imgA.b, imgA.g, imgA.r))
    return imgA.Image

orginalImage = Image('wibu.jpg')
HiddenImage = Image('colorful.jpg')
if HiddenImage.Image.size > orginalImage.Image.size:
    print("Sorry I cant encode that")
result = EncodeImage(orginalImage, HiddenImage, 3)
cv2.imwrite("Result.png", result)