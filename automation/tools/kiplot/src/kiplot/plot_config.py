
import os

import pcbnew

from . import error


class KiPlotConfigurationError(error.KiPlotError):
    pass


class TypeOptions(object):

    def validate(self):
        """
        Return list of invalid settings
        """

        return []


class LayerOptions(TypeOptions):
    """
    Common options that all layer outputs have
    """

    AUTO_SCALE = 0

    def __init__(self):

        super(LayerOptions, self).__init__()

        self.exclude_edge_layer = False
        self.exclude_pads_from_silkscreen = False
        self.plot_sheet_reference = False

        self._supports_line_width = False
        self._line_width = 0

        self._supports_aux_axis_origin = False
        self._use_aux_axis_as_origin = False

        # override for scalable formats
        self._supports_scaling = False

        self._auto_scale = False
        self._scaling = 1

        self._supports_mirror = False
        self._mirror_plot = False

        self._supports_negative = False
        self._negative_plot = False

        self._supports_drill_marks = False
        self._drill_marks = pcbnew.PCB_PLOT_PARAMS.NO_DRILL_SHAPE

        self._support_sketch_mode = False
        self._sketch_mode = False

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        """
        Set the line width, in mm
        """
        if self._supports_line_width:
            self._line_width = pcbnew.FromMM(value)
        else:
            raise KiPlotConfigurationError(
                "This output doesn't support setting line width")

    @property
    def auto_scale(self):
        return self._auto_scale

    @property
    def scaling(self):
        return self._scaling

    @scaling.setter
    def scaling(self, val):
        """
        Set scaling, if possible. AUTO_SCALE to set auto scaling
        """

        if self._supports_scaling:

            if val == self.AUTO_SCALE:
                self._scaling = 1
                self._auto_scale = True
            else:
                self._scaling = val
                self._auto_scale = False
        else:
            raise KiPlotConfigurationError(
                "This Layer output does not support scaling")

    @property
    def mirror_plot(self):
        return self._mirror_plot

    @mirror_plot.setter
    def mirror_plot(self, val):

        if self._supports_mirror:
            self._mirror_plot = val
        else:
            raise KiPlotConfigurationError(
                "This Layer output does not support mirror plotting")

    @property
    def negative_plot(self):
        return self._negative_plot

    @negative_plot.setter
    def negative_plot(self, val):

        if self._supports_mirror:
            self._negative_plot = val
        else:
            raise KiPlotConfigurationError(
                "This Layer output does not support negative plotting")

    @property
    def drill_marks(self):
        return self._drill_marks

    @drill_marks.setter
    def drill_marks(self, val):

        if self._supports_drill_marks:

            try:
                drill_mark = {
                    'none': pcbnew.PCB_PLOT_PARAMS.NO_DRILL_SHAPE,
                    'small': pcbnew.PCB_PLOT_PARAMS.SMALL_DRILL_SHAPE,
                    'full': pcbnew.PCB_PLOT_PARAMS.FULL_DRILL_SHAPE,
                }[val]
            except KeyError:
                raise KiPlotConfigurationError(
                    "Unknown drill mark type: {}".format(val))

            self._drill_marks = drill_mark
        else:
            raise KiPlotConfigurationError(
                "This Layer output does not support drill marks")

    @property
    def use_aux_axis_as_origin(self):
        return self._use_aux_axis_as_origin

    @use_aux_axis_as_origin.setter
    def use_aux_axis_as_origin(self, val):

        if self._supports_aux_axis_origin:
            self._use_aux_axis_as_origin = val
        else:
            raise KiPlotConfigurationError(
                "This Layer output does not support using the auxiliary"
                " axis as the origin")

    @property
    def sketch_mode(self):
        return self._sketch_mode

    @sketch_mode.setter
    def sketch_mode(self, val):

        if self._supports_sketch_mode:
            self._sketch_mode = val
        else:
            raise KiPlotConfigurationError(
                "This Layer output does not support sketch mode")


class GerberOptions(LayerOptions):

    def __init__(self):

        super(GerberOptions, self).__init__()

        self._supports_line_width = True
        self._supports_aux_axis_origin = True

        self.subtract_mask_from_silk = False
        self.use_protel_extensions = False
        self.create_gerber_job_file = False
        self.use_gerber_x2_attributes = False
        self.use_gerber_net_attributes = False

        # either 5 or 6
        self._gerber_precision = None

    def validate(self):

        errs = super(GerberOptions, self).validate()

        if (not self.use_gerber_x2_attributes and
                self.use_gerber_net_attributes):
            errs.append("Must set Gerber X2 attributes to use net attributes")

        return errs

    @property
    def gerber_precision(self):
        return self._gerber_precision

    @gerber_precision.setter
    def gerber_precision(self, val):
        """
        Set gerber precision: either 4.5 or 4.6
        """
        if val == 4.5:
            self._gerber_precision = 5
        elif val == 4.6:
            self._gerber_precision = 6
        else:
            raise KiPlotConfigurationError(
                "Bad Gerber precision : {}".format(val))


class HpglOptions(LayerOptions):

    def __init__(self):

        super(HpglOptions, self).__init__()

        self._supports_sketch_mode = True
        self._supports_mirror = True
        self._supports_scaling = True
        self._supports_drill_marks = True

        self._pen_width = None

    @property
    def pen_width(self):
        return self._pen_width

    @pen_width.setter
    def pen_width(self, pw_mm):
        self._pen_width = pcbnew.FromMM(pw_mm)


class PsOptions(LayerOptions):

    def __init__(self):

        super(PsOptions, self).__init__()

        self._supports_mirror = True
        self._supports_negative = True
        self._supports_scaling = True
        self._supports_drill_marks = True
        self._supports_line_width = True
        self._supports_sketch_mode = True

        self.scale_adjust_x = 1.0
        self.scale_adjust_y = 1.0

        self._width_adjust = 0

        self.a4_output = False

    @property
    def width_adjust(self):
        return self._width_adjust

    @width_adjust.setter
    def width_adjust(self, width_adjust_mm):
        self._width_adjust = pcbnew.FromMM(width_adjust_mm)


class SvgOptions(LayerOptions):

    def __init__(self):

        super(SvgOptions, self).__init__()

        self._supports_line_width = True
        self._supports_mirror = True
        self._supports_negative = True
        self._supports_drill_marks = True


class PdfOptions(LayerOptions):

    def __init__(self):

        super(PdfOptions, self).__init__()

        self._supports_line_width = True
        self._supports_mirror = True
        self._supports_negative = True
        self._supports_drill_marks = True


class DxfOptions(LayerOptions):

    def __init__(self):

        super(DxfOptions, self).__init__()

        self._supports_aux_axis_origin = True
        self._supports_drill_marks = True

        self.polygon_mode = False


class DrillOptions(TypeOptions):

    def __init__(self):

        super(DrillOptions, self).__init__()

        self.use_aux_axis_as_origin = False

        self.map_options = None
        self.report_options = None

    @property
    def generate_map(self):
        return self.map_options is not None

    @property
    def generate_report(self):
        return self.report_options is not None


class ExcellonOptions(DrillOptions):

    def __init__(self):

        super(ExcellonOptions, self).__init__()

        self.metric_units = True
        self.minimal_header = False
        self.mirror_y_axis = False


class GerberDrillOptions(DrillOptions):

    def __init__(self):

        super(GerberDrillOptions, self).__init__()


class DrillReportOptions(object):

    def __init__(self):
        self.filename = None


class DrillMapOptions(object):

    def __init__(self):
        self.type = None


class OutputOptions(object):

    GERBER = 'gerber'
    POSTSCRIPT = 'ps'
    HPGL = 'hpgl'
    SVG = 'svg'
    PDF = 'pdf'
    DXF = 'dxf'

    EXCELLON = 'excellon'
    GERB_DRILL = 'gerb_drill'

    def __init__(self, otype):
        self.type = otype

        if otype == self.GERBER:
            self.type_options = GerberOptions()
        elif otype == self.POSTSCRIPT:
            self.type_options = PsOptions()
        elif otype == self.HPGL:
            self.type_options = HpglOptions()
        elif otype == self.SVG:
            self.type_options = SvgOptions()
        elif otype == self.DXF:
            self.type_options = DxfOptions()
        elif otype == self.PDF:
            self.type_options = PdfOptions()
        elif otype == self.EXCELLON:
            self.type_options = ExcellonOptions()
        elif otype == self.GERB_DRILL:
            self.type_options = GerberDrillOptions()
        else:
            self.type_options = None

    def validate(self):

        if self.type_options is None:
            return ["No type specific options found"]

        return self.type_options.validate()


class LayerInfo(object):

    def __init__(self, layer, is_inner):

        self.layer = layer
        self.is_inner = is_inner


class LayerConfig(object):

    def __init__(self, layer):

        # the Pcbnew layer
        self.layer = layer
        self.suffix = ""
        self.desc = "desc"


class PlotOutput(object):

    def __init__(self, name, description, otype, options):
        self.name = name
        self.description = description
        self.outdir = None
        self.options = options

        self.layers = []

    def validate(self):
        return self.options.validate()


class PlotConfig(object):

    def __init__(self):

        self._outputs = []
        self.outdir = None

        self.check_zone_fills = False
        self.run_drc = False

    def add_output(self, new_op):
        self._outputs.append(new_op)

    def get_output_by_name(self, output_name):
        """
        Gets an output with a given name.

        @param output_name the name of the output to find
        """
        for o in self.outputs:

            if o.name == output_name:
                return o

        return None

    def resolve_output_dir_for_name(self, output_name):
        """
        Get the output dir for a given output name
        """

        o = self.get_output_by_name(output_name)
        return os.path.join(self.outdir, o.outdir) if o else None

    def validate(self):

        errs = []

        for o in self._outputs:
            errs += o.validate()

        return errs

    @property
    def outputs(self):
        return self._outputs
