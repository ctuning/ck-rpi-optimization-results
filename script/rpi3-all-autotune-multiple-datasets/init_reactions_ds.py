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

r=ck.access({'action':'search',
             'repo_uoa':'ck-rpi-optimization-results-reactions-multiple-datasets', 
             'module_uoa':'experiment',
             'data_uoa':'rpi3-*',
             'add_meta':'yes'})
if r['return']>0: ck.err(r)
lst=r['lst']

im=len(lst)
iq=0

ck.out('Found '+str(im)+' experiments ...')

# Get unique values for all keys AND PROGRAM/DATASETS
xdatasets={}
datasets={}

umeta={}
for q in lst:
    meta=q['meta']['meta']
    for k in meta:
        v=meta[k]

        x=umeta.get(k,[])
        if v not in x:
           x.append(v)
        umeta[k]=x

    cmd_key=meta['cmd_key']

    ds_uoa=meta['dataset_uoa']

    # Get alias
    r=ck.access({'action':'load',
                 'module_uoa':'dataset',
                 'data_uoa':ds_uoa})
    if r['return']>0: ck.err(r)
    z_ds_uoa=r['data_uoa']
    z_ds_uid=r['data_uid']

    p_uoa=meta['program_uoa']

    ind=p_uoa+' ; '+cmd_key

    if ind not in xdatasets:
       xdatasets[ind]=[]

    xdatasets[ind].append(z_ds_uoa)

# Numerate datasets
for ind in xdatasets:
    if ind not in datasets:
       datasets[ind]={}

    iq=1
    for ds in sorted(xdatasets[ind]):
        datasets[ind][ds]=iq
        iq+=1

# Get optimizations per compiler
compilers=umeta['compiler']

uopts={}
iuopts={}
classes={}
improvements={}
bench_index={}
individual_flags={}

ck.out('')
ck.out('Trying to pre-load optimization numbers from previous analysis ...')

for q in compilers:
    s='rpi3-snapshot-'+q.lower().replace(' ','-')+'-autotuning'

    # Find entry
    r=ck.access({'action':'load',
                 'module_uoa':'slide',
                 'data_uoa':s})
    if r['return']>0: ck.err(r)
    p=r['path']
    d=r['dict']

    d1=d['slides'][0]

    p1=os.path.join(p,d1+'.json')
    
    r=ck.load_json_file({'json_file':p1})
    if r['return']>0: ck.err(r)

    d2=r['dict']

    classes[q]={'-O3':[]}
    uopts[q]={'-O3':0}
    improvements[q]={}
    individual_flags[q]={}

    for t in d2['table']:
        num=t['solution_num']
        flags=t['best_flags'].strip()

        classes[q][flags]=[]
        uopts[q][flags]=num

#for q in compilers:
#    classes[q]={'-O3':[]}
#
#    uopts[q]={'-O3':0}
#    iuopts[q]=1

for comp in compilers:
    heatmaps={}

    iq=0
    for q in sorted(lst, key=lambda x: x['data_uoa']):
        meta=q['meta']['meta']

        compiler=meta['compiler']
        if compiler==comp:
           iq+=1

           duoa=q['data_uoa']
           p=q['path']

           cmd_key=meta['cmd_key']

           ds_uoa=meta['dataset_uoa']
           # Get alias
           r=ck.access({'action':'load',
                        'module_uoa':'dataset',
                        'data_uoa':ds_uoa})
           if r['return']>0: ck.err(r)
           z_ds_uoa=r['data_uoa']
           z_ds_uid=r['data_uid']

           p_uoa=meta['program_uoa']

           ck.out('')
           ind=p_uoa+' ; '+cmd_key
           ck.out('* '+compiler+' ; '+ind+' ; '+z_ds_uoa)

           if ind not in heatmaps:
              heatmaps[ind]=[]

           bench_index[str(iq)]=ind

           # Process reactions (and calcluate speedup based on min values to see what hardware can achieve, later can use expected values)
           ld=os.listdir(p)

           reactions={}
           default_time=None

           for df in ld:
               if df.endswith('.flat.json'):
                  # Load file
                  pdf=os.path.join(p,df)

                  r=ck.load_json_file({'json_file':pdf})
                  if r['return']>0: ck.err(r)

                  d=r['dict']

                  opt=d['##characteristics#compile#joined_compiler_flags#min'].strip()

                  if opt not in uopts[compiler]:
                     continue
#                     uopts[compiler][opt]=iuopts[compiler]
#                     iuopts[compiler]+=1

                  t=d.get('##characteristics#run#execution_time_kernel_0#min',None)

                  if t!=None:
                     if opt=='-O3':
                        default_time=t
                     else:
                        reactions[opt]=t

           # Calculate improvements/degradation
           if default_time!=None and default_time!=0.0:
              for k in reactions:
                  t=reactions[k]
                  if t==0.0:
                     reactions[k]=0.0
                  else:
                     s=default_time/t
                     if t<0.5:
                        s=0
                     reactions[k]=s

              # Sort by improvements
              opts=sorted(reactions, key=lambda v: reactions[v], reverse=True)

              ck.out('')
              for k in opts:
                  ck.out(('  %.2f' % reactions[k])+' : '+k)

              # Get highest improvement
              ohi=opts[0]
              hi=reactions[ohi]

              if hi>=improvement_threshold:
                 if ohi in classes[compiler]:
                    x=classes[compiler].get(ohi,[])
                    if ind not in x:
                       x.append({"name":ind,"improvement":hi})
                    classes[compiler][ohi]=x
                    improvements[compiler][ind]=hi
              else:
                 classes[compiler]['-O3'].append({"name":ind,"improvement":1.0})

              iq_ds=datasets[ind][z_ds_uoa]

              # Prepare heat map (unsorted)
              for opt in uopts[compiler]:
                  if opt!='-O3':
                     iopt=uopts[compiler][opt]
                     x=[iq_ds, iopt, reactions.get(opt,0.0)]

                     heatmaps[ind].append(x)

    # Prepare plotting
    ii={
          "action":"plot",
          "module_uoa":"graph",

          "plot_type":"mpl_2d_heatmap",
          "display_x_error_bar":"no",
          "display_y_error_bar":"no",

          "title":"Powered by Collective Knowledge",

          "axis_x_desc":"Datasets",
          "axis_y_desc":"Unique optimizations (choices)",
          "axis_z_desc":"Improvement",

          "plot_grid":"no",

          "mpl_image_size_x":"12",
          "mpl_image_size_y":"8",
          "mpl_image_dpi":"100",

          "colorbar_pad":0.08,

          "shifted_colormap":"no",
          "shifted_colormap_mid":1,

          "point_style":{"0":{"elinewidth":"40", "marker":"|", "size":800, "colorbar_orietation":"horizontal", "colorbar_label":"Reaction to optimization (speedup when > 1.0)"}}
        }


    # Record heat maps per program/cmd with multiple data sets
    for hm in heatmaps:
        hm1=hm.replace(' ; ','_').replace('  ','').replace(' ','_')

        results={}

        heatmap=heatmaps[hm] 

        dd={'table':{"0":heatmap}}

        xx=[]
        iq=0
        for k in uopts[comp]:
            xx.append(iq)
            iq+=1

        dd['axis_y_labels']=xx

        name='init_reactions_tmp_heatmap_'+comp.replace(' ','_')+'_'+hm1

        r=ck.save_json_to_file({'json_file':name+'.json','dict':dd,'sort_keys':'yes'})
        if r['return']>0: ck.err(r)

        # Plot
        ii.update(dd)

        ii['out_to_file']=name+'.pdf'

        # Check number of labels
        x=[]
        for iq in range(0,len(datasets[hm])+1):
            x.append(iq)

        ii['axis_x_labels']=x

        r=ck.access(ii)
        if r['return']>0: ck.err(r)

        for q in heatmap:
            ds=q[0]
            opt=q[1]
            val=q[2]

            # Find name of ds
            xds=''
            for k in datasets[hm]:
                if datasets[hm][k]==ds:
                   xds=k
                   break

            if opt not in results:
               results[opt]={}

            results[opt][xds]='%.3f'%val

        # Record
        r=ck.save_json_to_file({'json_file':name+'.results.json','dict':results,'sort_keys':'yes'})
        if r['return']>0: ck.err(r)

        # Sort classes
        for o in classes[comp]:
            b=classes[comp][o]

            b1=sorted(b, key=lambda k: k.get('improvement',0.0), reverse=True)

            classes[comp][o]=b1

        # Prepare individual flags to predict (YES/NO)
        for opt in classes[comp]:
            benchs=classes[comp][opt]

            sopt=opt.split(' ')
            for o in sopt:
                ot=o.strip()
                 
                x=individual_flags[comp].get(ot,[])

                for b in benchs:
                    if b not in x:
                       x.append(b)

                individual_flags[comp][ot]=x


# Save info
info={'opts':uopts, 'classes':classes, 'improvements':improvements, 'bench_index':bench_index, 'individual_flags':individual_flags}

r=ck.save_json_to_file({'json_file':'init_reactions_tmp_info.json','dict':info,'sort_keys':'yes'})
if r['return']>0: ck.err(r)
