#
# Collective Knowledge script to demo input-aware autotuning with various features (CPU/platforms/freq, etc)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net, 2017
#

import ck.kernel as ck
import os
import random
import math
import copy

line='*****************************************************************'

aggregated_stats='autotune_for_input_aware_blas.json'
aggregated_stats_small='autotune_for_input_aware_blas_small.json'
aggregated_stats_large='autotune_for_input_aware_blas_large.json'

def main(i):

    cur_dir=os.getcwd()
    fas=os.path.join(cur_dir,aggregated_stats)

    # Get some info about current platform
    ii={'action':'detect',
        'module_uoa':'platform',
        'out':'con'}

    r=ck.access(ii)
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    cpu_name=r['features']['cpu']['name']
    plat_name=r['features']['platform']['name']

    #############################################################
    ck.out(line)
    ck.out('CPU name: '+cpu_name)
    ck.out('Plat name: '+plat_name)

    #############################################################
    ck.out(line)
    ck.out('Loading aggregated stats ...')

    aa=[]
    if os.path.isfile(fas):
       r=ck.load_json_file({'json_file':fas})
       if r['return']>0: return r
       ax=r['dict']

       if 'all' not in ax: ax['all']=[]
       aa=ax['all']

    #############################################################
    ck.out(line)
    ck.out('Finding entry related to this platform ...')

    found=False
    for a in aa:
        if a.get('cpu_name','')==cpu_name and a.get('plat_name','')==plat_name:
           found=True

    if not found:
       a={'cpu_name':cpu_name, 'plat_name':plat_name}
       aa.append(a)

    if 'data' not in a: a['data']={}
    data=a.get('data',{})

    # Init pipeline
    r=ck.access({'action':'pipeline',
                 'module_uoa':'program',
                 'data_uoa':'shared-matmul-c2',
                 'cpu_freq':'max',
                 'gpu_freq':'max',
                 'speed':'yes',
                 'compiler_vars': {'USE_BLOCKED_MATMUL':'YES'},
                 'no_state_check':'yes',
                 'prepare':'yes',
                 'out':'con'})
    if r['return']>0: return r

    ready=r['ready']
    if ready!='yes':
       return {'return':1, 'error':'can\'t init pipeline'}

    pipeline=r

    # Compile program ones
    tpipeline=copy.deepcopy(pipeline)
    r=ck.access({'action':'autotune',
                 'module_uoa':'pipeline',
                 'pipeline':pipeline,
                 'pipeline_update':{
                 'env':{'CT_MATRIX_DIMENSION':16,
                        'CT_BLOCK_SIZE':16}
                        },
                 'iterations':1,
                 'repetitions':1,
                 'out':'con'})
    if r['return']>0: return r
    lsa=r.get('last_stat_analysis',{}).get('dict_flat',{})
    time_min=lsa.get('##characteristics#run#execution_time#min',None)
    if time_min==None or time_min==0.0:
       return {'return':1, 'error':'failed to run default pipeline'}

    # data is per N size
    while True: # continue infinite loop until stopping
       ck.out(line)

       n=random.randint(0,3) # Matrix size generator
       if n==0:
          N=random.randint(4,1024) # Matrix size
       else:
          NX=random.randint(2,10)
          N=2**NX
          if n==2: N=N-1
          if n==3: N=N+1

       SN=str(N)

       if SN not in data: data[SN]={}
       xdata=data.get(SN,{})

       tmin=xdata.get('tmin',None)
       tmax=xdata.get('tmax',None)
       gmin=xdata.get('gmin',None)
       gmax=xdata.get('gmax',None)
       best_tile=xdata.get('best_tile',None)

       for opts in range(0,16):
           # Choose if random BS or power of two or power of two -+1
           if opts==0:
              BS=1
           elif opts==1:
              BS=N
           else:
              b=random.randint(0,3)

              if b==0:
                 BS=random.randint(1,N)
              else:
                 B1=math.frexp(N)[1]-1
                 B2=random.randint(0,B1)
                 BS=2**B2

                 if b==2 and BS>1: BS=BS-1
                 elif b==3 and BS<N-1: BS=BS+1

           ck.out('Matrix size: '+str(N))
           ck.out('Tile size:   '+str(BS))

           # Run pipeline
           tpipeline=copy.deepcopy(pipeline)
           r=ck.access({'action':'autotune',
                        'module_uoa':'pipeline',
                        'pipeline':pipeline,
                        'pipeline_update':{
                         'no_compile':'yes',
                         'env':{'CT_MATRIX_DIMENSION':N,
                                'CT_BLOCK_SIZE':BS}
                        },
                        'iterations':1,
                        'repetitions':3,
                        'out':'con'})
           if r['return']>0: return r

           lsa=r.get('last_stat_analysis',{}).get('dict_flat',{})
           time_min=lsa.get('##characteristics#run#execution_time#min',None)

           changed=False
           if time_min!=None:
              ops=2*(N*N*N)
              if tmin==None or time_min<tmin: 
                 tmin=time_min
                 best_tile=BS
                 gmax=1.0e-9*ops/tmin
                 changed=True
              if tmax==None or time_min>tmax: 
                 tmax=time_min
                 gmin=1.0e-9*ops/tmax
                 changed=True

              if changed:
                 xdata['tmin']=tmin
                 xdata['tmax']=tmax
                 xdata['gmin']=gmin
                 xdata['gmax']=gmax
                 xdata['best_tile']=best_tile

              if opts==0:
                 xdata['tbs1']=time_min
                 xdata['gbs1']=1.0e-9*ops/time_min
                 changed=True
              elif opts==1:
                 xdata['tbsn']=time_min
                 xdata['gbsn']=1.0e-9*ops/time_min
                 xdata['bsn']=N
                 changed=True

           if changed:
              ck.out(line)
              ck.out('Saving aggregated stats ...')

              r=ck.save_json_to_file({'json_file':fas, 'dict':{'all':aa}, 'sort_keys':'yes'})
              if r['return']>0: return r

    #############################################################
    ck.out(line)
    ck.out('Saving aggregated stats ...')

    r=ck.save_json_to_file({'json_file':fas, 'dict':{'all':aa}, 'sort_keys':'yes'})
    if r['return']>0: return r

    return {'return':0}

r=main({})
if r['return']>0: ck.err(r)
