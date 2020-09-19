#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML

def plot_orbit(orb, ax):
    xs = np.asarray(orb.star_pos)[:,0]
    ys = np.asarray(orb.star_pos)[:,1]

    xp = np.asarray(orb.plan_pos)[:,0]
    yp = np.asarray(orb.plan_pos)[:,1]

    #ax.plot(xp, yp, marker='o', ls='None', ms=0.1)
    #ax.plot(xs, ys, marker='o', ls='None')
    return ax.plot(np.concatenate((xp, xs)),
                   np.concatenate((yp, ys)),
                   marker='o', ms=20,
                   ls='None')

    #plt.show()

class Anim():
    def __init__(self, orb):
        self.xs = np.asarray(orb.star_pos)[:,0]
        self.ys = np.asarray(orb.star_pos)[:,1]

        self.xp = np.asarray(orb.plan_pos)[:,0]
        self.yp = np.asarray(orb.plan_pos)[:,1]

    def show(self, fig, ax, plot_p, plot_s):
        self.linep = plot_p
        self.lines = plot_s

        self.linep.set_data(self.xp, self.yp)
        self.lines.set_data(self.xs, self.ys)
        ax.relim()
        ax.autoscale()

        #fig = plt.figure(figsize=(6,6))
        #ax = plt.gca()
        #ax.axis('equal')

        #self.linep, = ax.plot(self.xp, self.yp,
        #                      marker='o', ms=20, color='green',
        #                      ls='None')
        #ax.set_xlabel(r'$x$', fontsize=20)
        #ax.set_ylabel(r'$y$', fontsize=20)

        #self.lines, = ax.plot(self.xs, self.ys,
        #                      marker='$\star$', ms=20, color='orange',
        #                      ls='None')

        #plt.tight_layout()

        self.anim = animation.FuncAnimation(fig, self.animate,
                                            init_func = self.init,
                                            frames = len(self.xp),
                                            repeat=True,
                                            interval=20, blit=True)

        #plt.close('all')
        return HTML(self.anim.to_jshtml())
        #return self.anim

    def init(self):
        #self.line.set_data([self.xp[0], self.xs[0]],
        #                   [self.yp[0], self.ys[0]])
        self.linep.set_data([self.xp[0]],[self.yp[0]])
        self.lines.set_data([self.xs[0]],[self.ys[0]])
        return (self.linep,)

    def animate(self, i):
        #self.line.set_data([self.xp[i], self.xs[i]],
        #                   [self.yp[i], self.ys[i]])
        self.linep.set_data([self.xp[i]],[self.yp[i]])
        self.lines.set_data([self.xs[i]],[self.ys[i]])
        return (self.linep,)
