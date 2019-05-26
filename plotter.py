import matplotlib.pyplot as plt
import  numpy as np

class plotter_class:

    def __init__(self,row,col):
        self.row=row
        self.col=col
        self.fig=plt.figure(figsize=( 10, 7))
        self.ax1=self.fig.add_subplot(row,col,1)
        plt.tight_layout(pad=4, w_pad=5, h_pad=6)
        plt.draw()

    def spaceX(self, y):
        return np.linspace(0,y.size-1,y.size)

    def plot_signal(self, pos=1, x=1, y=1, title="", xLabel="", yLabel="", about='',trace='.',center=0,zoom=0):
        ax=self.fig.add_subplot(self.row,self.col,pos)
        N      = len(x)
        zoom   = int(zoom)
        center = int(center)
        if zoom!=0:
            zoom_min=center-zoom
            if zoom_min<0:
                zoom_min=0
            zoom_max=center+zoom
            if zoom_max>N:
                zoom_max=N
        else:
            zoom_max=N
            zoom_min=0
        line, =ax.plot(x[zoom_min:zoom_max],y[zoom_min:zoom_max],trace, label=about)

        ax.set_title(title)
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        ax.grid(which='both', axis='both')
        if about != '':
            ax.legend(loc='best')
        plt.draw()

    def stem_signal(self, pos, x, y, title, xLabel="", yLabel="", about='',trace='.',center=0,zoom=0):
        ax=self.fig.add_subplot(self.row,self.col,pos)
        N      = len(x)
        zoom   = int(zoom)
        center = int(center)
        if zoom!=0:
            zoom_min=center-zoom
            if zoom_min<0:
                zoom_min=0
            zoom_max=center+zoom
            if zoom_max>N:
                zoom_max=N
        else:
            zoom_max=N
            zoom_min=0
        line, =ax.plot(x[zoom_min:zoom_max],y[zoom_min:zoom_max],trace, label=about)
        ax.set_title(title)
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        ax.grid(which='both', axis='both')
        if about != '':
            ax.legend(loc='best')
        plt.stem(x[zoom_min:zoom_max],y[zoom_min:zoom_max])
        plt.draw()

    def plot_hist(self, pos=1, x=1, y=1, title="", xLabel="", yLabel="", about='',trace='.'):
        ax=self.fig.add_subplot(self.row,self.col,pos)
        plt.hist(x,y)
        ax.set_title(title)
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        ax.grid(which='both', axis='both')
        if about != '':
            ax.legend(loc='best')
        plt.draw()

    def plot_show(self):
        plt.show()

    def plot_draw(self,pause):
        plt.draw()
        plt.pause(pause)

    def plot_close(self):
        plt.close()


