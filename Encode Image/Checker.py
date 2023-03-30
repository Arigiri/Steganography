f = open('temp.txt')
g = open('origin.txt')

a = "0010000000000001100110000000001001100100"
b = "0010000000000001100110000000001001100101"
print(a[:8])
print(a[8:16])
idx = 0
while True:
    a = f.readline().split()
    b = g.readline().split()
    if a != b:
        print("Impossible")
        print(a, b)
        print(idx)
        break
    idx += 1
    
# print(a[:4])