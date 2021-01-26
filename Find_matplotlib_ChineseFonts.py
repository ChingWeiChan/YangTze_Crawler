
'''
This is the file which can print the fonts in matplotlib library.
And solve the Chinese Fonts cannot appear normally in plot.
You need to Download the Chinese fonts.
Step 1:
Download the file to /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/matplotlib/mpl-data/fonts/ttf

Step 2:
Go to /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/matplotlib/mpl-data/matplotlibrc 
and edit it.
    Remove the "#" in front of font.family
    Remove the "#" in front of font.sans-serif and add the font name(Ex: Noto Sans CJK TC)
    Save file.

Step 3:
    delete the caches file ~/.matplotlib/fontlist-vxxx.json.

Step 4:
    Reload Ipython.
'''
from matplotlib.font_manager import FontManager
fm = FontManager()
mat_fonts = set(f.name for f in fm.ttflist)
print(mat_fonts)