# Grigori Fursin prepared these low-level scripts for RPi3 autotuning and crowd-tuning

# --compiler_env_uoa=
#  7e149c8504752933 - gcc 4.9.2
#  4f11abfefd3cc031 - gcc 7.1.0
#  8e66a1d34e9e93ea - clang 3.8.1

# You need to substitute above UIDs with your environment (ck show env --tags=compiler)

ck run program:7z --cmd_key=encode --dataset_uoa=txt-novel-0001 --repeat=1
ck run program:aubio --cmd_key=aubionotes --dataset_uoa=audio-mp3-0001 --repeat=100
ck run program:ccrypt --cmd_key=encrypt --dataset_uoa=txt-novel-0001 --repeat=10
ck run program:gzip --cmd_key=decode --dataset_uoa=txt-novel-0001-gzipped --repeat=30
ck run program:gzip --cmd_key=encode --dataset_uoa=txt-novel-0001 --repeat=10
ck run program:minigzip --cmd_key=decode --dataset_uoa=txt-novel-0001-deflated --repeat=30
ck run program:minigzip --cmd_key=encode --dataset_uoa=txt-verse-novel-0001 --repeat=100
ck run program:rhash --cmd_key=sha3 --dataset_uoa=txt-verse-novel-0001 --repeat=100
ck run program:sha512sum --cmd_key=sha512 --dataset_uoa=txt-verse-novel-0001 --repeat=200
ck run program:unrar --cmd_key=unrar --dataset_uoa=txt-novel-0001-rared --repeat=10
