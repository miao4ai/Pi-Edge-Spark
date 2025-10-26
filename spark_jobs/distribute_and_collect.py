from pyspark import SparkContext
import requests
import pandas as pd

# Edge worker 列表
EDGE_NODES = [
    {"name": "edge1", "url": "http://192.168.1.11:8000/read_data"},
    {"name": "edge2", "url": "http://192.168.1.12:8000/read_data"},
    {"name": "edge3", "url": "http://192.168.1.13:8000/read_data"},
]

sc = SparkContext("spark://192.168.1.10:7077", "EdgeDataCollector")

def fetch_from_edge(edge):
    try:
        res = requests.get(edge["url"], timeout=10)
        js = res.json()
        if "rows" not in js:
            return []
        return js["rows"]
    except Exception as e:
        print(f"⚠️ {edge['name']} error: {e}")
        return []

# 并行向所有 Edge 请求数据
rdd = sc.parallelize(EDGE_NODES)
all_data = rdd.flatMap(fetch_from_edge).collect()

sc.stop()

# 汇总成 DataFrame
df = pd.DataFrame(all_data)
print(f"✅ Received {len(df)} rows from {len(EDGE_NODES)} edge nodes")

# 保存为本地文件供后续分析
df.to_csv("data/combined/edge_merged.csv", index=False)

# 简单分析：平均温度、湿度
if not df.empty:
    summary = df.agg({
        "temperature": ["mean", "min", "max"],
        "humidity": ["mean", "min", "max"]
    })
    print("📊 Summary statistics:\n", summary)
