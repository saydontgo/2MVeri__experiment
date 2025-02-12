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

fig1, (ax1, ax2) = plt.subplots(figsize=(15, 6), nrows=1, ncols=2, sharex=True)

x1 = [2.20, 2.40, 3.00, 3.70, 4.05]
y1 = np.array([0.1, 0.3, 0.5, 0.8, 1])
x2 = [2.50, 3.00, 3.77, 4.60, 5.56]
y2 = np.array([0.1, 0.25, 0.46, 0.77, 1])
x3 = [4.12, 4.90, 5.70, 6.44, 7.56]
y3 = np.array([0.1, 0.32, 0.48, 0.83, 1])

ax1.step(x1, y1, where='pre', label='P4Prime')
ax1.step(x2, y2, where='pre', label='2MVeri')
ax1.step(x3, y3, where='pre', label='P4Consist')
x_ticks = np.arange(0, 10, 1)
ax1.set_xticks(x_ticks)

ax1.set_xlabel('Detection Times(us)') 
ax1.set_ylabel('CDF') 
ax1.set_title('Detection Cycle(ms): T = 2us')
ax1.legend()

x1 = [4.80, 6.55, 7.56, 8.50, 9.80]
y1 = np.array([0.1, 0.3, 0.5, 0.8, 1])
x2 = [5.50, 6.88, 7.91, 8.90, 10.50]
y2 = np.array([0.1, 0.27, 0.48, 0.77, 1])
x3 = [7.10, 8.55, 9.60, 10.90, 12.10]
y3 = np.array([0.1, 0.29, 0.52, 0.81, 1])

ax2.step(x1, y1, where='pre', label='P4Prime')
ax2.step(x2, y2, where='pre', label='2MVeri')
ax2.step(x3, y3, where='pre', label='P4Consist')
x_ticks = np.arange(0, 15, 1)
ax2.set_xticks(x_ticks)

ax2.set_xlabel('Detection Times(us)') 
ax2.set_ylabel('CDF') 
ax2.set_title('Detection Cycle(ms): T = 5us')
ax2.legend()


plt.tight_layout()
plt.legend(loc="upper left") 
# plt.show()

plt.savefig('./experiment/experiment_7.png')
# 




