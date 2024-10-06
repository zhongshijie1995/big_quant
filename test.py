import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 8))
colors = ['#ff9999', '#66b3ff']
wedges, texts, autotexts = ax.pie(
    [20, 30],
    labels=['多', '空'],
    startangle=90,
    autopct='%1.1f%%',
    wedgeprops={'width': 0.5},
    labeldistance=1.15,
    colors=colors,
)

plt.legend(
    wedges,
    texts,
    loc='center left',
    bbox_to_anchor=(1, 0.5),
)

plt.setp(texts, fontsize=15)
plt.setp(autotexts, fontsize=14)
plt.show()
