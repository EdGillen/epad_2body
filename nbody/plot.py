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


class AnimKep3():
    def __init__(self, orb1, orb2):
        self.xs = np.asarray(orb1.star_pos)[:,0]
        self.ys = np.asarray(orb1.star_pos)[:,1]

        self.xp1 = np.asarray(orb1.plan_pos)[:,0]
        self.yp1 = np.asarray(orb1.plan_pos)[:,1]

        #self.xp2 = np.asarray(orb2.plan_pos)[::2,0]
        #self.yp2 = np.asarray(orb2.plan_pos)[::2,1]
        self.xp2 = (0.5)**(2/3)*np.asarray(orb1.plan_pos)[::2,0]
        self.yp2 = (0.5)**(2/3)*np.asarray(orb1.plan_pos)[::2,1]
        self.xp2 = np.append(self.xp2, self.xp2)
        self.yp2 = np.append(self.yp2, self.yp2)

    def show(self, fig, ax, plot_p1, plot_p2, plot_s):
        self.linep1 = plot_p1
        self.linep2 = plot_p2
        self.lines = plot_s

        xp1 = np.append(self.xp1, self.xp1[0])
        yp1 = np.append(self.yp1, self.yp1[0])
        xp2 = np.append(self.xp2, self.xp2[0])
        yp2 = np.append(self.yp2, self.yp2[0])

        self.linep1.set_data(xp1, yp1)
        self.linep2.set_data(xp2, yp2)
        self.lines.set_data(self.xs[0], self.ys[0])

        ax.relim()
        ax.autoscale()

        self.anim = animation.FuncAnimation(fig, self.animate,
                                            init_func = self.init,
                                            frames = len(self.xp1),
                                            repeat=True,
                                            interval=20, blit=True)

        return HTML(self.anim.to_jshtml())

    def init(self):
        self.linep1.set_data([self.xp1[0]],[self.yp1[0]])
        self.linep2.set_data([self.xp2[0]],[self.yp2[0]])
        self.lines.set_data([self.xs[0]],[self.ys[0]])
        return (self.linep2,)

    def animate(self, i):
        self.linep1.set_data([self.xp1[i]],[self.yp1[i]])
        self.linep2.set_data([self.xp2[i]],[self.yp2[i]])
        self.lines.set_data([self.xs[i]],[self.ys[i]])
        return (self.linep2,)
