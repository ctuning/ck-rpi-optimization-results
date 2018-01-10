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

        # Normalize (all features 0..1)
        ftable_range={}
        for f in ftable:
            for k in range(0,121):
                v=f[k]
                if k not in ftable_range:
                   ftable_range[k]={'min':None, 'max':None}
                if ftable_range[k]['min']==None or v<ftable_range[k]['min']:
                   ftable_range[k]['min']=v
                if ftable_range[k]['max']==None or v>ftable_range[k]['max']:
                   ftable_range[k]['max']=v

        ftable_normalized=[]
        for f in ftable:
            x=[]
            for k in range(0,121):
                v=0
                if ftable_range[k]['max']!=0:
                   v=f[k]/ftable_range[k]['max']
                x.append(v)
            ftable_normalized.append(x)

        features_mask=[]
        for f in range(0, 121):
            features_mask.append(1)

        r=model({'ftable':ftable_normalized,
                 'features_mask':features_mask,
                 'ctable':ctable})
        if r['return']>0: return r

        r1=ck.save_json_to_file({'json_file':'process_model_using_nearest_neighbour_reduce_features/prepare_reactions_model_train_ref_result.'+gx+'.json',
                                'dict':r})
        if r1['return']>0: ck.err(r1)

        ref_acc=r['accuracy'] # Reference accuracy

        x='Reference accuracy: '+str(ref_acc)
        s=x+'\n\n'

        ck.out('---------------------')
        ck.out(x)
        ck.out('')

        # Calculating Euclidean distance as in our MILEPOST GCC paper: https://hal.inria.fr/hal-00685276
        # MILPOST features: https://github.com/ctuning/ck-autotuning/blob/master/module/program.static.features/.cm/meta.json
        # 0..55 - original MILEPOST features
        # 56..64 - added by Jeremy Singer
        # 65..121 - 0..55/ft24 (normalized by total number of instructions)

        for k in range(0, 121):
            features_mask[k]=0

            r=model({'ftable':ftable_normalized,
                     'features_mask':features_mask,
                     'ctable':ctable,
                     'skip_out':'yes'})
            if r['return']>0: return r

            acc=r['accuracy']

            keep=False
            sx=''
            if acc<ref_acc:
               keep=True
               sx='kept'
            elif acc==ref_acc:
               sx='removed'
            elif acc>ref_acc:
               ref_acc=acc
               sx='removed (accuracy even improved)'

            if keep:
               features_mask[k]=1

            x='ft'+str(k+1)+') '+str(acc)+' '+sx+' (ref acc='+str(ref_acc)+')'
            ck.out(x)
            s+=x+'\n'

        # Final accuracy
        r=model({'ftable':ftable_normalized,
                 'features_mask':features_mask,
                 'ctable':ctable,
                 'skip_out':'yes'})
        if r['return']>0: return r

        acc=r['accuracy']

        r1=ck.save_json_to_file({'json_file':'process_model_using_nearest_neighbour_reduce_features/prepare_reactions_model_train_reduced_result.'+gx+'.json',
                                'dict':r})
        if r1['return']>0: ck.err(r1)

        # Final result
        ck.out('')
        ck.out('Final features mask:')
        ck.out('')

        s+='\nFinal features mask:\n\n'

        for f in range(0, len(features_mask)):
            x='  ft'+str(f+1)+') '+str(features_mask[f])
            ck.out(x)
            s+=x+'\n'

        s+='\nFinal features mask:\n\n'
        s1=''

        for f in range(0, len(features_mask)):
            x='  ft'+str(f+1)+') '+str(features_mask[f])
            ck.out(x)
            s+=x+'\n'

            if features_mask[f]==1:
               if s1!='': s1+=','
               s1+='ft'+str(f+1)

        s+='\nFinal accuracy: '+str(acc)+'\n'

        r=ck.save_text_file({'text_file':'process_model_using_nearest_neighbour_reduce_features/log.'+gx+'.txt', 'string':s})
        if r['return']>0: return r

        r=ck.save_text_file({'text_file':'process_model_using_nearest_neighbour_reduce_features/influential_features.'+gx+'.txt', 'string':s1})
        if r['return']>0: return r

        ddd[g]['milepost_reduce_complexity2_normalized_ft1_ft121']=acc

    # Save common data
    r=ck.save_json_to_file({'json_file':'save_all_model_data_tmp.json', 'dict':ddd})
    if r['return']>0: return r

    return {'return':0}

##############################################################################
def model(i):

    so=i.get('skip_out','')

    acc=0
    obs=0
    good=0
    good_top3=0

    ftable=i['ftable']
    features_mask=i.get('features_mask',[])
    ctable=i['ctable']

    pctable=[] # predictions
    pctable_all=[] # all
    edistance=[] # Euclidean distance
    similarity=[] # Similar program

    for q in range(0, len(ftable)):
        obs+=1
        
        ft=ftable[q]
        c=ctable[q]

        # search the most close features
        ed_min=-1
        similar=-1

        distances={}

        # Calculating Euclidean distance as in our MILEPOST GCC paper: https://hal.inria.fr/hal-00685276
        for k in range(0, len(ftable)):
            ft2=ftable[k]

            if k!=q:
               dist=0.0
#               for f in range(65, 121):
               for f in range(0, 121):
                   if len(features_mask)==0 or features_mask[f]==1:
                      dist+=pow((float(ft2[f])-float(ft[f])),2)

               ed=math.sqrt(dist)

               distances[k]=ed

               if ed_min==-1 or ed<ed_min: 
                  ed_min=ed
                  similar=k

        # Sort distances
        dd=sorted(distances, key=lambda x: distances[x])

        c2a=ctable[dd[0]]
        c2b=ctable[dd[1]]
        c2c=ctable[dd[2]]

#        ck.out('')
#        ck.out('Program (original and most similar): '+str(q)+' -> '+str(similar))
#        ck.out('Opt class (original and predicted top3):  '+str(c[0])+' -> '+str(c2a[0])+' or '+str(c2b[0])+' or '+str(c2c[0]))

        similarity.append(similar)

        pctable.append(c2a[0])

        x=[]
        for k in dd:
            x.append(ctable[k][0])
        pctable_all.append(x)

        x=[]
        for k in dd:
            x.append(distances[k])
        edistance.append(x)

        if int(c[0])==int(c2a[0]):
           good+=1

        if int(c[0])==int(c2a[0]) or int(c[0])==int(c2b[0]) or int(c[0])==int(c2c[0]):
           good_top3+=1

    wrong=obs-good
    wrong_top3=obs-good_top3
    acc=good/obs
    acc_top3=good_top3/obs

    info={'pctable':pctable,
          'pctable_all':pctable_all,
          'edistance':edistance,
          'similarity':similarity}

    if so!='yes':
       ck.out('')
       ck.out('Observations:          '+str(obs))
       ck.out('')
       ck.out('Mispredictions:        '+str(wrong))
       ck.out('Accuracy:              '+str(acc))
       ck.out('')
       ck.out('Mispredictions (top3): '+str(wrong_top3))
       ck.out('Accuracy (top3):       '+str(acc_top3))

#       ck.out('')
#       ck.inp({'text':'Press Enter to continue ...'})

    return {'return':0, 'accuracy':acc, 'accuracy_top3':acc_top3, 'observations':obs,
                        'wrong':wrong, 'wrong_top3':wrong_top3, 'info':info}
    
##############################################################################
if __name__ == "__main__":
   r=main(sys.argv[1:])
   if r['return']>0: ck.err(r)

   exit(int(r['return']))
