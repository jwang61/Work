import sys
import matplotlib.pyplot as plt

DELIM1 = ", "
DELIM2 = "], ["

def main():
    datafile = str(sys.argv[1])
    data = None
    plt.ion()
    fig, ax = plt.subplots(figsize = (6,6))
    with open(datafile, 'r') as file:
        data = [x.strip() for x in file.readlines()]
    
    print len(data)
    count = 1
    for matrix in data[:-1]:
        img = []
        rowSplit = matrix[2:-2].split(DELIM2)
        for row in rowSplit:
            img.append([int(x) for x in row.split(DELIM1)])
        ax.imshow(img, cmap = plt.cm.Reds, interpolation="none", extent=[-45,45,10,0.1])
        ax.set_aspect(10)
        if len(sys.argv) > 2:
            plt.savefig("image{0:04d}.png".format(count))
        else:
            plt.draw()
            plt.pause(0.1)
        count+= 1
    while True:
        plt.pause(0.5)
            

if __name__ == '__main__':
    main()
