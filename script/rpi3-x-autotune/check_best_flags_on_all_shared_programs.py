#
# Collective Knowledge script
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net, 2017
#

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
    duoa=q['data_uoa']

    meta=q['meta']

    cmds=meta['run_cmds']

    for cmd in cmds:

        # 7e149c8504752933 - gcc 4.9.2
        # 4f11abfefd3cc031 - gcc 7.1.0
        for xgcc in ['gcc4','gcc7']:

            if xgcc=='gcc4': gcc='7e149c8504752933'
            elif xgcc=='gcc7': gcc='4f11abfefd3cc031'

            ck.out('-------------------')
            ck.out('Program   '+str(iq)+' of '+str(im))
            ck.out('Program:  '+duoa)
            ck.out('CMD:      '+cmd)
            ck.out('Compiler: '+gcc)

            ii={'action':'autotune',
                'module_uoa':'program',
                'data_uoa':duoa,
                'iterations':1,
                'repetitions':2,
                'scenario':'9d88674c45b94971',
                'compiler_env_uoa':gcc,
                'seed':12345,
                'solution_module_uoa':'8289e0cf24346aa7',
                'solution_repo_uoa':'remote-ck',
                'cmd_key':cmd,
                'quiet':'yes',
                'record_uoa':'rpi3-all-'+duoa+'-'+cmd+'-'+xgcc+'-cbest',
                'out':'con'}

            r=ck.access(ii)
            # Ignore output