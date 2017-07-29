# Grigori Fursin prepared these low-level scripts for RPi3 autotuning and crowd-tuning

ck benchmark program:cbench-automotive-susan --cmd_key=corners --repeat=100 --dataset_uoa=image-pgm-0001 --flags="-Og -fcrossjumping -frename-registers -fschedule-insns -fno-associative-math -fno-auto-inc-dec -fno-branch-probabilities -fno-branch-target-load-optimize -fno-branch-target-load-optimize2 -fno-caller-saves -fno-combine-stack-adjustments -fno-conserve-stack -fno-compare-elim -fcprop-registers -fno-cse-follow-jumps -fno-cse-skip-blocks -fno-cx-fortran-rules -fdce -fno-delayed-branch -fno-delete-null-pointer-checks -fno-devirtualize -fno-devirtualize-at-ltrans -fno-dse -fno-early-inlining -fno-fat-lto-objects -fno-finite-math-only -fno-float-store -fno-function-sections -fno-gcse -fno-gcse-las -fno-gcse-lm -fno-graphite-identity -fno-gcse-sm -fno-hoist-adjacent-loads -fno-if-conversion -fno-if-conversion2 -fno-indirect-inlining -fno-inline-functions -fno-ipa-cp -fno-ipa-cp-clone -fno-ipa-cp-alignment -fno-ipa-pta -fno-ipa-pure-const -fno-ipa-reference -fno-ipa-icf -fno-ira-hoist-pressure -fno-ira-loop-pressure -fno-ira-share-save-slots -fno-ira-share-spill-slots -fno-isolate-erroneous-paths-dereference -fno-ivopts -fno-keep-inline-functions -fno-keep-static-consts -fno-live-range-shrinkage -fno-loop-block -fno-loop-strip-mine -fno-loop-unroll-and-jam -fno-loop-nest-optimize -fno-loop-parallelize-all -fno-lra-remat -fno-lto -fno-merge-all-constants -fno-merge-constants -fno-modulo-sched-allow-regmoves -fno-move-loop-invariants -fno-branch-count-reg -fno-defer-pop -fno-function-cse -fguess-branch-probability -finline -fmath-errno -fno-peephole -fno-peephole2 -fno-sched-interblock -fno-sched-spec -fno-signed-zeros -fno-toplevel-reorder -fno-trapping-math -fno-zero-initialized-in-bss -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-predictive-commoning -fno-prefetch-loop-arrays -fno-reciprocal-math -fno-ree -freorder-blocks -fno-reorder-blocks-and-partition -fno-reorder-functions -fno-rerun-cse-after-loop -fno-reschedule-modulo-scheduled-loops -fno-rounding-math -fno-sched2-use-superblocks -fsched-pressure -fno-sched-spec-load -fno-sched-spec-load-dangerous -fno-sched-group-heuristic -fno-sched-critical-path-heuristic -fno-sched-spec-insn-heuristic -fno-sched-rank-heuristic -fno-sched-last-insn-heuristic -fno-sched-dep-count-heuristic -fno-schedule-fusion -fno-schedule-insns2 -fno-section-anchors -fno-selective-scheduling -fno-selective-scheduling2 -fno-sel-sched-pipelining -fno-sel-sched-pipelining-outer-loops -fno-semantic-interposition -fno-shrink-wrap -fno-signaling-nans -fno-single-precision-constant -fno-split-ivs-in-unroller -fno-split-wide-types -fno-ssa-phiopt -fno-stdarg-opt -fno-strict-aliasing -fno-thread-jumps -fno-tracer -fno-tree-bit-ccp -fno-tree-builtin-call-dce -fno-tree-ccp -fno-tree-ch -ftree-coalesce-vars -fno-tree-copy-prop -fno-tree-copyrename -fno-tree-dce -fno-tree-dominator-opts -fno-tree-dse -ftree-forwprop -ftree-fre -fno-tree-loop-if-convert -fno-tree-loop-if-convert-stores -fno-tree-loop-im -fno-tree-phiprop -fno-tree-loop-distribution -fno-tree-loop-distribute-patterns -fno-tree-loop-ivcanon -fno-tree-loop-linear -fno-tree-loop-optimize -fno-tree-loop-vectorize -fno-tree-partial-pre -fno-tree-pta -fno-tree-reassoc -fno-tree-sink -fno-tree-sra -fno-tree-switch-conversion -fno-tree-tail-merge -fno-tree-vectorize -fno-tree-vrp -fno-unit-at-a-time -fno-unroll-all-loops -fno-unroll-loops -fno-unsafe-loop-optimizations -fno-unsafe-math-optimizations -fno-unswitch-loops -fno-ipa-ra -fno-variable-expansion-in-unroller -fno-vect-cost-model -fno-vpt -fno-web -fno-whole-program -fno-wpa -fno-use-linker-plugin -fexcess-precision=standard -ffp-contract=off -fira-algorithm=CB -fira-region=all -flto-partition=none"
