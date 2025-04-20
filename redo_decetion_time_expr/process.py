import matplotlib.pyplot as plt
import numpy as np

# 这两行代码使得 pyplot 画出的图形中可以显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 应用学术风格
# Solarize_Light2
# bmh
# classic
# seaborn-bright
# seaborn-darkgrid
plt.style.use('classic')

fig1, (ax1, ax2) = plt.subplots(figsize=(15, 6), nrows=1, ncols=2, sharex=False)

x1 = [2, 5, 27, 28, 34, 43, 53, 62, 84, 111]
y1 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
x3 = [250, 300, 377, 460, 556]
y3 = np.array([0.1, 0.25, 0.46, 0.77, 1])
x2 = [63, 85, 99, 134, 176, 185, 192, 251, 400, 576]
y2 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

ax1.step(x1, y1, where='pre', label='P4Prime')
ax1.step(x2, y2, where='pre', label='2MVeri')
ax1.step(x3, y3, where='pre', label='P4Consist')
x_ticks = np.arange(0, 500, 50)
ax1.set_xticks(x_ticks)

ax1.set_xlabel('Detection Times(ms)') 
ax1.set_ylabel('CDF') 
ax1.set_title('Detection Cycle(ms): T = 10ms')
ax1.legend(loc="lower right")

x1 = [18, 22, 45, 45, 48, 56, 74, 77, 83, 123]
y1 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
x2 = [111, 182, 246, 267, 312, 323, 361, 504, 540, 708]
y2 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
x3 = [710, 855, 960, 1090, 1210]
y3 = np.array([0.1, 0.29, 0.52, 0.81, 1])

ax2.step(x1, y1, where='pre', label='P4Prime')
ax2.step(x2, y2, where='pre', label='2MVeri')
ax2.step(x3, y3, where='pre', label='P4Consist')
x_ticks = np.arange(0, 1300, 100)
ax2.set_xticks(x_ticks)

ax2.set_xlabel('Detection Times(ms)') 
ax2.set_ylabel('CDF') 
ax2.set_title('Detection Cycle(ms): T = 20ms')
ax2.legend()


plt.tight_layout()
plt.legend(loc="lower right") 
# plt.show()

plt.savefig('redo_test.png')
# 




