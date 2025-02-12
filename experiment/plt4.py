import matplotlib.pyplot as plt
import numpy as np

# 这两行代码使得 pyplot 画出的图形中可以显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 应用学术风格
# Solarize_Light2
# bmh
# classic
# grayscale
# seaborn-bright
# seaborn-darkgrid
plt.style.use('bmh')

# 4294967296
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151]
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
y1 = [b * 4 for b in x]
y2 = [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]
y3 = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,]
y4 = [4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 12, 12, 12, 12, 12, 16, 16, 16, 16, 16, 20, 20, 20, 20, 24, 24, 24, 24, 28, 28, 28]

# prime_prod = 1
# for x in primes:
#     if prime_prod * x > 2**32 - 1:
#         print(prime_prod, x)
#         prime_prod = x
#     else:
#         prime_prod = prime_prod * x
        
# 2, 3, 5, 7, 11, 13, 17, 19, 23 = 223092870 
# 29, 31, 37, 41, 43, 47 = 2756205443
# 53, 59, 61, 67, 71 = 907383479
# 73, 79, 83, 89, 97 = 4132280413
# 101, 103, 107, 109 = 121330189 
# 113, 127, 131, 137 = 257557397 
# 139, 149, 151 = 3127361

plt.plot(x, y1, label='P4Consist')
plt.plot(x, y2, label='2MVeri')
plt.plot(x, y3, label='P4Prime')
plt.plot(x, y4, label='P4Prime2')


plt.xlabel('The length of forwarding paths') 
plt.ylabel('Header OverHead(Bytes)')

# plt.title('Consistency check overhead of P4Prime and P4Consist \n under different verification cycles in fat tree with k=4') #设置图名为Simple Plot
plt.legend()

plt.show()


