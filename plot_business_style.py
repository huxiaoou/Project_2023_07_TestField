import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

test_dict = {'x': [0, 5, 10, 15, 20, 25, 30], 'year': ['1990', '1995', '2000', '2005', '2010', '2015', '2020']}
artist_04 = pd.DataFrame(test_dict)

color = ("#F5A34D", "#F26F77", "#48AEBA", "#A3BA74", "#958298", "#B88357", '#608CB1')
data = artist_04['x'].to_list()
data_color = dict(zip(data, color))

fig, ax = plt.subplots(figsize=(8, 4), dpi=200, facecolor='#FFF7F2', edgecolor='#FFF7F2')
ax.set_facecolor('#FFF7F2')
# 绘制中间横线
ax.set_ylim(-.5, 1.5)
# 绘制具有端点形状的直线
ax.plot([-3, 38], [.5, .5], "-o", lw=1.2, color='gray', markerfacecolor="w", mec='gray', ms=5,
        markeredgewidth=1., zorder=1)

# 分上下情况绘制点、线混合图形
for x in [0, 10, 20, 30]:
    # 绘制横线上的散点，颜色不同
    ax.scatter(x, .5, s=120, color=data_color[x], zorder=2)
    # 绘制叠加在颜色散点之上的散点，颜色为白色
    ax.scatter(x, .5, s=50, zorder=3, color='white')
    # 绘制散点和圆柱之间的连接线，端点为圆点
    ax.plot([x, x], [.5, .5 + .6], "-o", color=data_color[x], lw=.6, mfc="w", ms=5, mew=1.2, zorder=3)
    # 绘制横置圆柱图
    ax.plot([x, x + 7.5], [.5 + .6, .5 + .6], lw=15, color=data_color[x], solid_capstyle='round', zorder=1)
    ax.scatter(x, .5 + .6, s=80, zorder=3, color='white')
    ax.text(x + 4, .5 + .6, s='Lorem Ipsum', color='white', fontsize=7.5, fontweight='semibold', ha='center',
            va='center')
    # 添加年份
    ax.text(x - 1.4, .5 + .2, s=artist_04.loc[artist_04['x'] == x, 'year'].values[0], color='#686866', fontsize=12,
            fontweight='bold', rotation=90)

    # 添加描述文字
    ax.text(x + .5, .5 + .3, 'Optionally, the text can bedisplayed\n in anotherpositionxytext.Anarrow\npointingfrom the text totheannotated\npoint xy canthen beaddedbydefining\narrowprops.',
            ha='left', va='center', fontsize=4, color='gray')

for x in [5, 15, 25]:
    # 绘制横线上的散点，颜色不同
    ax.scatter(x, .5, s=120, color=data_color[x], zorder=2)
    # 绘制叠加在颜色散点之上的散点，颜色为白色
    ax.scatter(x, .5, s=50, zorder=3, color='white')
    # 绘制散点和圆柱之间的连接线，端点为圆点
    ax.plot([x, x], [.5, .5 - .6], "-o", color=data_color[x], lw=.6, mfc="w", ms=5, mew=1.2, zorder=3)
    # 绘制横置圆柱图
    ax.plot([x, x + 7.5], [.5 - .6, .5 - .6], lw=15, color=data_color[x], solid_capstyle='round', zorder=1)
    ax.scatter(x, .5 - .6, s=80, zorder=3, color='white')
    ax.text(x + 4, .5 - .6, s='Lorem Ipsum', color='white', fontsize=7.5, fontweight='semibold', ha='center',
            va='center')
    # 添加描述文字
    ax.text(x + .5, .5 - .3, 'Optionally, the text can bedisplayed\n in anotherpositionxytext.Anarrow\npointingfrom the text totheannotated\npoint xy canthen beaddedbydefining\narrowprops.',
            ha='left', va='center', fontsize=4, color='gray')
    # 添加年份
    ax.text(x - 1.4, .5 - .4, s=artist_04.loc[artist_04['x'] == x, 'year'].values[0], color='#686866', fontsize=12,
            fontweight='bold', rotation=90)

# 添加题目文本
ax.axis('off')
ax.text(.49, 1.15, '\nTIMELINE INFOGRAPHICS', transform=ax.transAxes,
        ha='center', va='center', fontsize=20, color='gray', fontweight='light')
ax.text(.92, .00, '\nVisualization by DataCharm', transform=ax.transAxes,
        ha='center', va='center', fontsize=5, color='black')
plt.savefig('artist_04.png', # width=8, height=4,
            dpi=900, bbox_inches='tight', facecolor='#FFF7F2')
