import matplotlib.pyplot as plt
from eir_visualize import EvyonStyle

class GalvanoStatic():
    def __init__(self, title = "Galvanostatic", style = None):
        if style:
            if style == "Evyon":
                self.fig, self.ax = EvyonStyle().__enter__()
        else:
            self.fig, self.ax = plt.subplots(nrows = 1, ncols = 1)
        #self.fig.suptitle(suptitle) # This is figure title, not axis
        self.ax.set(
            title = title,
            #ylabel = 'Potential [V]',
            #xlabel = 'Specific Capacity [mAh]',
            #ylim = (2.5,5),
            #xlim = (0, 150),
            #xticks = (np.arange(0, 150), step=20)),
            #yticks = (np.arange(3, 5, step=0.2)),
        )
        self.fig.tight_layout()
        self.twinx = None

    def get_twinx(self):
        if not self.twinx:
            self.twinx = self.ax.twinx()
            return self.twinx
        else:
            return self.twinx

    def add_scatter(self, x, y1, y2 = None, labely1 = None, labely2= None):
        dotsize = 2
        # Plot data
        for i, (x, y1) in enumerate(zip(x, y1)):
            self.ax.scatter(x, y1, label = labely1 if labely1 else i, s = dotsize)
            if y2:
                self.get_twinx().scatter(x, y2, label = labely2 if labely2 else i, s = dotsize)


    def set_x(self, xlabel = 'Specific Capacity [mAh]'):
        self.ax.set_xlabel(xlabel)

    def set_y(self, ylabel = 'Potential [V]'):
        self.ax.set_ylabel(ylabel)

    def save(self, filename = None, format = "svg"):
        format = format.strip(".")
        if filename and not filename.endswith(f".{format}"):
            filename += "." + format
        plt.savefig(filename if filename else f"plot.{format}", dpi=300, bbox_inches="tight", format=format)
        
    def plot(self):
        plt.legend()
        plt.show()