# Grigori Fursin prepared these low-level scripts for RPi3 autotuning and crowd-tuning

# --compiler_env_uoa=
#  7e149c8504752933 - gcc 4.9.2
#  4f11abfefd3cc031 - gcc 7.1.0
#  8e66a1d34e9e93ea - clang 3.8.1

# You need to substitute above UIDs with your environment (ck show env --tags=compiler)

# Scenario 3) auto/crowd-tune GCC compiler flags (minimize execution time and code size) (759e460c08f9bdc7)

ck autotune program:zlib --iterations=300 --repetitions=2 --scenario=759e460c08f9bdc7 --compiler_env_uoa=7e149c8504752933 --seed=12345 \
   --cmd_key=encode --quiet --repeat=10 --dataset_uoa=video-raw-0001 --record_uoa=rpi3-zlib-encode-gcc4-300-rnd-pareto @autotune-rnd-and-leave-only-frontier.json

ck autotune program:zlib --iterations=300 --repetitions=2 --scenario=759e460c08f9bdc7 --compiler_env_uoa=4f11abfefd3cc031 --seed=12345 \
   --cmd_key=encode --quiet --repeat=10 --dataset_uoa=video-raw-0001 --record_uoa=rpi3-zlib-encode-gcc7-300-rnd-pareto @autotune-rnd-and-leave-only-frontier.json
