del /Q /S plot_heatmap_gcc7_clustered.pdf

call ck plot graph: @plot_heatmap_gcc7_clustered_to_file.json @"init_reactions_tmp_heatmap_GCC_7.1.0_clustered.json"

ck copy_file slide:rpi3-crowdmodeling-all-apps --file=plot_heatmap_gcc7_clustered.pdf --new_name=29119378e09b4dc8.pdf
