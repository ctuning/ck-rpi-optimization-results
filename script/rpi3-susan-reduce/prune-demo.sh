# Grigori Fursin prepared these low-level scripts for RPi3 autotuning and crowd-tuning

ck benchmark program:cbench-automotive-susan --cmd_key=corners --repeat=100 --dataset_uoa=image-pgm-0001 --prune --prune_md5 --flags="-O3 -fno-guess-branch-probability -fno-if-conversion -fno-ivopts -fno-schedule-insns -fsingle-precision-constant --param max-unswitch-insns=5" @prune-demo.json