#
# Collective Knowledge script
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net, 2017
#

import ck.kernel as ck
import os
import json
import copy
import sys

gcc=['GCC 4.9.2', 'GCC 7.1.0']

def main(i):

    # Load common table file (for all models)
    ddd={}
    r=ck.load_json_file({'json_file':'save_all_model_data_tmp.json'})
    if r['return']==0:
       ddd=r['dict']

    # Searching for features
    for g in gcc:
        ck.out('********************************************************************************')
        ck.out('Preparing accuracy graph for '+g)
        ck.out('')

        gx=g.replace(' ','_')

        d=ddd[g]

        table={"0":[], "1":[]}

        for depth in range(1,30):
            key1='decision_trees_with_cross_validation_depth_'+str(depth)+'_ft1_ft65'
            key2='decision_trees_without_cross_validation_depth_'+str(depth)+'_ft1_ft65'
            
            acc1=d[key1]
            acc2=d[key2]

            table["0"].append([depth,acc1])
            table["1"].append([depth,acc2])

        # Graph input
        ii={
              "action":"plot",
              "module_uoa":"graph",

              "table":table,

              "add_x_loop":"no",

              "ignore_point_if_none":"yes",

              "plot_type":"mpl_2d_scatter",

              "display_y_error_bar":"no",

              "title":"Powered by Collective Knowledge",

              "axis_x_desc":"Decision tree depth",
              "axis_y_desc":"Model accuracy for "+g+" (%)",

              "plot_grid":"yes",

              "mpl_image_size_x":"12",
              "mpl_image_size_y":"6",
              "mpl_image_dpi":"100",

              "font_size":22,

              "out_to_file":'process_model_using_decision_trees_accuracy_graph_output.'+gx+'.pdf',

              "point_style":{"0":{"marker":"o"},
                             "1":{"marker":"x"}}
           }

        # Save common data (continuously, not to loose data)
        r=ck.save_json_to_file({'json_file':'process_model_using_decision_trees_accuracy_graph_input.'+gx+'.json', 'dict':ii})
        if r['return']>0: return r

        # Plot graph (save to pdf)
        r=ck.access(ii)
        if r['return']>0: return r

    return {'return':0}

##############################################################################
if __name__ == "__main__":
   r=main(sys.argv[1:])
   if r['return']>0: ck.err(r)

   exit(int(r['return']))
