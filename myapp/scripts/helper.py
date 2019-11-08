from bokeh.palettes import Category20_20

def getKColors(k):
    k_color_list = []
    for i in range(k):
        k_color_list.append(Category20_20[i % 20])

    return k_color_list
