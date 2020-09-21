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

        self.anim = animation.FuncAnimation(fig, self.animate,
                                            init_func = self.init,
                                            frames = len(self.xp),
                                            repeat=True,
                                            interval=20, blit=True)

        return HTML(self.anim.to_jshtml())

    def init(self):
        self.linep.set_data([self.xp[0]],[self.yp[0]])
        self.lines.set_data([self.xs[0]],[self.ys[0]])
        return (self.linep,)

    def animate(self, i):
        self.linep.set_data([self.xp[i]],[self.yp[i]])
        self.lines.set_data([self.xs[i]],[self.ys[i]])
        return (self.linep,)

class AnimKep2():
    def __init__(self, orb):
        self.xs = np.asarray(orb.star_pos)[:,0]
        self.ys = np.asarray(orb.star_pos)[:,1]

        self.xp = np.asarray(orb.plan_pos)[:,0]
        self.yp = np.asarray(orb.plan_pos)[:,1]

    def show(self, fig, ax, coll, plot_p, plot_s, ndiff=10):
        self.coll = coll
        self.n = ndiff

        self.linep = plot_p
        self.lines = plot_s

        xp = np.append(self.xp, self.xp[0])
        yp = np.append(self.yp, self.yp[0])

        self.linep.set_data(xp, yp)
        self.lines.set_data(self.xs[0], self.ys[0])

        xsel = np.ravel(np.append(self.xp[0:ndiff],
                                  np.asarray([self.xs[0], self.xp[0]])))
        ysel = np.ravel(np.append(self.yp[0:ndiff],
                                  np.asarray([self.ys[0], self.yp[0]])))

        xy = np.transpose(np.asarray([xsel, ysel]))

        self.coll.set_xy(xy)
        ax.relim()
        ax.autoscale()

        self.anim = animation.FuncAnimation(fig, self.animate,
                                            init_func = self.init,
                                            frames = len(self.xp),
                                            repeat=True,
                                            interval=20, blit=True)

        return HTML(self.anim.to_jshtml())

    def init(self):
        xsel = np.ravel(np.append(self.xp[0:self.n],
                                  np.asarray([self.xs[0], self.xp[0]])))
        ysel = np.ravel(np.append(self.yp[0:self.n],
                                  np.asarray([self.ys[0], self.yp[0]])))
        xy = np.transpose(np.asarray([xsel, ysel]))

        self.coll.set_xy(xy)
        return (self.coll,)

    def animate(self, i):
        sel = np.arange(i, i+self.n) % len(self.xp)

        xsel = np.ravel(np.append(self.xp[sel],
                                  np.asarray([self.xs[0], self.xp[i]])))
        ysel = np.ravel(np.append(self.yp[sel],
                                  np.asarray([self.ys[0], self.yp[i]])))

        xy = np.transpose(np.asarray([xsel, ysel]))
        self.coll.set_xy(xy)
        return (self.coll,)
