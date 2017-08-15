ck autotune program:7z --iterations=1 --repetitions=2 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 --seed=12345 \
   --new --skip_collaborative --only_filter @apply_frontier.json \
   --cmd_key=encode --dataset_uoa=txt-novel-0001 --repeat=1 \
   --record_uoa=rpi3-7z-encode-gcc7-cbest-frontier --quiet

ck autotune program:aubio --iterations=1 --repetitions=2 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 --seed=12345 \
   --new --skip_collaborative --only_filter @apply_frontier.json \
   --cmd_key=aubionotes --dataset_uoa=audio-mp3-0001 --repeat=100 \
   --record_uoa=rpi3-aubio-aubionotes-gcc7-cbest-frontier --quiet

ck autotune program:ccrypt --iterations=1 --repetitions=2 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 --seed=12345 \
   --new --skip_collaborative --only_filter @apply_frontier.json \
   --cmd_key=encrypt --dataset_uoa=txt-novel-0001 --repeat=10 \
   --record_uoa=rpi3-ccrypt-encrypt-gcc7-cbest-frontier --quiet

ck autotune program:gzip --iterations=1 --repetitions=2 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 --seed=12345 \
   --new --skip_collaborative --only_filter @apply_frontier.json \
   --cmd_key=decode --dataset_uoa=txt-novel-0001-gzipped --repeat=30 \
   --record_uoa=rpi3-gzip-decode-gcc7-cbest-frontier --quiet

ck autotune program:gzip --iterations=1 --repetitions=2 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 --seed=12345 \
   --new --skip_collaborative --only_filter @apply_frontier.json \
   --cmd_key=encode --dataset_uoa=txt-novel-0001 --repeat=10 \
   --record_uoa=rpi3-gzip-encode-gcc7-cbest-frontier --quiet

ck autotune program:minigzip --iterations=1 --repetitions=2 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 --seed=12345 \
   --new --skip_collaborative --only_filter @apply_frontier.json \
   --cmd_key=decode --dataset_uoa=txt-novel-0001-deflated --repeat=30 \
   --record_uoa=rpi3-minigzip-decode-gcc7-cbest-frontier --quiet

ck autotune program:minigzip --iterations=1 --repetitions=2 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 --seed=12345 \
   --new --skip_collaborative --only_filter @apply_frontier.json \
   --cmd_key=encode --dataset_uoa=txt-verse-novel-0001 --repeat=100 \
   --record_uoa=rpi3-minigzip-encode-gcc7-cbest-frontier --quiet

ck autotune program:rhash --iterations=1 --repetitions=2 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 --seed=12345 \
   --new --skip_collaborative --only_filter @apply_frontier.json \
   --cmd_key=sha3 --dataset_uoa=txt-verse-novel-0001 --repeat=100 \
   --record_uoa=rpi3-rhash-sha3-gcc7-cbest-frontier --quiet

ck autotune program:sha512sum --iterations=1 --repetitions=2 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 --seed=12345 \
   --new --skip_collaborative --only_filter @apply_frontier.json \
   --cmd_key=sha512 --dataset_uoa=txt-verse-novel-0001 --repeat=200 \
   --record_uoa=rpi3-sha512sum-sha512-gcc7-cbest-frontier --quiet

ck autotune program:unrar --iterations=1 --repetitions=2 --scenario=9d88674c45b94971 --compiler_env_uoa=4f11abfefd3cc031 --seed=12345 \
   --new --skip_collaborative --only_filter @apply_frontier.json \
   --cmd_key=unrar --dataset_uoa=txt-novel-0001-rared --repeat=10 \
   --record_uoa=rpi3-unrar-unrar-gcc7-cbest-frontier --quiet
