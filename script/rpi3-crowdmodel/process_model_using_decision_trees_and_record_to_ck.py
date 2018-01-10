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
best_depth=[8,4]

def main(i):

    # Load common table file (for all models)
    ddd={}
    r=ck.load_json_file({'json_file':'save_all_model_data_tmp.json'})
    if r['return']==0:
       ddd=r['dict']

    # Searching for features
    for gi in range(0,len(gcc)):
        g=gcc[gi]
        depth=best_depth[gi]

        ck.out('********************************************************************************')
        ck.out('Modeling optimizations for '+g)
        ck.out('')

        if g not in ddd: ddd[g]={}

        gx=g.replace(' ','_')
        gx2=g.replace(' ','-')

        r=ck.load_json_file({'json_file':'prepare_train_data_tmp.'+gx+'.json'})
        if r['return']>0: ck.err(r)

        d=r['dict']

        ftable=d['ftable']
        ctable=d['ctable']

        s='==============================================================\n'
        s+='Depth: '+str(depth)+'\n\n'

        ck.out(s)

        # Building decision tree on all data
        ck_model_entry_name="rpi3-milepost-model-"+gx2.lower()

        ii={'action':'build',
            'module_uoa':'model',

            'ftable':ftable,
            'ctable':ctable,

            'keep_temp_files':'yes',

            "model_module_uoa":"model.sklearn",
            "model_name":"dtc",
            "model_file":"tmp-model-sklearn-dtc",
            "model_params":{"max_depth":depth},

            "model_repo_uoa":"ck-rpi-optimization-results",
            "model_data_uoa":ck_model_entry_name,

            "out":""}

        # Training
        cii=copy.deepcopy(ii)

        r=ck.access(ii)
        if r['return']>0: ck.err(r)

        # Validating
        ii=copy.deepcopy(ii)

        ii['action']='validate'

        r=ck.access(ii)
        if r['return']>0: ck.err(r)

        obs=r['observations']
        wrong=r['mispredictions']

        acc=float(obs-wrong)/float(obs)

        x='  Accuracy on all data: '+str(acc)
        s+=x
        ck.out(x)

        # Record example of features to demo predictions (to be integrated with compiler optimization prediction (web)services)
        d={
            "action":"use",
            "module_uoa":"model",

            "features": ftable[123], # features of some random benchmark

            "model_module_uoa":"model.sklearn",
            "model_name":"dtc",
            "model_file":"tmp-model-sklearn-dtc",
            "model_data_uoa":ck_model_entry_name
          }

        r=ck.save_json_to_file({'json_file':'process_model_using_decision_trees_and_record_to_ck_use.'+gx+'.json',
                                'dict':d})
        if r['return']>0: return r

    return {'return':0}

##############################################################################
if __name__ == "__main__":
   r=main(sys.argv[1:])
   if r['return']>0: ck.err(r)

   exit(int(r['return']))
