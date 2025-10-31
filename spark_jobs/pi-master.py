from pyspark import SparkContext
import random

# 启动 Spark 上下文
sc = SparkContext("spark://10.0.0.6:7077", "DistributedPi")

# 总样本数（比如 1 亿个点）
N = 100_000_000
num_partitions = 12  # 划分任务数

def inside(_):
    """单个样本是否在圆内"""
    x, y = random.random(), random.random()
    return 1 if x*x + y*y <= 1 else 0

# RDD 并行计算（每个 Worker 处理一部分）
count = sc.parallelize(range(N), numSlices=num_partitions) \
           .map(inside) \
           .reduce(lambda a, b: a + b)

pi_est = 4.0 * count / N

print(f"✅ Estimated Pi = {pi_est}")
sc.stop()