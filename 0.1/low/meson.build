dir = '0.1/low'
gerbers_tgt = dir.underscorify() + '_gerbers'

custom_target(gerbers_tgt,
              build_by_default: true,
              input : gerbers_in,
              output : gerbers_out,
              command : gerbers_cmd + ['-d', dir],)

subdir_done()

