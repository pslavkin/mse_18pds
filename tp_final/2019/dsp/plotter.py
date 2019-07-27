import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.figure import Figure
from matplotlib import rcParams

class plotter_class:

    def __init__(self,row,col):
        self.row=row
        self.col=col
        self.fig=plt.figure(figsize=( 10, 7))
        self.ax1=self.fig.add_subplot(row,col,1)
        plt.tight_layout(pad=4, w_pad=5, h_pad=6)
        plt.draw()

    def plot_signal(self, pos, x, y, title, xLabel, yLabel, about='',trace='.',center=0,zoom=0):
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

    def stem_signal(self, pos, x, y, title, xLabel, yLabel, about='',trace='.',center=0,zoom=0):
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

    def plot_show(self):
        plt.show()

    def plot_draw(self,pause):
        plt.draw()
        plt.pause(pause)

    def plot_close(self):
        plt.close()

    def zplane(self,b,a,pos):
        """Plot the complex z-plane given a transfer function.
        """

        # get a figure/plot
        #ax = plt.subplot(111)
        ax=self.fig.add_subplot(self.row,self.col,pos)

        # create the unit circle
        uc = patches.Circle((0,0), radius=1, fill=False,
                color='black', ls='dashed')
        ax.add_patch(uc)

        # The coefficients are less than 1, normalize the coeficients
        if np.max(b) > 1:
            kn = np.max(b)
            b = b/float(kn)
        else:
            kn = 1

        if np.max(a) > 1:
            kd = np.max(a)
            a = a/float(kd)
        else:
            kd = 1

        # Get the poles and zeros
        p = np.roots(a)
        z = np.roots(b)
        k = kn/float(kd)

        # Plot the zeros and set marker properties    
        t1 = plt.plot(z.real, z.imag, 'go', ms=10)
        plt.setp( t1, markersize=10.0, markeredgewidth=1.0,
                markeredgecolor='k', markerfacecolor='g')

        # Plot the poles and set marker properties
        t2 = plt.plot(p.real, p.imag, 'rx', ms=10)
        plt.setp( t2, markersize=12.0, markeredgewidth=3.0,
                markeredgecolor='r', markerfacecolor='r')

        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('center')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # set the ticks
        r = 1.5; plt.axis('scaled'); plt.axis([-r, r, -r, r])
        ticks = [-1, -.5, .5, 1]; plt.xticks(ticks); plt.yticks(ticks)
        float_formatter2 = lambda x: f"{x:.2f}"
        np.set_printoptions(formatter={'float_kind':float_formatter2})

         
        ax.set_title(f"polos={p}  \nZreal={z.real}\nZima={z.imag}")

        return z, p, k

