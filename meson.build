project('ferris')


# Describe the arguments to kiplot from the point of view of a variant subdirectory.
# These are common to all variants, so it makes sense to declare them here to minimize duplication.

gerbers_in = ['ferris.kicad_pcb', files('.kiplot.yml')]

gerbers_out = ['ferris-B_Cu.gbr', 'ferris-B_Mask.gbr', 'ferris-B_Paste.gbr', 'ferris-B_SilkS.gbr', 'ferris-Edge_Cuts.gbr', 'ferris-F_Cu.gbr', 'ferris-F_Mask.gbr', 'ferris-F_Paste.gbr', 'ferris-F_SilkS.gbr']

gerbers_cmd = [find_program('kiplot'), '-b', '@INPUT0@', '-c', '@INPUT1@']

# Custom targets for each subdirectory will be declared in the subdirectories as it is the only way for the relative paths to be evaluated correctly in the context of each subdirectory

subdir('0.1/base')
subdir('0.1/compact')
subdir('0.1/high')
subdir('0.1/low')
subdir('0.2/bling')
subdir('0.2/compact')
subdir('0.2/high')
subdir('0.2/mini')
