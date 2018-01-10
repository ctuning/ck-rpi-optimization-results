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

improvement_threshold=1.05

gcc=['GCC 4.9.2', 'GCC 7.1.0']

# Load info file
r=ck.load_json_file({'json_file':'init_reactions_tmp_info.json'})
if r['return']>0: ck.err(r)
info=r['dict']

bench_index=info['bench_index']

for g in gcc:
    # Load heatmap
    fn='init_reactions_tmp_heatmap_'+g.replace(' ','_')
    r=ck.load_json_file({'json_file':fn+'.json'})
    if r['return']>0: ck.err(r)

    dd=r['dict']

    heatmap=dd['table']['0']
    max_opts=len(dd['axis_y_labels'])-1

    # Cluster by reactions (improvements)
    sorted_heatmap=[]
    sorted_heatmap2=[[1,0,0]]

    remapping={}

    ibench=1

    classes=info['classes'][g]
    opts=info['opts'][g]

    ck.out('')
    for iopt in range(0,max_opts+1):
        opt=''

        # Find opt
        for o in opts:
            if opts[o]==iopt:
               opt=o
               break

        if opt=='':
           ck.err({'return':1, 'error':'can\'t find opt'})

        ck.out('Processing opt: '+str(iopt)+' ('+opt+')')

        benchs=classes[opt]

        sorted_heatmap.append([ibench+1,0,1.0])

        for b in benchs:
            bn=b['name']
            reaction=b['improvement']

            original_index=-1

            for bx in bench_index:
                bv=bench_index[bx]
                if bv==bn:
                   original_index=bx
                   break

            if original_index==-1: 
               ck.err({'return':1, 'error':'can\'t find bench index'})

            if original_index in remapping:
               ck.err({'return':1, 'error':'inconsistency in remapping'})

            remapping[original_index]=ibench

            sorted_heatmap2.append([ibench,iopt,reaction])

            ibench+=1

    # Move all without improvements to the end
    for bx in bench_index:
        sbx=str(bx)
        if sbx not in remapping:
           remapping[sbx]=ibench
           ibench+=1

    # remap
    for h in heatmap:
        bench=h[0]
        iopt=h[1]
        reaction=h[2]

        x=[remapping[str(bench)],iopt,reaction]

        sorted_heatmap.append(x)

    # save
    dd['table']['0']=sorted_heatmap
    r=ck.save_json_to_file({'json_file':fn+'_clustered.json','dict':dd,'sort_keys':'yes'})
    if r['return']>0: ck.err(r)

    # save
    dd['table']['0']=sorted_heatmap2
    r=ck.save_json_to_file({'json_file':fn+'_clustered2.json','dict':dd,'sort_keys':'yes'})
    if r['return']>0: ck.err(r)
