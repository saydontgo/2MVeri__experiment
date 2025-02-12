import matplotlib.pyplot as plt
import numpy as np

# 这两行代码使得 pyplot 画出的图形中可以显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig1, (ax1, ax2, ax3) = plt.subplots(figsize=(15, 6), nrows=1, ncols=3, sharex=True)
x = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

bandwidth1= int(1000 * 1400 * 8 / 34000) 
y1 = [5820, 3100, 2160, 1660, 1340, 1100, 960, 860, 760, 680]
y1 = [t/34 for t in y1]
y2 = [1200, 640, 432, 332, 260, 224, 196, 168, 152, 136]
y2 = [t/34 for t in y2]
ax1.plot(x, y1, label='P4Consist')
ax1.plot(x, y2, label='P4Prime')
ax1.set_xlabel('Detection Cycle(s)') 
ax1.set_ylabel('Check Overhead(B/s)') 
ax1.set_title('Network Throughput:'+ str(bandwidth1) + 'kb/s')
ax1.legend()

bandwidth2= int(4000 * 1400 * 8/ 34000) 
y3 = [20752, 11640, 7888, 6304, 4968, 4032, 3456, 3036, 2736, 2520]
y3 = [t/34 for t in y3]
y4 = [4716, 2552, 1772, 1368, 1048, 896, 788, 672, 584, 560]
y4 = [t/34 for t in y4]
ax2.plot(x, y3, label='P4Consist')
ax2.plot(x, y4, label='P4Prime')
ax2.set_xlabel('Detection Cycle(s)') 
ax2.set_ylabel('Check Overhead(B/s)') 
ax2.set_title('Network Throughput:'+ str(bandwidth2) + 'kb/s')
ax2.legend()

bandwidth3= int(7000 * 1400 * 8/ 34000) 
y5 = [35716, 21496, 15120, 11566, 8896, 7656, 6660, 5940, 5036, 4620]
y5 = [t/34 for t in y5]
y6 = [8312, 4456, 3348, 2420, 2028, 1916, 1644, 1420, 1208, 948]
y6 = [t/34 for t in y6]
ax3.plot(x, y5, label='P4Consist')
ax3.plot(x, y6, label='P4Prime')
ax3.set_xlabel('Detection Cycle(s)') 
ax3.set_ylabel('Check Overhead(B/s)') 
ax3.set_title('Network Throughput:'+ str(bandwidth3) + 'kb/s')
ax3.legend()


plt.tight_layout()
plt.legend() 
plt.show()


# sends1 = int(1000 / 34)
# sends2 = int(7000 / 37)

# y1 = [5820, 3100, 2160, 1640, 1320, 1100, 940, 840, 740, 640]
# y1 = [t/34 for t in y1]
# plt.plot(x, y1, label='P4Consist-' + str(sends1) + 'pkt/s')

# y2 = [1180, 636, 444, 332, 268, 220, 196, 172, 148, 136]
# y2 = [t/34 for t in y2]
# plt.plot(x, y2, label='P4Prime-' + str(sends1) + 'pkt/s')

# y3 = [36548, 20128, 15364, 11628, 9080, 7240, 6448, 5788, 4864, 4356]
# y3 = [t/37 for t in y3]
# plt.plot(x, y3, label='P4Consist-' + str(sends2) + 'pkt/s')

# y4 = [7660, 4336, 3180, 2260, 1964, 1600, 1364, 1144, 976, 876]
# y4 = [t/37 for t in y4]
# plt.plot(x, y4, label='P4Prime-' + str(sends2) + 'pkt/s')


# plt.xlabel('Detection Cycle(s)') #设置x轴名称 x label
# plt.ylabel('Check Overhead(Bps)') #设置y轴名称 y label
# # plt.title('Consistency check overhead of P4Prime and P4Consist \n under different verification cycles in fat tree with k=4') #设置图名为Simple Plot
# plt.legend() #自动检测要在图例中显示的元素，并且显示

# plt.show() #图形可视化
