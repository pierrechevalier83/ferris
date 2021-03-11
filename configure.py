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
PCBDRAW_DIR = "tools/PcbDraw/pcbdraw"
KIPLOT_DIR = "tools/kiplot/src/kiplot"
IBOM_DIR = "tools/InteractiveHtmlBom/InteractiveHtmlBom"
JLCBOM_DIR = "tools/kicad-jlcpcb-bom-plugin"
RENDER_COLORS = {
    "0.1/base": "white",
    "0.1/compact": "white",
    "0.1/high": "yellow",
    "0.1/low": "blue",
    "0.2/bling": "white",
    "0.2/compact": "white",
    "0.2/high": "yellow",
    "0.2/mini": "blue",
}
CASE_DIRS = {
    "mid_profile_with_puck": "mid_profile",
    "mid_profile_without_puck": "mid_profile",
}
CASE_BASENAMES = {
    "mid_profile_with_puck": [
        "top_left_plate_with_puck",
        "top_right_plate_with_puck",
        "mid_plate",
        "bottom_plate_with_puck",
    ],
    "mid_profile_without_puck": [
        "top_left_plate_without_puck",
        "top_right_plate_without_puck",
        "mid_plate",
        "bottom_plate_without_puck",
    ],
}
CASES = {
    "0.2/bling": ["mid_profile_with_puck", "mid_profile_without_puck"],
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


def make_rule_name(variant, suffix):
    return f"{underscorify(variant)}_{suffix}"


def make_variant_out_dir(variant):
    return f"{OUTPUT_DIR}/{variant}"


def make_output_file_path(variant, filename):
    return f"{make_variant_out_dir(variant)}/{filename}"


def add_render_rule(ninja, variant):
    pcbdraw = f"{PCBDRAW_DIR}/pcbdraw.py"
    color = RENDER_COLORS[variant]
    style = f"{PCBDRAW_DIR}/styles/set-{color}-enig.json"
    pcb = make_pcb_file_name(variant, "ferris")
    render_front = make_rule_name(variant, "render_front")
    front_svg = make_output_file_path(variant, "front.svg")
    ninja.rule(
        name=render_front,
        command=[f"python3 {pcbdraw} --style {style} {pcb} {front_svg}"],
    )
    ninja.build(
        inputs=[pcbdraw, style, pcb],
        outputs=[front_svg],
        rule=make_rule_name(variant, "render_front"),
    )
    render_back = make_rule_name(variant, "render_back")
    back_svg = make_output_file_path(variant, "back.svg")
    ninja.rule(
        name=render_back,
        command=[f"python3 {pcbdraw} --style {style} {pcb} {back_svg} --back"],
    )
    ninja.build(
        inputs=[pcbdraw, style, pcb],
        outputs=[back_svg],
        rule=make_rule_name(variant, "render_back"),
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
        command=[f"./run_ibom.sh {variant}"],
    )
    ninja.build(
        inputs=["./run_ibom.sh", ibom_generator, pcb, raw_bom],
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
        command=[f"python3 ./tools/generate_pos.py {pcb} > {pos_file}"],
    )
    ninja.build(
        inputs=["./tools/generate_pos.py", pcb],
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
    # On success, we create a file which informs the next rule that it's ok to proceed. We don't want to generate gerber files if ERC fails.
    erc_file = make_output_file_path(variant, "erc_success")
    ninja.rule(
        name=erc_rule,
        command=[f"./run_erc.sh {variant}"],
    )
    ninja.build(
        inputs=["./run_erc.sh", make_sch_file_name(variant)],
        outputs=[erc_file],
        rule=erc_rule,
    )
    ninja.newline()


def add_drc_rule(ninja, rel_dir, basename):
    drc_rule = make_rule_name(f"{rel_dir}/{basename}", "drc")
    pcb_file = make_pcb_file_name(rel_dir, basename)
    ninja.rule(
        name=drc_rule,
        command=[f"./run_drc.sh {pcb_file}"],
    )
    ninja.build(
        inputs=["./run_drc.sh", f"{pcb_file}"],
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
        "ferris-Edge_Cuts.gbr",
        "ferris-F_Cu.gbr",
        "ferris-F_Mask.gbr",
        "ferris-F_Paste.gbr",
        "ferris-F_SilkS.gbr",
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
        outputs=make_gerber_output_paths(variant),
        rule=gerber_rule,
    )
    ninja.newline()


def add_zip_gerber_rule(ninja, variant):
    zip_gerber_rule = make_rule_name(variant, "gerbers_zip")
    zip_file = make_output_file_path(variant, "gerbers.zip")
    gerber_files = make_gerber_output_paths(variant)
    gerber_rule = make_rule_name(variant, "gerbers")
    ninja.rule(name=zip_gerber_rule, command=[f"zip -j -r {zip_file}"] + gerber_files)
    ninja.build(
        inputs=[
            make_output_file_path(variant, "erc_success"),
            make_drc_success_file_name(variant, "ferris"),
        ]
        + gerber_files,
        outputs=zip_file,
        rule=zip_gerber_rule,
    )
    ninja.newline()


def add_case_drc_rules(ninja, variant, case, already_checked):
    for basename in CASE_BASENAMES[case]:
        case_dir = CASE_DIRS[case]
        if not (variant, case_dir, basename) in already_checked:
            add_drc_rule(ninja, f"{variant}/cases/{case_dir}", basename)
            already_checked.add((variant, case_dir, basename))


def add_case_rules(ninja, variant):
    already_checked = set(())
    for case in CASES.get(variant, []):
        add_case_drc_rules(ninja, variant, case, already_checked)


def add_shorthand_rule(ninja, variant):
    ninja.build(
        inputs=[
            make_output_file_path(variant, f)
            for f in [
                "gerbers.zip",
                "front.svg",
                "back.svg",
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
        add_render_rule(ninja, variant)
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
