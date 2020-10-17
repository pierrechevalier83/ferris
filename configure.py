#!/usr/bin/env python3

from tools.ninja.misc.ninja_syntax import Writer

OUTPUT_DIR = "build"
VARIANTS = [
    "0.1/base",
    "0.1/compact",
    "0.1/high",
    "0.1/low",
    "0.2/bling",
    "0.2/compact",
    "0.2/high",
    "0.2/mini",
]


def add_comment_header(ninja, variant):
    ninja.comment(f"{variant}")
    ninja.newline()


def underscorify(variant):
    return variant.replace("/", "_").replace(".", "_")


def make_gerber_rule_name(variant):
    return underscorify(variant) + "_gerbers"


def make_board_path(variant):
    return variant + "/ferris.kicad_pcb"


def make_variant_out_dir(variant):
    return f"{OUTPUT_DIR}/{variant}"


def make_gerber_output_paths(variant):
    gerbers_out = [
        "ferris-B_Cu.gbr",
        "ferris-B_Mask.gbr",
        "ferris-B_Paste.gbr",
        "ferris-B_SilkS.gbr",
        "ferris-Edge_Cuts.gbr",
        "ferris-F_Cu.gbr",
        "ferris-F_Mask.gbr",
        "ferris-F_Paste.gbr",
        "ferris-F_SilkS.gbr",
    ]
    return [f"{make_variant_out_dir(variant)}/{f}" for f in gerbers_out]


def add_gerber_rule(ninja, variant):
    gerber_rule = make_gerber_rule_name(variant)
    board = make_board_path(variant)
    config = ".kiplot.yml"
    out_dir = make_variant_out_dir(variant)
    ninja.rule(
        name=gerber_rule,
        command=[f"mkdir -p {out_dir} && kiplot -b {board} -c {config} -d {out_dir}"],
    )
    ninja.build(outputs=make_gerber_output_paths(variant), rule=gerber_rule)
    ninja.newline()


def make_zip_filename(variant):
    return underscorify(variant) + "_gerbers.zip"


def make_zip_gerber_rule_name(variant):
    return underscorify(make_zip_filename(variant))


def add_zip_gerber_rule(ninja, variant):
    zip_gerber_rule = make_zip_gerber_rule_name(variant)
    zip_file = f"{OUTPUT_DIR}/{make_zip_filename(variant)}"
    gerber_files = make_gerber_output_paths(variant)
    gerber_rule = make_gerber_rule_name(variant)
    ninja.rule(name=zip_gerber_rule, command=[f"zip -r {zip_file}"] + gerber_files)
    ninja.build(inputs=gerber_files, outputs=zip_file, rule=zip_gerber_rule)
    ninja.newline()


def generate_buildfile_content():
    ninja = Writer(open("build.ninja", "w"))
    variants = VARIANTS
    for variant in variants:
        add_comment_header(ninja, variant)
        add_gerber_rule(ninja, variant)
        add_zip_gerber_rule(ninja, variant)
    return ninja


generate_buildfile_content()
