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

def main(i):

    # Load data
    r=ck.load_json_file({'json_file':'autotune_for_input_aware_blas_fixed.json'})
    if r['return']>0: return r
    ddd=r['dict']

    table={"0":[], "1":[]}

    # Find RPi3
    found=False
    for a in ddd.get('all',[]):
        if a.get('cpu_name','')=='BCM2709':
           found=True
           break

    if not found:
       return {'return':1, 'error':'RPi3 data not found'}

    data=a.get('data',{})

    for N in sorted(data, key=lambda x: int(x)):
        results=data[N]

        gflops_default=None
        tmin_default=None
        
        gflops_best=None
        tmin_best=None

        for BS in sorted(results, key=lambda x: int(x)):
            x=results[BS]

            tmin=x['tmin']
            gflops=x['gflops']

            if BS==N:
               gflops_default=gflops
               tmin_default=tmin

               table['0'].append([int(N),gflops_default])
            else:
               if gflops_best==None or gflops>gflops_best:
                  gflops_best=gflops
                  tmin_best=tmin

        if gflops_best!=None:
           table['1'].append([int(N),gflops_best])

    # Graph input
    ii={
          "action":"plot",
          "module_uoa":"graph",

          "table":table,

          "plot_type":"mpl_2d_scatter",

#          "title":"Powered by Collective Knowledge",

          "axis_x_desc":"Square matrix size",
          "axis_y_desc":"GFLOPS",

          "plot_grid":"no",

          "mpl_image_size_x":"12",
          "mpl_image_size_y":"6",
          "mpl_image_dpi":"100",

          "font_size":22,

#          "out_to_file":'process_data_and_plot_graph_out.pdf',

          "point_style":{"0":{"marker":"o"},
                         "1":{"marker":"x"}}
       }

    # Save common data (continuously, not to loose data)
    r=ck.save_json_to_file({'json_file':'process_data_and_plot_graph_out.json', 'dict':ii})
    if r['return']>0: return r

    return {'return':0}

##############################################################################
if __name__ == "__main__":
   r=main(sys.argv[1:])
   if r['return']>0: ck.err(r)

   exit(int(r['return']))
