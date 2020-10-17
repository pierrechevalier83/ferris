dir = '0.1/low'

gerbers_tgt = dir.underscorify() + '_gerbers'

gerbers_tgt_out = custom_target(gerbers_tgt,
              build_by_default: true,
              input : gerbers_in,
              output : gerbers_out,
              command : gerbers_cmd + ['-d', dir],)

gerbers_zip_tgt = gerbers_tgt + '_zip'
gerbers_zip = gerbers_tgt + '.zip'

custom_target(gerbers_zip_tgt,
              build_by_default: true,
              input : gerbers_tgt_out,
              output: gerbers_zip,
              command : zip_cmd,)

subdir_done()
