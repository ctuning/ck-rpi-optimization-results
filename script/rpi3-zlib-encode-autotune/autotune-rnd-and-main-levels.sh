# Grigori Fursin prepared these low-level scripts for RPi3 autotuning and crowd-tuning

# --compiler_env_uoa=
#  7e149c8504752933 - gcc 4.9.2
#  4f11abfefd3cc031 - gcc 7.1.0
#  8e66a1d34e9e93ea - clang 3.8.1

# You need to substitute above UIDs with your environment (ck show env --tags=compiler)

ck autotune program:zlib --iterations=150 --repetitions=3 --scenario=9d88674c45b94971 --compiler_env_uoa=7e149c8504752933 \
   --base_flags --new --skip_collaborative --skip_pruning \
   --cmd_key=encode --quiet --repeat=10 --dataset_uoa=video-raw-0001 --record_uoa=rpi3-zlib-encode-gcc4-150b-rnd

ck autotune program:zlib --iterations=150 --repetitions=3 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 \
   --base_flags --new --skip_collaborative --skip_pruning \
   --cmd_key=encode --quiet --repeat=10 --dataset_uoa=video-raw-0001 --record_uoa=rpi3-zlib-encode-gcc7-150b-rnd
