#
# Collective Knowledge script
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net, 2017
#

max_dataset=20

import ck.kernel as ck

r=ck.access({'action':'search',
             'module_uoa':'program',
             'add_meta':'yes',
             'tags':'crowd-tuning'})
if r['return']>0: ck.err(r)
lst=r['lst']

r=ck.access({'action':'search',
             'module_uoa':'program',
             'add_meta':'yes',
             'tags':'milepost'})
if r['return']>0: ck.err(r)
for q in r['lst']:
    duoa=q['data_uoa']
    found=False
    for qq in lst:
        if duoa==qq['data_uoa']:
           found=True
           break
    if not found:
       lst.append(q)

im=len(lst)
iq=0

for q in sorted(lst, key=lambda x: x['data_uoa']):
    iq+=1

    # Reuse experiments if failed
#    if iq<21: continue

    duoa=q['data_uoa']

    meta=q['meta']

    cmds=meta['run_cmds']

    for cmd in cmds:

        vcmd=cmds[cmd]

        # 7e149c8504752933 - gcc 4.9.2
        # 4f11abfefd3cc031 - gcc 7.1.0
#        for xgcc in ['gcc4','gcc7']:
        for xgcc in ['gcc7']:

            if xgcc=='gcc4': gcc='7e149c8504752933'
            elif xgcc=='gcc7': gcc='4f11abfefd3cc031'

            # Check if takes datasets from CK and prepare selection
            idataset=0

            dtags=vcmd.get('dataset_tags',[])
            if len(dtags)>0:
               ii={'action':'search',
                   'module_uoa':'dataset',
                   'add_meta':'yes'}

               tags=''
               for q in dtags:
                   if tags!='': tags+=','
                   tags+=q

               ii['tags']=tags

               rx=ck.access(ii)
               if rx['return']>0: ck.err(rx)

               dlst=rx['lst']

               if len(dlst)<2: continue # only run ones with multiple datasets

               # Iterate over datasets and check data files
               for dataset in sorted(dlst, key=lambda x: x.get('data_uoa','')):
                   dduoa=dataset['data_uoa']
                   dduid=dataset['data_uid']

                   dd=dataset['meta']

                   dfiles=dd.get('dataset_files',[''])

                   # Iterate over data files
                   for dfile in dfiles:
                       idataset+=1

                       if idataset>max_dataset:
                          break

                       ck.out('-------------------')
                       ck.out('Program        '+str(iq)+' of '+str(im))
                       ck.out('')
                       ck.out('Program:      '+duoa)
                       ck.out('CMD:          '+cmd)
                       ck.out('Dataset:      '+dduoa)
                       ck.out('Dataset file: '+dfile)
                       ck.out('Dataset No:   '+str(idataset))
                       ck.out('Compiler:     '+gcc)

                       ii={'action':'autotune',
                           'module_uoa':'program',
                           'data_uoa':duoa,
                           'dataset_uoa':dduid,
                           'iterations':1,
                           'repetitions':2,
                           'scenario':'9d88674c45b94971',
                           'compiler_env_uoa':gcc,
                           'seed':12345,
                           'solution_module_uoa':'8289e0cf24346aa7',
                           'solution_repo_uoa':'remote-ck',
                           'cmd_key':cmd,
                           'quiet':'yes',
                           'record_uoa':'rpi3-all-'+duoa+'-'+cmd+'-'+xgcc+'-'+dduid+'-'+dfile+'-cbest',
                           'tags':duoa+','+cmd+','+xgcc+','+dduid+','+dfile+',multi-datasets,reactions,'+str(max_dataset)+' datasets,top optimizations',
                           'out':'con'}

                       r=ck.access(ii)
                       # Ignore output

                   if idataset>max_dataset:
                      break
