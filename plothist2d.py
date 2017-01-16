#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals

__all__ = ["corner", "hist2d", "error_ellipse"]
__version__ = "0.0.6"
__author__ = "Dan Foreman-Mackey (danfm@nyu.edu)"
__copyright__ = "Copyright 2013 Daniel Foreman-Mackey"
__contributors__ = [
                    # Alphabetical by first name.
                    "Adrian Price-Whelan @adrn",
                    "Brendon Brewer @eggplantbren",
                    "Ekta Patel @ekta1224",
                    "Emily Rice @emilurice",
                    "Geoff Ryan @geoffryan",
                    "Kyle Barbary @kbarbary",
                    "Phil Marshall @drphilmarshall",
                    "Pierre Gratier @pirg",
                    "Becky Smethurst @becky1505",
                    ]

import numpy as np
import matplotlib.pyplot as pl
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Ellipse
import matplotlib.cm as cm

def plothist2d(H, X, Y, *args, **kwargs):
    """
        Plot a 2-D histogram of already histogrammed data.
        
        """
    ax = kwargs.pop("ax", pl.gca())
    
    extent = kwargs.pop("extent", [[X.min(), X.max()], [X.min(), Y.max()]])
    bins = kwargs.pop("bins", 50)
    color = kwargs.pop("color", "k")
    linewidths = kwargs.pop("linewidths", None)
    plot_datapoints = kwargs.get("plot_datapoints", True)
    plot_contours = kwargs.get("plot_contours", True)
    levels = kwargs.get("levels", None)
    
    cmap = cm.get_cmap("gray")
    cmap._init()
    cmap._lut[:-3, :-1] = 0.
    cmap._lut[:-3, -1] = np.linspace(1, 0, cmap.N)
    
        
    X = np.linspace(np.min(X), np.max(X), len(X) + 1)
    Y = np.linspace(np.min(Y), np.max(Y), len(Y) + 1)
        
    V = 1.0 - np.exp(-0.5 * np.arange(0.1, 2.6, 0.5) ** 2)
    Hflat = H.flatten()
    inds = np.argsort(Hflat)[::-1]
    Hflat = Hflat[inds]
    sm = np.cumsum(Hflat)
    sm /= sm[-1]
    
    for i, v0 in enumerate(V):
        try:
            V[i] = Hflat[sm <= v0][-1]
        except:
            V[i] = Hflat[0]
    
    X1, Y1 = 0.5 * (X[1:] + X[:-1]), 0.5 * (Y[1:] + Y[:-1])
    X, Y = X[:-1], Y[:-1]
    
    if plot_datapoints:
        ax.plot(x, y, "o", color=color, ms=1.5, zorder=-1, alpha=0.1,
                rasterized=True)
        if plot_contours:
            ax.contourf(X1, Y1, H.T, [V[-1], H.max()],
                        cmap=LinearSegmentedColormap.from_list("cmap",
                                                               ([1] * 3,
                                                                [1] * 3),
                                                               N=2), antialiased=False)
    
    if plot_contours:
        ax.pcolor(X, Y, H.max() - H.T, cmap=cmap)
        ax.contour(X1, Y1, H.T, levels = levels, colors=color, linewidths=linewidths)
    
#    data = np.vstack([x, y])
#    mu = np.mean(data, axis=1)
#    cov = np.cov(data)
#    if kwargs.pop("plot_ellipse", False):
#        error_ellipse(mu, cov, ax=ax, edgecolor="r", ls="dashed")
    
    ax.set_xlim(extent[0])
    ax.set_ylim(extent[1])
