#!/usr/bin/env python

import matplotlib 
matplotlib.use("pgf") 
pgf_with_latex = {"pgf.texsystem": "docker run --rm -it johntfoster/texlive pdflatex"}
matplotlib.rcParams.update(pgf_with_latex)

from assignment9 import Plotter 

p = Plotter("data_1.dat")
p.plot_pgf("ss_plot")'

