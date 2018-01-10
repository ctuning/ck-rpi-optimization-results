del /Q /S plot_heatmap_gcc4_clustered.pdf

call ck plot graph: @plot_heatmap_gcc4_clustered_to_file.json @"init_reactions_tmp_heatmap_GCC_4.9.2_clustered.json"

ck copy_file slide:rpi3-crowdmodeling-all-apps --file=plot_heatmap_gcc4_clustered.pdf --new_name=ba5ecb7074b4985a.pdf
