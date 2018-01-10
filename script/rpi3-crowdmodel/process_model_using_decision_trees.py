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
        ck.out('Modeling optimizations for '+g)
        ck.out('')

        if g not in ddd: ddd[g]={}

        gx=g.replace(' ','_')

        r=ck.load_json_file({'json_file':'prepare_train_data_tmp.'+gx+'.json'})
        if r['return']>0: ck.err(r)

        d=r['dict']

        ftable=d['ftable']
        ctable=d['ctable']

        s=''

        for depth in range(1,30):
            # Full cross-validation
            acc=0
            obs=0
            wrong=0

            acc_min=None
            acc_max=None

            s='==============================================================\n'
            s+='Depth: '+str(depth)+'\n\n'

            ck.out(s)
  
            for n in range(0,3): # Trying to build model N times (random - sometimes slightly different result)

                # Building decision tree on all data
                ii={'action':'build',
                    'module_uoa':'model',

                    'ftable':ftable,
                    'ctable':ctable,

                    'keep_temp_files':'yes',

                    "model_module_uoa":"model.sklearn",
                    "model_name":"dtc",
                    "model_file":"process_model_using_decision_trees/model-sklearn-dtc-"+gx+'-depth'+str(depth),
                    "model_params":{"max_depth":depth},

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

                obs+=r['observations']
                wrong+=r['mispredictions']

                acc=float(obs-wrong)/float(obs)

                x='  Accuracy on all data ('+str(n+1)+' out of 3):   '+str(acc)
                s+=x
                ck.out(x)

                acc=float(obs-wrong)/float(obs)

                if acc_min==None or acc<acc_min: 
                   acc_min=acc

                if acc_max==None or acc>acc_max: 
                   acc_max=acc

            x='\nDepth: '+str(depth)+' ; accuracy (min/max): '+'%.2f'%acc_min+' .. '+'%.2f'%acc_max+'\n'
            s+=x
            ck.out(x)

            # Cross-validating (for simplicity 1 run)
            cross_obs=0
            cross_wrong=0

            x='  *************************************************\n'
            x+='  Cross-validating model (leave one out)\n\n'
            s+=x
            ck.out(x)

            for bench in range(0, len(ftable)):
                train_ftable=[]
                train_ctable=[]
                test_ftable=[]
                test_ctable=[]

                for k in range(0,len(ftable)):
                    if k!=bench:
                       train_ftable.append(ftable[k])
                       train_ctable.append(ctable[k])
                    else:
                       test_ftable.append(ftable[k])
                       test_ctable.append(ctable[k])

                # Selecting model
                ii={'action':'build',
                    'module_uoa':'model',

                    'ftable':train_ftable,
                    'ctable':train_ctable,

                    'keep_temp_files':'no',

                    "model_module_uoa":"model.sklearn",
                    "model_name":"dtc",
                    "model_file":"tmp-model-sklearn-dtc",
                    "model_params":{"max_depth":depth},

                    "out":""}

                # Training
                cii=copy.deepcopy(ii)

                r=ck.access(ii)
                if r['return']>0: ck.err(r)

                # Validating
                ii=copy.deepcopy(ii)

                ii['action']='validate'
                ii['ftable']=test_ftable
                ii['ctable']=test_ctable

                r=ck.access(ii)
                if r['return']>0: ck.err(r)

                cross_obs+=r['observations']
                cross_wrong+=r['mispredictions']

                cross_acc=float(cross_obs-cross_wrong)/float(cross_obs)

                x='    '+str(bench)+' out of '+str(len(ftable))+' ) current cross-validation accuracy: '+'%.2f'%cross_acc
                s+=x
                ck.out(x)

            x='\nDepth: '+str(depth)+' ; accuracy (with cross-validation): '+'%.2f'%cross_acc+'\n'
            s+=x
            ck.out(x)

            ddd[g]['decision_trees_with_cross_validation_depth_'+str(depth)+'_ft1_ft65']=cross_acc
            ddd[g]['decision_trees_without_cross_validation_depth_'+str(depth)+'_ft1_ft65']=acc_max

        r=ck.save_text_file({'text_file':'process_model_using_decision_trees/log.'+gx+'.txt', 'string':s})
        if r['return']>0: return r

        # Save common data (continuously, not to loose data)
        r=ck.save_json_to_file({'json_file':'save_all_model_data_tmp.json', 'dict':ddd})
        if r['return']>0: return r

    return {'return':0}

##############################################################################
if __name__ == "__main__":
   r=main(sys.argv[1:])
   if r['return']>0: ck.err(r)

   exit(int(r['return']))
