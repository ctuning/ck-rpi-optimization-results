del /Q /S plot_heatmap_gcc7_clustered2.pdf

call ck plot graph: @plot_heatmap_gcc7_clustered2_to_file.json @"init_reactions_tmp_heatmap_GCC_7.1.0_clustered2.json"

ck copy_file slide:rpi3-crowdmodeling-all-apps --file=plot_heatmap_gcc7_clustered2.pdf --new_name=2d416955df7546b1.pdf
