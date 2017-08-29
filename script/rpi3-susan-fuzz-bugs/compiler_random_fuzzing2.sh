# Grigori Fursin prepared these low-level scripts for RPi3 crowd-fuzzing (searching for bugs via different compiler flag selection)

# --compiler_env_uoa=
#  7e149c8504752933 - gcc 4.9.2
#  4f11abfefd3cc031 - gcc 7.1.0
#  8e66a1d34e9e93ea - clang 3.8.1

# You need to substitute above UIDs with your environment (ck show env --tags=compiler)

ck autotune program:cbench-automotive-susan --iterations=150 --repetitions=1 --scenario=f7045b998e4732e9 --compiler_env_uoa=7e149c8504752933 \
   --seed=12345 \
   --base_flags --new --skip_collaborative --skip_pruning \
   --cmd_key=corners --quiet --repeat=100 --dataset_uoa=image-pgm-0001 --record_uoa=rpi3-susan-corners-gcc4-150bpc-rnd-fuzzing2

ck autotune program:cbench-automotive-susan --iterations=150 --repetitions=1 --scenario=f7045b998e4732e9 --compiler_env_uoa=4f11abfefd3cc031 \
   --seed=12345 \
   --base_flags --new --skip_collaborative --skip_pruning \
   --cmd_key=corners --quiet --repeat=100 --dataset_uoa=image-pgm-0001 --record_uoa=rpi3-susan-corners-gcc7-150bpc-rnd-fuzzing2
