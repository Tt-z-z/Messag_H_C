import random

def random_list(length, start=1, end=100):
    if end - start + 1 < length:
        raise ValueError("范围不足以生成不重复的随机数")
    return random.sample(range(start, end+1), length)

# 示例
random_list =  random.sample(range(0, 8), 8)
print(random_list)  # 输出类似：[2, 5, 1, 8, 3, 7, 6, 4]