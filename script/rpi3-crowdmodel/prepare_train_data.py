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

extract_missing_features=False

gcc=['GCC 4.9.2', 'GCC 7.1.0']

# Load info file
r=ck.load_json_file({'json_file':'init_reactions_tmp_info.json'})
if r['return']>0: ck.err(r)
info=r['dict']

all_classes=info['classes']

# Load features name
r=ck.access({'action':'load',
             'module_uoa':'module',
             'data_uoa':'program.static.features'})
if r['return']>0: ck.err(r)
features=r['dict']['milepost_features_description']
milepost_normalization_feature=r['dict']['milepost_normalization_feature']

# Searching for features
for g in gcc:
    ac=all_classes[g]

    gx=g.replace(' ','_')

    ftable=[]
    ctable=[]
    labels=info['opts'][g]

    for opt_class in sorted(ac):
        label=labels[opt_class]

        ck.out('Processing class '+str(label)+' ('+opt_class+')')

        for b in ac[opt_class]:
            bb=b['name']

            bx=bb.split(';')

            prog=bx[0].strip()
            cmd=bx[1].strip()

            # Process
            ck.out('')
            ck.out('* Processing '+prog+' ('+cmd+')')

            # Load program
            r=ck.access({'action':'load',
                         'module_uoa':'program',
                         'data_uoa':prog})
            if r['return']>0: ck.err(r)
            d=r['dict']
            puid=r['data_uid']
            ruid=r['repo_uid']

            run_cmds=d.get('run_cmds',{}).get(cmd,{})

            hot_spot=''
            hot_functions=run_cmds.get('hot_functions',{})
            if len(hot_functions)>0:
               sorted_hot_functions=sorted(hot_functions, key=lambda x: float(x['percent']), reverse=True)
               hot_spot=sorted_hot_functions[0]['name']

               ck.out('  Hotspot: '+hot_spot) 

            if hot_spot=='':
               ck.out('  WARNING: hotspot not found')

            # Checking features
            r=ck.access({'action':'load',
                         'module_uoa':'program.static.features',
                         'data_uoa':puid})
            if r['return']>0 and r['return']!=16: ck.err(r)

            if r['return']==16:
               ck.out('  WARNING: MILEPOST features not found ...')

               if extract_missing_features:
                  r=ck.access({'action':'extract',
                               'module_uoa':'program.static.features',
                               'data_uoa':prog,
                               'repo_uod':ruid,
                               'target_repo_uoa':'upload',
                               'out':'con'})
                  if r['return']>0:
                     ck.out('CK WARNING: feature extraction failed!')
            else:
               df=r['dict']

               ft=df.get('features',{}).get('program_static_milepost_features',{}).get(hot_spot,{})
               if len(ft)==0:
                  ck.out('CK WARNING: extracted features for the hot spot are not found!')
               else:
                  # Convert dict features to vector (for unified CK modeling such as via DNN TensorFlow)
                  utf=[]
                  for q in range(1,65+1):
                      q1=str(q)
                      if q1 in ft:
                         utf.append(ft[q1])

                  # Add normalized features (ft1..ft56 / ft24)
                  nf=ft['24']
                  for q in range(1,56+1):
                      v=0.0
                      if nf>0:
                         v=float(ft[str(q)])/float(nf)
                      utf.append(v)

                  ftable.append(utf)
                  ctable.append([label])

        # Increase label
        label=label+1

    # Prepare features
    fkeys=[]
    ffkd={}

    for q in range(1,65+1):
        ffkd[q]={'name':features[str(q)]['desc']} # Add real name
        fkeys.append('ft'+str(q))

    for q in range(1,56+1):
        q1=65+q
        fkeys.append('ft'+str(q1))
        ffkd[q1]={'name':'Normalized '+features[str(q)]['desc']+' (by ft24)'} # Add real name

    # Recording input for model such as TensorFlow DNN
    r=ck.save_json_to_file({'json_file':'prepare_train_data_tmp.'+gx+'.json',
                            'dict':{'ftable':ftable, 'fkeys':fkeys, 'features_flat_keys_desc': ffkd,
                            'ctable':ctable,   "ckeys": ["Optimization class"], 'optimization_classes':labels}})
    if r['return']>0: ck.err(r)
