"""
Class to read KiPlot config files
"""

import logging
import yaml
import os
import re

import pcbnew

from . import plot_config as PC
from . import error


class CfgReader(object):

    def __init__(self):
        pass


class YamlError(error.KiPlotError):
    pass


class CfgYamlReader(CfgReader):

    def __init__(self):
        super(CfgYamlReader, self).__init__()

    def _check_version(self, data):

        try:
            version = data['kiplot']['version']
        except KeyError:
            raise YamlError("YAML config needs kiplot.version.")
            return None

        if version != 1:
            raise YamlError("Unknown KiPlot config version: {}"
                            .format(version))
            return None

        return version

    def _get_required(self, data, key):

        try:
            val = data[key]
        except KeyError:
            raise YamlError("Value is needed for {}".format(key))

        return val

    def _parse_drill_map(self, map_opts):

        mo = PC.DrillMapOptions()

        TYPES = {
            'hpgl': pcbnew.PLOT_FORMAT_HPGL,
            'ps': pcbnew.PLOT_FORMAT_POST,
            'gerber': pcbnew.PLOT_FORMAT_GERBER,
            'dxf': pcbnew.PLOT_FORMAT_DXF,
            'svg': pcbnew.PLOT_FORMAT_SVG,
            'pdf': pcbnew.PLOT_FORMAT_PDF
        }

        type_s = self._get_required(map_opts, 'type')

        try:
            mo.type = TYPES[type_s]
        except KeyError:
            raise YamlError("Unknown drill map type: {}".format(type_s))

        return mo

    def _parse_drill_report(self, report_opts):

        opts = PC.DrillReportOptions()

        opts.filename = self._get_required(report_opts, 'filename')

        return opts

    def _perform_config_mapping(self, otype, cfg_options, mapping_list, 
                                target):
        """
        Map a config dict onto a target object given a mapping list
        """

        for mapping in mapping_list:

            # if this output type matches the mapping specification:
            if otype in mapping['types']:

                key = mapping['key']

                # set the internal option as needed
                if mapping['required'](cfg_options):

                    cfg_val = self._get_required(cfg_options, key)
                elif key in cfg_options:
                    # not required but given anyway
                    cfg_val = cfg_options[key]
                else:
                    continue

                # transform the value if needed
                if 'transform' in mapping:
                    cfg_val = mapping['transform'](cfg_val)

                setattr(target, mapping['to'], cfg_val)

    def _parse_out_opts(self, otype, options):

        # note - type IDs are strings form the _config_, not the internal
        # strings used as enums (in plot_config)
        ANY_LAYER = ['gerber', 'ps', 'svg', 'hpgl', 'pdf', 'dxf']
        ANY_DRILL = ['excellon', 'gerb_drill']

        # mappings from YAML keys to type_option keys
        MAPPINGS = [
            {
                'key': 'use_aux_axis_as_origin',
                'types': ['gerber', 'dxf'],
                'to': 'use_aux_axis_as_origin',
                'required': lambda opts: True,
            },
            {
                'key': 'exclude_edge_layer',
                'types': ANY_LAYER,
                'to': 'exclude_edge_layer',
                'required': lambda opts: True,
            },
            {
                'key': 'exclude_pads_from_silkscreen',
                'types': ANY_LAYER,
                'to': 'exclude_pads_from_silkscreen',
                'required': lambda opts: True,
            },
            {
                'key': 'plot_sheet_reference',
                'types': ANY_LAYER,
                'to': 'plot_sheet_reference',
                'required': lambda opts: True,
            },
            {
                'key': 'plot_footprint_refs',
                'types': ANY_LAYER,
                'to': 'plot_footprint_refs',
                'required': lambda opts: True,
            },
            {
                'key': 'plot_footprint_values',
                'types': ANY_LAYER,
                'to': 'plot_footprint_values',
                'required': lambda opts: True,
            },
            {
                'key': 'force_plot_invisible_refs_vals',
                'types': ANY_LAYER,
                'to': 'force_plot_invisible_refs_vals',
                'required': lambda opts: True,
            },
            {
                'key': 'tent_vias',
                'types': ANY_LAYER,
                'to': 'tent_vias',
                'required': lambda opts: True,
            },
            {
                'key': 'check_zone_fills',
                'types': ANY_LAYER,
                'to': 'check_zone_fills',
                'required': lambda opts: True,
            },
            {
                'key': 'line_width',
                'types': ['gerber', 'ps', 'svg', 'pdf'],
                'to': 'line_width',
                'required': lambda opts: True,
            },
            {
                'key': 'subtract_mask_from_silk',
                'types': ['gerber'],
                'to': 'subtract_mask_from_silk',
                'required': lambda opts: True,
            },
            {
                'key': 'mirror_plot',
                'types': ['ps', 'svg', 'hpgl', 'pdf'],
                'to': 'mirror_plot',
                'required': lambda opts: True,
            },
            {
                'key': 'negative_plot',
                'types': ['ps', 'svg', 'pdf'],
                'to': 'negative_plot',
                'required': lambda opts: True,
            },
            {
                'key': 'sketch_plot',
                'types': ['ps', 'hpgl'],
                'to': 'sketch_plot',
                'required': lambda opts: True,
            },
            {
                'key': 'scaling',
                'types': ['ps', 'hpgl'],
                'to': 'scaling',
                'required': lambda opts: True,
            },
            {
                'key': 'drill_marks',
                'types': ['ps', 'svg', 'dxf', 'hpgl', 'pdf'],
                'to': 'drill_marks',
                'required': lambda opts: True,
            },
            {
                'key': 'use_protel_extensions',
                'types': ['gerber'],
                'to': 'use_protel_extensions',
                'required': lambda opts: True,
            },
            {
                'key': 'gerber_precision',
                'types': ['gerber'],
                'to': 'gerber_precision',
                'required': lambda opts: True,
            },
            {
                'key': 'create_gerber_job_file',
                'types': ['gerber'],
                'to': 'create_gerber_job_file',
                'required': lambda opts: True,
            },
            {
                'key': 'use_gerber_x2_attributes',
                'types': ['gerber'],
                'to': 'use_gerber_x2_attributes',
                'required': lambda opts: True,
            },
            {
                'key': 'use_gerber_net_attributes',
                'types': ['gerber'],
                'to': 'use_gerber_net_attributes',
                'required': lambda opts: True,
            },
            {
                'key': 'scale_adjust_x',
                'types': ['ps'],
                'to': 'scale_adjust_x',
                'required': lambda opts: True,
            },
            {
                'key': 'scale_adjust_y',
                'types': ['ps'],
                'to': 'scale_adjust_y',
                'required': lambda opts: True,
            },
            {
                'key': 'width_adjust',
                'types': ['ps'],
                'to': 'width_adjust',
                'required': lambda opts: True,
            },
            {
                'key': 'a4_output',
                'types': ['ps'],
                'to': 'a4_output',
                'required': lambda opts: True,
            },
            {
                'key': 'pen_width',
                'types': ['hpgl'],
                'to': 'pen_width',
                'required': lambda opts: True,
            },
            {
                'key': 'polygon_mode',
                'types': ['dxf'],
                'to': 'polygon_mode',
                'required': lambda opts: True,
            },
            {
                'key': 'use_aux_axis_as_origin',
                'types': ANY_DRILL,
                'to': 'use_aux_axis_as_origin',
                'required': lambda opts: True,
            },
            {
                'key': 'map',
                'types': ANY_DRILL,
                'to': 'map_options',
                'required': lambda opts: False,
                'transform': self._parse_drill_map
            },
            {
                'key': 'report',
                'types': ANY_DRILL,
                'to': 'report_options',
                'required': lambda opts: False,
                'transform': self._parse_drill_report
            },
            {
                'key': 'metric_units',
                'types': ['excellon'],
                'to': 'metric_units',
                'required': lambda opts: True,
            },
            {
                'key': 'pth_and_npth_single_file',
                'types': ['excellon'],
                'to': 'pth_and_npth_single_file',
                'required': lambda opts: True,
            },
            {
                'key': 'minimal_header',
                'types': ['excellon'],
                'to': 'minimal_header',
                'required': lambda opts: True,
            },
            {
                'key': 'mirror_y_axis',
                'types': ['excellon'],
                'to': 'mirror_y_axis',
                'required': lambda opts: True,
            },
        ]

        po = PC.OutputOptions(otype)

        # options that apply to the specific output type
        to = po.type_options

        self._perform_config_mapping(otype, options, MAPPINGS, to)

        return po

    def _get_layer_from_str(self, s):
        """
        Get the pcbnew layer from a string in the config
        """

        D = {
            'F.Cu': pcbnew.F_Cu,
            'B.Cu': pcbnew.B_Cu,
            'F.Adhes': pcbnew.F_Adhes,
            'B.Adhes': pcbnew.B_Adhes,
            'F.Paste': pcbnew.F_Paste,
            'B.Paste': pcbnew.B_Paste,
            'F.SilkS': pcbnew.F_SilkS,
            'B.SilkS': pcbnew.B_SilkS,
            'F.Mask': pcbnew.F_Mask,
            'B.Mask': pcbnew.B_Mask,
            'Dwgs.User': pcbnew.Dwgs_User,
            'Cmts.User': pcbnew.Cmts_User,
            'Eco1.User': pcbnew.Eco1_User,
            'Eco2.User': pcbnew.Eco2_User,
            'Edge.Cuts': pcbnew.Edge_Cuts,
            'Margin': pcbnew.Margin,
            'F.CrtYd': pcbnew.F_CrtYd,
            'B.CrtYd': pcbnew.B_CrtYd,
            'F.Fab': pcbnew.F_Fab,
            'B.Fab': pcbnew.B_Fab,
        }

        layer = None

        if s in D:
            layer = PC.LayerInfo(D[s], False)
        elif s.startswith("Inner"):
            m = re.match(r"^Inner\.([0-9]+)$", s)

            if not m:
                raise YamlError("Malformed inner layer name: {}"
                                .format(s))

            layer = PC.LayerInfo(int(m.group(1)), True)
        else:
            raise YamlError("Unknown layer name: {}".format(s))

        return layer

    def _parse_layer(self, l_obj):

        l_str = self._get_required(l_obj, 'layer')
        layer_id = self._get_layer_from_str(l_str)
        layer = PC.LayerConfig(layer_id)

        layer.desc = l_obj['description'] if 'description' in l_obj else None
        layer.suffix = l_obj['suffix'] if 'suffix' in l_obj else ""

        return layer

    def _parse_output(self, o_obj):

        try:
            name = o_obj['name']
        except KeyError:
            raise self.YamlError("Output needs a name")

        try:
            desc = o_obj['description']
        except KeyError:
            desc = None

        try:
            otype = o_obj['type']
        except KeyError:
            raise YamlError("Output needs a type")

        if otype not in ['gerber', 'ps', 'hpgl', 'dxf', 'pdf', 'svg',
                         'gerb_drill', 'excellon']:
            raise YamlError("Unknown output type: {}".format(otype))

        try:
            options = o_obj['options']
        except KeyError:
            raise YamlError("Output need to have options specified")

        logging.debug("Parsing output options for {} ({})".format(name, otype))

        outdir = self._get_required(o_obj, 'dir')

        output_opts = self._parse_out_opts(otype, options)

        o_cfg = PC.PlotOutput(name, desc, otype, output_opts)
        o_cfg.outdir = outdir

        try:
            layers = o_obj['layers']
        except KeyError:
            layers = []

        for l in layers:
            o_cfg.layers.append(self._parse_layer(l))

        return o_cfg

    def _parse_preflight(self, pf, cfg):

        logging.debug("Parsing preflight options: {}".format(pf))

        if 'check_zone_fills' in pf:
            cfg.check_zone_fills = pf['check_zone_fills']

        if 'run_drc' in pf:
            cfg.run_drc = pf['run_drc']

    def read(self, fstream):
        """
        Read a file object into a config object

        :param fstream: file stream of a config YAML file
        """

        try:
            data = yaml.load(fstream)
        except yaml.YAMLError as e:
            raise YamlError("Error loading YAML")
            return None

        self._check_version(data)

        cfg = PC.PlotConfig()

        if 'preflight' in data:
            self._parse_preflight(data['preflight'], cfg)

        for o in data['outputs']:

            op_cfg = self._parse_output(o)
            cfg.add_output(op_cfg)

        return cfg
