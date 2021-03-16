
import os
import shutil
import tempfile
import logging
import pytest


from kiplot import kiplot
from kiplot import config_reader


KICAD_PCB_EXT = '.kicad_pcb'


class KiPlotTestContext(object):

    def __init__(self, test_name):
        self.cfg = None

        # The name used for the test output dirs and other logging
        self.test_name = test_name

        # The name of the PCB board file (will be interpolated into the plot
        # files by pcbnewm so we need to know
        self.board_name = None

        # The actual board file that will be loaded
        self.board_file = None

        # The directory under which to place plots (None: use a temp dir)
        self.plot_dir = pytest.config.getoption('plot_dir')

        # The actual output dir for this plot run
        self._output_dir = None
        # Clean the output dir afterwards (true for temp dirs)
        self._del_dir_after = self.plot_dir is None

    def _get_text_cfg_dir(self):

        this_dir = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(this_dir, '../yaml_samples')

    def _get_board_cfg_dir(self):

        this_dir = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(this_dir, '../board_samples')

    def load_yaml_config_file(self, filename):
        """
        Reads a config from a YAML file
        """

        cfg_file = os.path.join(self._get_text_cfg_dir(), filename)

        cr = config_reader.CfgYamlReader()

        with open(cfg_file) as cf_file:
            cfg = cr.read(cf_file)

        self.cfg = cfg

    def _load_board_file(self, filename=None):
        """
        Load the named board.

        @param filename: a filename to load, or None to load the relevant
        board name from the board sample dir
        """

        if filename is None:
            self.board_file = os.path.join(self._get_board_cfg_dir(),
                                           self.board_name + KICAD_PCB_EXT)
        else:
            self.board_file = filename

        assert os.path.isfile(self.board_file)

    def _set_up_output_dir(self):

        if not self.plot_dir:
            # create a tmp dir
            self.output_dir = tempfile.mkdtemp(
                    prefix='tmp_kiplot_{}'.format(self.test_name))

        else:
            self.output_dir = os.path.join(self.plot_dir, self.test_name)
            # just create the dir
            if os.path.isdir(self.output_dir):
                # exists, that's OK
                pass
            else:
                os.makedirs(self.output_dir)

        self.cfg.outdir = self.output_dir
        logging.info(self.output_dir)

    def clean_up(self):

        if self._del_dir_after:
            shutil.rmtree(self.output_dir)

    def do_plot(self):

        self.cfg.validate()

        self._load_board_file(self.board_file)

        self._set_up_output_dir()

        plotter = kiplot.Plotter(self.cfg)
        plotter.plot(self.board_file)
