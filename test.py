import matplotlib.pyplot as plt

plt.rcParams["font.family"] = 'Arial Unicode MS'
fig, ax = plt.subplots(figsize=(10, 6))
labels = ['新多', '多换', '空平', '多平', '空换', '新空']
colors = ['#FF0000', '#FF6666', '#FF6600', '#66FFFF', '#66FF99', '#66FF00']
wedges, texts, autotexts = ax.pie(
    [3, 4, 5, 2, 3, 4],
    labels=labels,
    startangle=90,
    autopct='%.2f%%',
    wedgeprops={'width': 0.3},
    labeldistance=1.15,
    colors=colors
)
ax.set_title('多空对阵', size=20)
ax.legend(
    wedges,
    labels,
    title='阵营',
    loc="center left",
    bbox_to_anchor=(1, 0.5, 0.5, 0.5),
    fontsize=14
)
plt.setp(texts, size=15)
plt.setp(autotexts, size=14)
plt.show()

