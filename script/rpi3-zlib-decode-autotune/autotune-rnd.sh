# Grigori Fursin prepared these low-level scripts for RPi3 autotuning and crowd-tuning

# --compiler_env_uoa=
#  7e149c8504752933 - gcc 4.9.2
#  4f11abfefd3cc031 - gcc 7.1.0
#  8e66a1d34e9e93ea - clang 3.8.1

# You need to substitute above UIDs with your environment (ck show env --tags=compiler)

ck autotune program:zlib --iterations=150 --repetitions=3 --scenario=9d88674c45b94971 --compiler_env_uoa=7e149c8504752933 \
   --cmd_key=decode --quiet --repeat=100 --dataset_uoa=video-raw-0001-deflated --record_uoa=rpi3-zlib-decode-gcc4-150-rnd

ck autotune program:zlib --iterations=150 --repetitions=3 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 \
   --cmd_key=decode --quiet --repeat=100 --dataset_uoa=video-raw-0001-deflated --record_uoa=rpi3-zlib-decode-gcc7-150-rnd
