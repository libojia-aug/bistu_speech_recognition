# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
plt.figure(1) # 创建图表1
ax1 = plt.subplot(3, 4, 1) # 在图表2中创建子图1
ax2 = plt.subplot(3, 4, 2) # 
ax3 = plt.subplot(3, 4, 3) # 在图表2中创建子图2
ax4 = plt.subplot(3, 4, 4) # 在图表2中创建子图2
ax5 = plt.subplot(3, 4, 5) # 在图表2中创建子图2
ax6 = plt.subplot(3, 4, 6) # 在图表2中创建子图2
ax7 = plt.subplot(3, 4, 7) # 在图表2中创建子图2
ax8 = plt.subplot(3, 4, 8) # 在图表2中创建子图2
ax9 = plt.subplot(3, 4, 9) # 在图表2中创建子图2
ax10 = plt.subplot(3, 4, 10) # 在图表2中创建子图2
ax11 = plt.subplot(3, 4, 11) # 在图表2中创建子图2
ax12 = plt.subplot(3, 4, 12) # 在图表2中创建子图2
x = np.arange(6)

def sel(p, plt):
    fo = open(p, "r")
    all_the_text = fo.read()
    arr = all_the_text.splitlines()
    for i in range(len(arr)):
    # for i in range(4):
        plt.plot(x, arr[i].split(','))

p = './oi/na0t500d6/1.txt'
plt.sca(ax1)
sel(p, plt)

p = './oi/na0t500d6/2.txt'
plt.sca(ax2)
sel(p, plt)

p = './oi/na0t500d6/3.txt'
plt.sca(ax3)
sel(p, plt)

p = './oi/na0t500d6/4.txt'
plt.sca(ax4)
sel(p, plt)

p = './oi/na0t500d6/5.txt'
plt.sca(ax5)
sel(p, plt)

p = './oi/na0t500d6/6.txt'
plt.sca(ax6)
sel(p, plt)

p = './oi/na0t500d6/7.txt'
plt.sca(ax7)
sel(p, plt)

p = './oi/na0t500d6/8.txt'
plt.sca(ax8)
sel(p, plt)

p = './oi/na0t500d6/9.txt'
plt.sca(ax9)
sel(p, plt)

p = './oi/na0t500d6/10.txt'
plt.sca(ax10)
sel(p, plt)

p = './oi/na0t500d6/11.txt'
plt.sca(ax11)
sel(p, plt)

p = './oi/na0t500d6/12.txt'
plt.sca(ax12)
sel(p, plt)


# p = './oi/a0l/1.txt'
# fo = open(p, "r")
# all_the_text = fo.read()
# arr = all_the_text.splitlines()
# x = np.arange(250)

# for i in range(len(arr)):
#     pl.plot(x, arr[i].split(','))
plt.show()# show the plot on the screen
