import cv2

class Image1:
    def __init__(self, name : str) -> None:
        self.Image = cv2.imread(name)
        
        self.b, self.g, self.r = cv2.split(self.Image)
        pass
    
    def DecodeBin(self):
        BinList = []
        BinString = ""
        for i in range(self.r.shape[0]):
            for j in range(self.r.shape[1]):
                r = self.r[i][j]
                g = self.g[i][j]
                b = self.b[i][j]
                if len(BinString) % 8 == 0 and len(BinString) != 0:
                    BinList.append(BinString)
                    BinString = ""
                BinString += bin(r)[-1]
                if len(BinString) % 8 == 0:
                    BinList.append(BinString)
                    BinString = ""
                BinString += bin(g)[-1]
                if len(BinString) % 8 == 0:
                    BinList.append(BinString)
                    BinString = ""
                BinString += bin(b)[-1]
                if len(BinString) % 8 == 0:
                    BinList.append(BinString)
                    BinString = ""

        Binaries = []
        BinString = ""
        index = 0
        for bins in BinList:
            try:
                st = str(bins)[0] 
                st += "b" + str(bins)[1:]
                b = int(st, 2)
                Binaries.append(b)
            except:
                pass

        Words = []
        for bins in Binaries:
            Words.append(chr(bins))
        
        num = ""
        for char in Words:
            if char == " ":
                break
            num += char
        Result = ""
        total = int(num) + len(str(num)) + 1
        for idx in range(total):
            Result += Words[idx]
        f = open("DecodeResult.txt", 'w')
        f.write(Result)
        f.close()
    def printColor(self, num):
        result = []
        for i in range(self.r.shape[0]):
            for j in range(self.r.shape[1]):
                r = bin(self.r[i][j])
                g = bin(self.g[i][j])
                b = bin(self.b[i][j])
                result.append((r, g, b))
        
        for i in range(num + 1):
            print (result[i])
        return result

img1 = Image1("Secret.png")
# print(img.g[0][0])
img1.DecodeBin()
# result1 = img1.printColor(19)
