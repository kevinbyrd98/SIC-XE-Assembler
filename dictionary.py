#made by Jon Lemos 2/11/2019
thing = [s.split() for s in open('juice.txt', 'r')]
print("{")
for t in thing:
    print("\t\"" + t[0] + "\": [0x" + t[1] + ", " + t[2] + "],")
print("}")