import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    pulldata = open("data.txt", "r").read()
    dataarray = pulldata.split('\n')
    xar = []
    yar = []
    for eachLine in dataarray:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar, yar)
    #if len(xar) >= 2:
        #z = numpy.polyfit(xar, yar, 1)
        #p = numpy.poly1d(z)
        #plt.plot(xar, p(xar), "r--")
        #seg = 20
        #for i in range(len(yar)//seg):
            #z = numpy.polyfit(xar[i*seg:(i+1)*seg], yar[i*seg:(i+1)*seg], 1)
            #p = numpy.poly1d(z)
            #plt.plot(xar[i*seg:(i+1)*seg], p(xar[i*seg:(i+1)*seg]), "r--")


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
