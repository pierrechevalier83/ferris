#!/usr/bin/env python3

from tools.ninja.misc.ninja_syntax import Writer

OUTPUT_DIR = "build"
VARIANTS_0_1 = [
    "0.1/base",
    "0.1/compact",
    "0.1/high",
    "0.1/low",
]
VARIANTS_0_2 = [
    "0.2/bling",
    "0.2/compact",
    "0.2/high",
    "0.2/mini",
]
VARIANTS = VARIANTS_0_1 + VARIANTS_0_2
PCBDRAW_DIR = "automation/tools/PcbDraw/pcbdraw"
KIPLOT_DIR = "automation/tools/kiplot/src/kiplot"
IBOM_DIR = "automation/tools/InteractiveHtmlBom/InteractiveHtmlBom"
JLCBOM_DIR = "automation/tools/kicad-jlcpcb-bom-plugin"
RENDER_COLORS = {
    "0.1/base": "white",
    "0.1/compact": "white",
    "0.1/high": "yellow",
    "0.1/low": "blue",
    "0.2/bling": "white",
    "0.2/bling/cases/mid_profile": "white",
    "0.2/compact": "white",
    "0.2/compact/cases/low_profile": "white",
    "0.2/high": "yellow",
    "0.2/mini": "blue",
}
CASE_DIRS = {
    "mid_profile": "mid_profile",
    "low_profile": "low_profile",
}
CASE_BASENAMES = {
    "mid_profile": [
        "left_switch_plate",
        "right_switch_plate",
        "lip",
        "bottom_plate_puck",
        "bottom_plate_no_puck",
    ],
    "mid_profile_without_puck": [
        "top_left_plate_without_puck",
        "top_right_plate_without_puck",
        "mid_plate",
        "bottom_plate_without_puck",
    ],
    "low_profile": [
        "metal_plate",
        "cork_spacer_and_lip",
        "lip",
    ],
}
CASES = {
    "0.2/bling": ["mid_profile"],
    "0.2/compact": ["low_profile"],
}


def add_comment_header(ninja, variant):
    ninja.comment(f"{variant}")
    ninja.newline()


def underscorify(variant):
    return variant.replace("/", "_").replace(".", "_")


def make_pcb_file_name(rel_dir, basename):
    return f"{rel_dir}/{basename}.kicad_pcb"


def make_drc_success_file_name(rel_dir, basename):
    return f"{OUTPUT_DIR}/{make_pcb_file_name(rel_dir, basename)}.drc_success"


def make_raw_bom_file_name(variant):
    return f"{variant}/ferris.xml"


def make_sch_file_name(variant):
    return f"{variant}/ferris.sch"


def make_erc_success_file_name(variant):
    return f"{OUTPUT_DIR}/{make_sch_file_name(variant)}.erc_success"


def make_rule_name(variant, suffix):
    return f"{underscorify(variant)}_{suffix}"


def make_variant_out_dir(variant):
    return f"{OUTPUT_DIR}/{variant}"


def make_output_file_path(variant, filename):
    return f"{make_variant_out_dir(variant)}/{filename}"


def add_render_front_rule(ninja, rel_dir, basename="ferris"):
    pcbdraw = f"{PCBDRAW_DIR}/pcbdraw.py"
    color = RENDER_COLORS[rel_dir]
    style = f"{PCBDRAW_DIR}/styles/set-{color}-enig.json"
    pcb = make_pcb_file_name(rel_dir, basename)
    render_front = make_rule_name(rel_dir, f"render_{basename}_front")
    front_svg = make_output_file_path(rel_dir, f"{basename}_front.svg")
    ninja.rule(
        name=render_front,
        command=[f"python3 {pcbdraw} --silent --style {style} {pcb} {front_svg}"],
    )
    ninja.build(
        inputs=[pcbdraw, style, pcb],
        outputs=[front_svg],
        rule=make_rule_name(rel_dir, f"render_{basename}_front"),
    )
    ninja.newline()


def add_render_back_rule(ninja, rel_dir, basename="ferris"):
    pcbdraw = f"{PCBDRAW_DIR}/pcbdraw.py"
    color = RENDER_COLORS[rel_dir]
    style = f"{PCBDRAW_DIR}/styles/set-{color}-enig.json"
    pcb = make_pcb_file_name(rel_dir, basename)
    render_back = make_rule_name(rel_dir, f"render_{basename}_back")
    back_svg = make_output_file_path(rel_dir, f"{basename}_back.svg")
    ninja.rule(
        name=render_back,
        command=[f"python3 {pcbdraw} --silent --style {style} {pcb} {back_svg} --back"],
    )
    ninja.build(
        inputs=[pcbdraw, style, pcb],
        outputs=[back_svg],
        rule=make_rule_name(rel_dir, f"render_{basename}_back"),
    )
    ninja.newline()


def add_interactive_bom_rule(ninja, variant):
    ibom_generator = f"{IBOM_DIR}/generate_interactive_bom.py"
    # Has to be relative to the PCB file
    out_dir = f"../../{OUTPUT_DIR}/{variant}"
    ibom_output = make_output_file_path(variant, "ibom.html")
    pcb = make_pcb_file_name(variant, "ferris")
    raw_bom = make_raw_bom_file_name(variant)
    ibom_rule = make_rule_name(variant, "ibom")
    ninja.rule(
        name=ibom_rule,
        command=[f"./automation/run_ibom.sh {variant}"],
    )
    ninja.build(
        inputs=["./automation/run_ibom.sh", ibom_generator, pcb, raw_bom],
        outputs=[ibom_output],
        rule=ibom_rule,
    )
    ninja.newline()


def add_jlc_bom_rule(ninja, variant):
    jlc_bom_generator = f"{JLCBOM_DIR}/bom_csv_jlcpcb.py"
    jlc_bom = make_output_file_path(variant, "bom_jlcpcb.csv")
    raw_bom = make_raw_bom_file_name(variant)
    jlc_bom_rule = make_rule_name(variant, "jlc_bom")
    ninja.rule(
        name=jlc_bom_rule,
        command=[f"python3 {jlc_bom_generator} {raw_bom} {jlc_bom}"],
    )
    ninja.build(
        inputs=[jlc_bom_generator, raw_bom],
        outputs=[jlc_bom],
        rule=jlc_bom_rule,
    )
    ninja.newline()


def add_pos_rule(ninja, variant):
    pos_rule = make_rule_name(variant, "pos")
    pcb = make_pcb_file_name(variant, "ferris")
    pos_file = make_output_file_path(variant, "pos.csv")
    ninja.rule(
        name=pos_rule,
        command=[f"python3 ./automation/tools/generate_pos.py {pcb} > {pos_file}"],
    )
    ninja.build(
        inputs=["./automation/tools/generate_pos.py", pcb],
        outputs=[pos_file],
        rule=pos_rule,
    )
    ninja.newline()


def add_jlc_pick_and_place(ninja, variant):
    rule = make_rule_name(variant, "jlc_cpl")
    pos_file = make_output_file_path(variant, "pos.csv")
    output = make_output_file_path(variant, "cpl.csv")
    tool = f"{JLCBOM_DIR}/kicad_pos_to_cpl.py"
    pcb = make_pcb_file_name(variant, "ferris")
    ninja.rule(
        name=rule,
        command=[f"python3 {tool} {pos_file} {output}"],
    )
    ninja.build(
        inputs=[tool, pos_file, pcb],
        outputs=[output],
        rule=rule,
    )
    ninja.newline()


def add_erc_rule(ninja, variant):
    erc_rule = make_rule_name(variant, "erc")
    sch_file = make_sch_file_name(variant)
    ninja.rule(
        name=erc_rule,
        command=[f"./automation/run_erc.sh {sch_file}"],
    )
    ninja.build(
        inputs=["./automation/run_erc.sh", sch_file],
        outputs=[make_erc_success_file_name(variant)],
        rule=erc_rule,
    )
    ninja.newline()


def add_drc_rule(ninja, rel_dir, basename):
    drc_rule = make_rule_name(f"{rel_dir}/{basename}", "drc")
    pcb_file = make_pcb_file_name(rel_dir, basename)
    ninja.rule(
        name=drc_rule,
        command=[f"./automation/run_drc.sh {pcb_file}"],
    )
    ninja.build(
        inputs=["./automation/run_drc.sh", f"{pcb_file}"],
        outputs=[make_drc_success_file_name(rel_dir, basename)],
        rule=drc_rule,
    )
    ninja.newline()


def add_keyboard_drc_rule(ninja, variant):
    add_drc_rule(ninja, variant, "ferris")


def make_gerber_output_paths(variant):
    gerbers_out = [
        "ferris-B_Cu.gbr",
        "ferris-B_Mask.gbr",
        "ferris-B_Paste.gbr",
        "ferris-B_SilkS.gbr",
        "ferris-B_Fab.gbr",
        "ferris-Edge_Cuts.gbr",
        "ferris-F_Cu.gbr",
        "ferris-F_Mask.gbr",
        "ferris-F_Paste.gbr",
        "ferris-F_SilkS.gbr",
        "ferris-F_Fab.gbr",
        "ferris-NPTH-drl_map.gbr",
        "ferris-NPTH.drl",
        "ferris-PTH-drl_map.gbr",
        "ferris-PTH.drl",
    ]
    return [f"{make_variant_out_dir(variant)}/{f}" for f in gerbers_out]


def add_gerber_rule(ninja, variant):
    gerber_rule = make_rule_name(variant, "gerbers")
    board = make_pcb_file_name(variant, "ferris")
    config = ".kiplot.yml"
    out_dir = make_variant_out_dir(variant)
    kiplot = "kiplot"

    ninja.rule(
        name=gerber_rule,
        command=[f"mkdir -p {out_dir} && {kiplot} -b {board} -c {config} -d {out_dir}"],
    )
    ninja.build(
        inputs=[config, board],
        outputs=make_gerber_output_paths(variant),
        rule=gerber_rule,
    )
    ninja.newline()


def add_zip_gerber_rule(ninja, variant):
    zip_gerber_rule = make_rule_name(variant, "gerbers_zip")
    zip_file = make_output_file_path(variant, "gerbers.zip")
    gerber_files = make_gerber_output_paths(variant)
    gerber_rule = make_rule_name(variant, "gerbers")
    ninja.rule(
        name=zip_gerber_rule, command=[f"zip -q -j -r {zip_file}"] + gerber_files
    )
    ninja.build(
        inputs=[
            make_erc_success_file_name(variant),
            make_drc_success_file_name(variant, "ferris"),
        ]
        + gerber_files,
        outputs=zip_file,
        rule=zip_gerber_rule,
    )
    ninja.newline()


def add_edge_cuts_rule(ninja, reldir, basename):
    edge_cuts_rule = make_rule_name(reldir, f"{basename}_edge_cuts")
    board = make_pcb_file_name(reldir, basename)
    config = ".kiplot.edge_cuts.yml"
    out_dir = make_variant_out_dir(reldir)
    kiplot = "kiplot"

    ninja.rule(
        name=edge_cuts_rule,
        command=[f"mkdir -p {out_dir} && {kiplot} -b {board} -c {config} -d {out_dir}"],
    )
    ninja.build(
        inputs=[board, config],
        outputs=[make_output_file_path(reldir, f"{basename}-Edge_Cuts.dxf"),
                 make_output_file_path(reldir, f"{basename}-Edge_Cuts.svg")],
        rule=edge_cuts_rule,
    )
    ninja.newline()


def add_case_pcb_rules(ninja, variant, case, already_checked):
    for basename in CASE_BASENAMES[case]:
        case_dir = CASE_DIRS[case]
        if not (variant, case_dir, basename) in already_checked:
            add_drc_rule(ninja, f"{variant}/cases/{case_dir}", basename)
            add_render_front_rule(ninja, f"{variant}/cases/{case_dir}", basename)
            add_edge_cuts_rule(ninja, f"{variant}/cases/{case_dir}", basename)
            already_checked.add((variant, case_dir, basename))


def add_case_rules(ninja, variant):
    already_checked = set(())
    for case in CASES.get(variant, []):
        add_case_pcb_rules(ninja, variant, case, already_checked)


def add_shorthand_rule(ninja, variant):
    ninja.build(
        inputs=[
            make_output_file_path(variant, f)
            for f in [
                "gerbers.zip",
                "ferris_front.svg",
                "ferris_back.svg",
                "ibom.html",
                "bom_jlcpcb.csv",
                "cpl.csv",
            ]
        ],
        outputs=[variant],
        rule="phony",
    )


def add_0_1_shorthand_rule(ninja):
    ninja.build(inputs=VARIANTS_0_1, outputs=["0.1"], rule="phony")


def add_0_2_shorthand_rule(ninja):
    ninja.build(inputs=VARIANTS_0_2, outputs=["0.2"], rule="phony")


def generate_buildfile_content():
    ninja = Writer(open("build.ninja", "w"))
    variants = VARIANTS
    for variant in variants:
        add_comment_header(ninja, variant)
        add_render_front_rule(ninja, variant)
        add_render_back_rule(ninja, variant)
        add_interactive_bom_rule(ninja, variant)
        add_jlc_bom_rule(ninja, variant)
        add_pos_rule(ninja, variant)
        add_jlc_pick_and_place(ninja, variant)
        add_erc_rule(ninja, variant)
        add_keyboard_drc_rule(ninja, variant)
        add_gerber_rule(ninja, variant)
        add_zip_gerber_rule(ninja, variant)
        add_case_rules(ninja, variant)
        add_shorthand_rule(ninja, variant)
    add_0_1_shorthand_rule(ninja)
    add_0_2_shorthand_rule(ninja)
    return ninja


generate_buildfile_content()
