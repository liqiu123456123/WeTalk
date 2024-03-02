import numpy as np
import ast

a = "[0.06466158 -0.05744882 -0.18802193 -0.04693305  0.07074973 -0.06571367  0.09510736  0.05574648]"
# 去掉开头和结尾的方括号
a = a[1:-1]

# 使用split方法按空格分割字符串
list_data = a.split()

# 将列表转换为NumPy数组
np_array = np.array(list_data, dtype=float)

print(np_array)