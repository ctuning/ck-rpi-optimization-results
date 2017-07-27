# Grigori Fursin prepared these low-level scripts for RPi3 autotuning and crowd-tuning

# --compiler_env_uoa=
#  7e149c8504752933 - gcc 4.9.2
#  4f11abfefd3cc031 - gcc 7.1.0
#  8e66a1d34e9e93ea - clang 3.8.1

# You need to substitute above UIDs with your environment (ck show env --tags=compiler)

ck autotune program:cbench-automotive-susan --repetitions=2 --scenario=experiment.tune.compiler.flags --extra_tags=main-flags --compiler_env_uoa=7e149c8504752933 \
   --new --skip_collaborative --skip_pruning \
   --cmd_key=corners --quiet --repeat=100 --dataset_uoa=image-pgm-0001 --record_uoa=rpi3-susan-corners-gcc4-main-empty-opt @run-without-opt.json

ck autotune program:cbench-automotive-susan --repetitions=2 --scenario=experiment.tune.compiler.flags --extra_tags=main-flags --compiler_env_uoa=4f11abfefd3cc031 \
   --new --skip_collaborative --skip_pruning \
   --cmd_key=corners --quiet --repeat=100 --dataset_uoa=image-pgm-0001 --record_uoa=rpi3-susan-corners-gcc7-main-empty-opt @run-without-opt.json

ck autotune program:cbench-automotive-susan --repetitions=2 --scenario=experiment.tune.compiler.flags --extra_tags=main-flags --compiler_env_uoa=8e66a1d34e9e93ea \
   --new --skip_collaborative --skip_pruning \
   --cmd_key=corners --quiet --repeat=100 --dataset_uoa=image-pgm-0001 --record_uoa=rpi3-susan-corners-clang381-main-empty-opt @run-without-opt.json
