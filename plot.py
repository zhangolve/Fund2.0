import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

color_list =['b','g','r','c','m','y','k', '#FFC2EB', '#99FFC4', '#CFFF99', '#FFF7B3', '#FFE5B3', '#FFD1AD', '#FFB299', '#EBC2FF', '#A8C9FF', '#B3FFFA'];


def write_plot(data, attachment):    
    plt.figure(figsize=(15, 8), dpi=80)
    my_font = font_manager.FontProperties(fname="./msyhl.ttc")
    for idx, jijin in enumerate(data):
        plt.plot(range(1,21), jijin.get('data'), label=jijin.get('label'),color=color_list[idx])
    #设置x,y坐标
    # 0, 20
    # y轴最大最小值为盈亏百分比
    plt.xticks(range(1,21))
    plt.yticks(range(-10,10))
    #设置网格线
    plt.grid(alpha=0.2)
    plt.legend(prop=my_font, loc="upper left")
    plt.title('收益折线图',fontproperties=my_font)
    plt.show()
    plt.savefig(attachment)