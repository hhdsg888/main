import matplotlib.pyplot as plt

# ==============================
#   TAM / SAM / SOM 数据设置
# ==============================
TAM = 2000   # 2000+ 亿元
SAM = 400    # 350–450 亿元
SOM = 3      # 1–5 亿元

sizes = [TAM, SAM, SOM]

labels = [
    "TAM: Total Addressable Market\n(≈2000+ 亿元)",
    "SAM: Serviceable Available Market\n(≈350–450 亿元)",
    "SOM: Serviceable Obtainable Market\n(≈1–5 亿元)"
]

# ==============================
#        绘制论文风格三环图
# ==============================
plt.figure(figsize=(7,7))

# 外圈（TAM）
plt.pie([sizes[0]], radius=1.0, labels=None,
         wedgeprops=dict(width=0.3))

# 中圈（SAM）
plt.pie([sizes[1]], radius=0.7, labels=None,
         wedgeprops=dict(width=0.3))

# 内圈（SOM）
plt.pie([sizes[2]], radius=0.4, labels=None,
         wedgeprops=dict(width=0.3))

plt.gca().set(aspect="equal")

# ==============================
#          添加文本标签
# ==============================
plt.text(0, 1.05, labels[0], ha='center', va='center', fontsize=11)
plt.text(0, 0.35, labels[1], ha='center', va='center', fontsize=11)
plt.text(0, -0.35, labels[2], ha='center', va='center', fontsize=11)

plt.title("TAM / SAM / SOM Market Structure", fontsize=14)

plt.show()
