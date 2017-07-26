#!/usr/bin/env python

'''
Use the 'pdfpages' latex package to only include some pages and arrange several
on a sheet of paper.
Requires 'pdflatex' and the 'pdfpages' latex package.
'''

import sys
import os
import tempfile
import subprocess
import shutil
import optparse

TEMPLATE = r'''
\documentclass[%(paper)s]{article}
\usepackage{pdfpages}

\begin{document}
\includepdf[
    pages={%(pages)s},
    nup=%(nup)s,
    landscape=%(landscape)s,
    openright=%(open_right)s,
]{%(filename)s}
\end{document}
'''

def program_name():
    return os.path.basename(sys.argv[0])

def run_cmd_quiet(cmd_line_list):
    # use TemporaryFile for '> /dev/null' behavior
    r = subprocess.call(cmd_line_list, stdout=tempfile.TemporaryFile(mode='w'))
    if r != 0:
        raise Exception('%s returned %d' % cmd_line_list)

def bool_to_latex(v):
    if not isinstance(v, bool):
        return v
    if v:
        return 'true'
    else:
        return 'false'

def do_pdf_pages(filename, options):
    'output is in options.filename + ".pdf-pages.pdf"'
    filename = os.path.realpath(filename)
    tdir = tempfile.mkdtemp('-pdf-pages')
    if options.debug:
        sys.stderr.write('%s: working dir: "%s"\n' % (program_name(), tdir))
    try:
        old_dir = os.getcwd()
        os.chdir(tdir)
        
        # work around for using Unicode filenames in Tex
        os.link(filename, 'input.pdf')

        pdfpages_options = dict( (k, bool_to_latex(v)) 
                for (k, v) in options.__dict__.iteritems())
        pdfpages_options['filename'] = 'input.pdf'
        t = file('pdfpages.tex', 'w')
        t.write(TEMPLATE % pdfpages_options)
        t.close()
        if options.debug:
            sys.stderr.write(TEMPLATE % pdfpages_options)

        run_cmd_quiet(['pdflatex', 'pdfpages.tex'])
        shutil.move('pdfpages.pdf',
                    os.path.join(old_dir,
                    os.path.splitext(os.path.basename(filename))[0] + '-pdf-pages.pdf'))
    finally:
        if not options.debug:
            shutil.rmtree(tdir)

def main(args):
    op = optparse.OptionParser(usage='usage: %prog PDF_FILE', option_list=[
        optparse.Option('--paper', dest='paper', default='a4paper',
                    help='physical size of the paper to print on'),
        optparse.Option('-p', '--pages', dest='pages', default='-', # all pages
                    help='pages specification, inclusive, ex:1-3,17'),
        optparse.Option('-n', '--nup', dest='nup', default='1x2',
                    help='number of pages to put on a sheet, ex:1x2 or 2x2'),
        optparse.Option('--portrait',
                    action='store_false', dest='landscape',
                    default=True,
                    help='print in portrait mode'),
        optparse.Option('--open-left',
                    action='store_false', dest='open_right',
                    default=True,
                    help='insert blank page at start'),
        optparse.Option('--debug',
                    action='store', dest='debug',
                    default=0, type=int,
                    help='enable debugging'),
    ])

    (options, args) = op.parse_args(args)

    if len(args) != 1:
        op.print_help()
        sys.exit(1)

    filename = args[0]

    # 'b5' -> 'b5paper'
    if not options.paper.endswith('paper'):
        options.paper = options.paper.lower() + 'paper'

    do_pdf_pages(filename, options)

if __name__ == '__main__':
    main(sys.argv[1:])
