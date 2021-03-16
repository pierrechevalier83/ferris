"""
Tests of simple 2-layer PCBs
"""

from . import plotting_test_utils

import os
import mmap
import re
import logging


def expect_file_at(filename):

    assert(os.path.isfile(filename))


def get_gerber_filename(board_name, layer_slug, ext='.gbr'):
    return board_name + '-' + layer_slug + ext


def find_gerber_aperture(s, ap_desc):

    m = re.search(r'%AD(.*)' + ap_desc + r'\*%', s)

    if not m:
        return None

    return m.group(1)


def expect_gerber_has_apertures(gbr_data, ap_list):

    aps = []

    for ap in ap_list:

        # find the circular aperture for the outline
        ap_no = find_gerber_aperture(gbr_data, ap)

        assert ap_no is not None

        # apertures from D10 to D999
        assert len(ap_no) in [2, 3]

        aps.append(ap_no)

    logging.debug("Found apertures {}".format(aps))
    return aps


def expect_gerber_flash_at(gbr_data, pos):
    """
    Check for a gerber flash at a given point
    (it's hard to check that aperture is right without a real gerber parser
    """

    repat = r'^X{x}Y{y}D03\*$'.format(
        x=int(pos[0] * 100000),
        y=int(pos[1] * 100000)
    )

    m = re.search(repat, gbr_data, re.MULTILINE)

    assert(m)

    logging.debug("Gerber flash found: " + repat)


def get_mmapped_data(filename):

    with open(filename) as fo:
        return mmap.mmap(fo.fileno(), 0, access=mmap.ACCESS_READ)


# content of test_sample.py
def test_2layer():

    ctx = plotting_test_utils.KiPlotTestContext('simple_2layer')

    ctx.load_yaml_config_file('simple_2layer.kiplot.yaml')
    ctx.board_name = 'simple_2layer'

    ctx.do_plot()

    gbr_dir = ctx.cfg.resolve_output_dir_for_name('gerbers')

    f_cu_gbr = os.path.join(gbr_dir,
                            get_gerber_filename(ctx.board_name, "F_Cu"))

    expect_file_at(f_cu_gbr)

    f_cu_data = get_mmapped_data(f_cu_gbr)

    ap_ids = expect_gerber_has_apertures(f_cu_data, [
        "C,0.200000",
        "R,2.000000X2.000000",
        "C,1.000000"])

    # expect a flash for the square pad
    expect_gerber_flash_at(f_cu_data, (140, -100))

    ctx.clean_up()
