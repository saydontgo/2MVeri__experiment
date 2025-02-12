import matplotlib.pyplot as plt
import numpy as np

# 这两行代码使得 pyplot 画出的图形中可以显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 应用学术风格
plt.style.use('seaborn')

# x = [200, 240, 300, 370, 400]
# y = np.array([0.1, 0.3, 0.5, 0.8, 1])

# x1 = [220, 270, 350, 410, 500]
# y1 = np.array([0.1, 0.2, 0.4, 0.7, 1])

# x2 = [250, 360, 460, 550, 600]
# y2 = np.array([0.1, 0.3, 0.55, 0.85, 1])

x = [200, 240, 300, 370, 405]
y = np.array([0.1, 0.3, 0.5, 0.8, 1])

# x1 = [220, 270, 350, 410, 498]
# y1 = np.array([0.1, 0.27, 0.45, 0.73, 1])

x2 = [250, 300, 377, 460, 556]
y2 = np.array([0.1, 0.25, 0.46, 0.70, 1])


plt.step(x, y, where='pre', label='P4Prime')
# plt.step(x1, y1, where='pre', label='P4Consist')
plt.step(x2, y2, where='pre', label='2MVeri')

x_ticks = np.arange(0, 600, 100)
plt.xticks(x_ticks)

plt.xlabel('Detection Times(ms)') 
plt.ylabel('CDF') 

plt.tight_layout()
plt.legend() 
plt.show()


