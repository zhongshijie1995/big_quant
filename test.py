import matplotlib.pyplot as plt

plt.rcParams["font.family"] = 'Arial Unicode MS'
fig, ax = plt.subplots(figsize=(10, 6))
labels = ['新多', '多持', '多平', '新空', '空持', '空平']
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ffa3a3', '#ffb3a3']
wedges, texts, autotexts = ax.pie(
    [3, 4, 5, 2, 3, 4],
    labels=labels,
    startangle=90, autopct='%.2f%%',
    wedgeprops={'width': 0.3}, labeldistance=1.15,
    colors=colors
)
ax.set_title('多空对阵', size=20)
ax.legend(
    wedges, labels,
    title='阵营',
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=14
)
plt.setp(texts, size=15)
plt.setp(autotexts, size=14)
plt.show()
