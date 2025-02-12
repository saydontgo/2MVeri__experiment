import matplotlib.pyplot as plt
import numpy as np

# 这两行代码使得 pyplot 画出的图形中可以显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 应用学术风格
plt.style.use('ggplot')


x = [200, 400, 600, 800]
y = np.array([1/7, 3/7, 5/7,1])
x1 = [400, 600, 1000, 1400]
y1 = np.array([1/7, 4/7, 5/7, 1])
x2 = [800, 1400, 1600, 2000]
y2 = np.array([1/7, 4/7, 5/7, 1])



plt.step(x, y, label='Detection Cycle(s): 0.2s')
plt.step(x1, y1, label='Detection Cycle(s): 0.5s')
plt.step(x2, y2, label='Detection Cycle(s): 1.0s')

plt.xlabel('Detection Times(ms)') 
plt.ylabel('CDF') 



plt.tight_layout()
plt.legend() 
plt.show()


