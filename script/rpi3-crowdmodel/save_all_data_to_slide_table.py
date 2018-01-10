#
# Collective Knowledge script
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net, 2017
#

import ck.kernel as ck
import sys
import os
import json
import math
import copy
import time

def main(i):

    # Load common table file (for all models)
    r=ck.load_json_file({'json_file':'save_all_model_data_tmp.json'})
    if r['return']>0: return r
    d=r['dict']

    # Get all models/features
    kk=list(d['GCC 4.9.2'])

    table=[]
    table_milepost=[]
    table_short=[]

    ikk=[]
    for k in kk:
        sort=0
        k1=k

        j=k.find('_depth_')
        if j>0:
           j1=k.find('_',j+7)
           if j1>0:
              sort=int(k[j+7:j1])
              k1=k[:j]

        j=k.find('_iteration_')
        if sort=='' and j>0:
           j1=k.find('_',j+11)
           if j1>0:
              sort=int(k[j+11:j1])
              k1=k[:j]

        ikk.append([k1,sort,k])

    for k1 in sorted(ikk, key=lambda x: (x[0],x[1])):
        k=k1[2]

        norm=False

        j=k.find('_ft')
        j1=k.find('_normalized')
        if j1>0:
           norm=True
           j=j1

        km=k[:j].replace('_',' ')
        if km.startswith('milepost'):
           ext=km[9:]
           if ext!='': ext=' ('+ext+')'
           km='milepost nn'+ext

        km=km.replace(' depth','; depth')
        km=km.replace(' iteration','; iteration')

        kf=k[j+1:]
        if norm:
           kf=kf[11:]+'\\newline'+'(normalized)'
        kf=kf.replace('_',' .. ')

        a4="%.2f" % d['GCC 4.9.2'][k]
        a7="%.2f" % d['GCC 7.1.0'][k]

        # Full table (for interactive report)
        line=[km,kf,a4,a7]
        table.append(line)

        # Shorter version for paper - ugly but didn't have time to make it nicer ;) 
        if 'depth 3' not in km and \
           'depth 5' not in km and \
           'depth 6' not in km and \
           'depth 7' not in km and \
           'depth 9' not in km and \
           'depth 10' not in km and \
           'depth 11' not in km and \
           'depth 12' not in km and \
           'depth 13' not in km and \
           'depth 14' not in km and \
           'depth 15' not in km and \
           'depth 17' not in km and \
           'depth 18' not in km and \
           'depth 19' not in km and \
           'depth 21' not in km and \
           'depth 22' not in km and \
           'depth 23' not in km and \
           'depth 24' not in km and \
           'depth 26' not in km and \
           'depth 27' not in km and \
           'depth 28' not in km and \
           'iteration 5' not in km and \
           'iteration 6' not in km and \
           'iteration 7' not in km and \
           'iteration 8' not in km and \
           'iteration 9' not in km:

           table_short.append(line)

        # Only short MILEPOST
        if km=='milepost nn' and kf=='ft1 .. ft56':
           table_milepost.append(line)

    dd={
         "table_style":"border=\"1\"",

         "table_header":[
                     {"name":"Model", "html_before":"<b>", "html_after":"</b>", "tex":"l", "tex_before":"\\textbf{", "tex_after":"}"}, 
                     {"name":"Features", "html_change_space":"yes", "tex":"p{1.2in}"},
                     {"name":"Accuracy (GCC 4.9.2)", "html_change_space":"yes", "tex":"p{0.9in}"},
                     {"name":"Accuracy (GCC 7.1.0)", "html_change_space":"yes", "tex":"p{0.9in}"} 
                    ]
      }

    # Save full table file (for all models)
    dd['table']=table

    r=ck.save_json_to_file({'json_file':'save_all_model_data_tmp_table_full.json', 'dict':dd, 'sort_keys':'yes'})
    if r['return']>0: return r

    # Save common table file (for all models)
    dd['table']=table_short

    r=ck.save_json_to_file({'json_file':'save_all_model_data_tmp_table_short.json', 'dict':dd, 'sort_keys':'yes'})
    if r['return']>0: return r

    # Save common table file (for all models)
    dd['table']=table_milepost

    r=ck.save_json_to_file({'json_file':'save_all_model_data_tmp_table_milepost.json', 'dict':dd, 'sort_keys':'yes'})
    if r['return']>0: return r


    return {'return':0}
    
##############################################################################
if __name__ == "__main__":
   r=main(sys.argv[1:])
   if r['return']>0: ck.err(r)

   exit(int(r['return']))
