# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys

from . import kiplot
from . import config_reader


def main():

    EXIT_BAD_ARGS = 1
    EXIT_BAD_CONFIG = 2

    parser = argparse.ArgumentParser(
        description='Command-line Plotting for KiCad')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show debugging information')
    parser.add_argument('-b', '--board-file', required=True,
                        help='The PCB .kicad-pcb board file')
    parser.add_argument('-c', '--plot-config', required=True,
                        help='The plotting config file to use')
    parser.add_argument('-d', '--out-dir', default='.',
                        help='The output directory (cwd if not given)')

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    if not os.path.isfile(args.board_file):
        logging.error("Board file not found: {}".format(args.board_file))

    if not os.path.isfile(args.plot_config):
        logging.error("Plot config file not found: {}"
                      .format(args.plot_config))
        sys.exit(EXIT_BAD_ARGS)

    cr = config_reader.CfgYamlReader()

    with open(args.plot_config) as cf_file:
        cfg = cr.read(cf_file)

    # relative to CWD (absolute path overrides)
    outdir = os.path.join(os.getcwd(), args.out_dir)
    cfg.outdir = outdir

    # Finally, once all value are in, check they make sense
    errs = cfg.validate()

    if errs:
        logging.error('Invalid config:\n\n' + "\n".join(errs))
        sys.exit(EXIT_BAD_CONFIG)

    # Set up the plotter and do it
    plotter = kiplot.Plotter(cfg)
    plotter.plot(args.board_file)


if __name__ == "__main__":
    main()
