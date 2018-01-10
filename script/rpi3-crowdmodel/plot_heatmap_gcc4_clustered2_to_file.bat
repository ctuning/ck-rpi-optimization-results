del /Q /S plot_heatmap_gcc4_clustered2.pdf

call ck plot graph: @plot_heatmap_gcc4_clustered2_to_file.json @"init_reactions_tmp_heatmap_GCC_4.9.2_clustered2.json"

ck copy_file slide:rpi3-crowdmodeling-all-apps --file=plot_heatmap_gcc4_clustered2.pdf --new_name=8cb40f9e0ee52bcd.pdf
