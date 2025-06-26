import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Caminho para a fonte TTF
font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
times_new_roman = FontProperties(fname=font_path)

plt.figure()
plt.title("Testando Times New Roman", fontproperties=times_new_roman, fontsize=16)
plt.xlabel("Eixo X", fontproperties=times_new_roman, fontsize=12)
plt.ylabel("Eixo Y", fontproperties=times_new_roman, fontsize=12)
plt.plot([1, 2, 3], [4, 1, 7], 'o-')
plt.grid(True)
plt.show()
