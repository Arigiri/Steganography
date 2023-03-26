import cv2
import numpy as np

class Image:
    def __init__(self, name : str) -> None:
        self.Image = cv2.imread(name)
        self.Image -= np.ones(self.Image.shape, dtype = np.uint8)
        self.b, self.g, self.r = cv2.split(self.Image)
        pass
    
    def Read(self):
        f = open("EncodeText.txt", 'r')
        EncodeString = f.readline()
        f.close()
        f = open("EncodeType.txt", 'r')
        EncodeType = f.readline()
        self.Encode(EncodeString, EncodeType)
    
    def ComPare(self, listA, listB):
        for i in range(len(listA)):
            if listA[i] != listB[i]:
                print(i, listA[i], listB[i])
    
    def AddToString(self, StringAdd, charToAdd):
        string = ''.join(bin(ord(charToAdd)))
        if len(string) == 8:
            string = string[0:2] + "0" + string[2:]
        StringAdd += string
        return StringAdd
    
    def BinEncode(self, text : str):
        amount = str(len(text))
        BinList = ""
        print(amount)
        for char in amount:
            BinList = self.AddToString(BinList, char)
        BinList = self.AddToString(BinList, ' ')
        for char in text:
            BinList = self.AddToString(BinList, char)
        currIndex = 0
        print(BinList[8:16])
        for i in range(self.r.shape[0]):
            for j in range(self.r.shape[1]):
                r = self.r[i][j]
                g = self.g[i][j]
                b = self.b[i][j]
                rbin = bin(r)
                gbin = bin(g)
                bbin = bin(b)
                try:
                    charBin = BinList[currIndex]
                    if charBin == 'b':
                        # 
                        currIndex += 1
                    if rbin[-1] != BinList[currIndex]:
                        r += 1
                    currIndex += 1
                    charBin = BinList[currIndex]
                    if charBin == 'b':
                        # 
                        currIndex += 1
                    if gbin[-1] != BinList[currIndex]:
                        g += 1
                    currIndex += 1
                    charBin = BinList[currIndex]
                    if charBin == 'b':
                        # 
                        currIndex += 1
                    if bbin[-1] != BinList[currIndex]:
                        b += 1
                    currIndex += 1
                    charBin = BinList[currIndex]
                    if charBin == 'b':
                        # 
                        currIndex += 1
                except:
                    self.r[i][j] = r
                    self.g[i][j] = g
                    self.b[i][j] = b
                    break
                self.r[i][j] = r
                self.g[i][j] = g
                self.b[i][j] = b
                
        self.Image = cv2.merge((self.b, self.g, self.r))

    def Encode(self, text : str, Etype : str) -> str:
        amount = len(text)
        if amount > (self.Image.size - len(str(amount)))*3 :
            print("Sorry I cant encode that")
            return
        if Etype.lower() == "bin":
            self.BinEncode(text)
            pass
        pass

img = Image('Wibu.jpg')
cv2.imshow("orginal", img.Image)
img.Read()
cv2.imshow("Secret", img.Image)
cv2.waitKey()
cv2.destroyAllWindows()
cv2.imwrite("Secret.png", img.Image)
