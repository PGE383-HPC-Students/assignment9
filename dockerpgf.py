#!/usr/bin/env python
from matplotlib.backend_bases import Gcf
from matplotlib.backends.backend_pgf import (FigureCanvasPgf, LatexManager, 
                                             LatexError)
import os
import functools
from tempfile import TemporaryDirectory

FigureCanvas = FigureCanvasPgf

class MyLatexManager(LatexManager):

    def __init__(self):
        # create a tmp directory for running latex, register it for deletion
        self._tmpdir = TemporaryDirectory()
        self.tmpdir = self._tmpdir.name
        self._finalize_tmpdir = weakref.finalize(self, self._tmpdir.cleanup)

        # test the LaTeX setup to ensure a clean startup of the subprocess
        self.texcommand = ['docker', 'run', '--rm', '-v', \
                           f'{os.environ["PWD"]}:{os.environ["PWD"]}', '-w', \
                           f'{os.environ["PWD"]}', 'texlive/texlive', \
                           'pdflatex']
        self.latex_header = LatexManager._build_latex_header()
        latex_end = "\n\\makeatletter\n\\@@end\n"
        try:
            latex = subprocess.Popen(
                [self.texcommand, "-halt-on-error"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                encoding="utf-8", cwd=self.tmpdir)
        except FileNotFoundError as err:
            raise RuntimeError(
                f"{self.texcommand} not found.  Install it or change "
                f"rcParams['pgf.texsystem'] to an available TeX "
                f"implementation.") from err
        except OSError as err:
            raise RuntimeError("Error starting process %r" %
                               self.texcommand) from err
        test_input = self.latex_header + latex_end
        stdout, stderr = latex.communicate(test_input)
        if latex.returncode != 0:
            raise LatexError("LaTeX returned an error, probably missing font "
                             "or error in preamble.", stdout)

        self.latex = None  # Will be set up on first use.
        self.str_cache = {}  # cache for strings already processed

@functools.lru_cache(1)
def _get_image_inclusion_command():
    man = MyLatexManager._get_cached_or_new()
    man._stdin_writeln(
        r"\includegraphics[interpolate=true]{%s}"
        # Don't mess with backslashes on Windows.
        % cbook._get_data_path("images/matplotlib.png").as_posix())
    try:
        prompt = man._expect_prompt()
        return r"\includegraphics"
    except LatexError:
        # Discard the broken manager.
        MyLatexManager._get_cached_or_new_impl.cache_clear()
        return r"\pgfimage"
