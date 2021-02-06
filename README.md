[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)
[![automation](https://github.com/ctuning/ck-guide-images/blob/master/ck-artifact-automated-and-reusable.svg)](http://cTuning.org/ae)
[![workflow](https://github.com/ctuning/ck-guide-images/blob/master/ck-workflow.svg)](http://cKnowledge.org)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2455637.svg)](https://doi.org/10.5281/zenodo.2455637)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by/4.0/)

**All CK components can be found at [cKnowledge.io](https://cKnowledge.io) and in [one GitHub repository](https://github.com/ctuning/ai)!**

*This project is hosted by the [cTuning foundation](https://cTuning.org).*

Introduction
============

Optimization results to demonstrate compiler autotuning, crowd-tuning and machine learning on RPi3 
via customizable Collective Knowledge workflow framework with a portable package manager.

* arXiv report: http://arxiv.org/abs/1801.08024
* interactive CK report: http://cknowledge.org/rpi-crowd-tuning

License
=======
* CC BY 4.0 

Prerequisites
=============
* Collective Knowledge framework ([@GitHub](http://github.com/ctuning/ck))
* Python 2.7 or 3.3+
* Python PIP
* Git client

Minimal CK installation
=======================

The minimal installation requires:

* Python 2.7 or 3.3+ (limitation is mainly due to unitests)
* Git command line client.

You can install CK in your local user space as follows:

```
$ git clone http://github.com/ctuning/ck
$ export PATH=$PWD/ck/bin:$PATH
$ export PYTHONPATH=$PWD/ck:$PYTHONPATH
```

You can also install CK via PIP with sudo to avoid setting up environment variables yourself:

```
$ sudo pip install ck
```

CK repository installation
==========================

Install the CK repository:

```
 $ ck pull repo --url=https://github.com/dividiti/ck-rpi-optimization
```

Update all CK repositories at any time
```
 $ ck pull all
```

Check out report and see related scripts in the following entries:
```
 $ ck ls script:rpi3-*

```

For example, you can see individual scripts we used to prepare, run and reproduce autotuning experiments 
via CK for susan corners benchmark in the following entry:
```
 $ cd `ck find:scriptrpi3-susan-autotune`
 $ ls
```

Two CK repositories with additional experimental results in a reproducible form are available at FigShare:
* https://doi.org/10.6084/m9.figshare.5789007.v1

You can download and install them directly via CK as follows (note that each zip is around 150Mb archived
and ~1-1.5GB unzipped):
```
 $ ck add repo:ck-rpi-optimization-results-reactions --zip=https://ndownloader.figshare.com/files/10218435 --quiet
 $ ck add repo:ck-rpi-optimization-results-reactions-multiple-datasets --zip=https://ndownloader.figshare.com/files/10218441 --quiet
 $ ck ls experiment:rpi3-*
```

We continue gradually documenting all scripts in above entry together with the community - 
your help is appreciated. Feel free to get in touch with the community via CK mailing list:
* https://groups.google.com/forum/#!forum/collective-knowledge

Next steps:
* We plan to use reproducible optimization methodology prototyped here to support Pareto-efficient co-design
  competitions of the whole software and hardware stack for emerging workloads such as deep learning
  in terms of speed, accuracy, energy and costs: http://cKnowledge.org/request

Notes
=====
We could not build GCC 7.1.0 for RPi3 via CK with Graphite support (outdated libraries and missing deps). This may reduce optimization possibilities during autotuning:

```
gcc -c    -I../ -DCK_HOST_OS_NAME2_LINUX=1 -DCK_HOST_OS_NAME_LINUX=1 -DCK_TARGET_OS_NAME2_LINUX=1 -DCK_TARGET_OS_NAME_LINUX=1 -DXOPENME -I/home/fursin/CK-TOOLS/lib-rtl-xopenme-0.3-gcc-4.9.2-linux-32/include -O3 -fcaller-saves -fcse-follow-jumps -fgcse-lm -fno-gcse-sm -fira-share-save-slots -fno-ira-share-spill-slots -floop-interchange -flto -fmodulo-sched-allow-regmoves -fpeephole -fsched-spec -freciprocal-math -fno-sched-spec-load-dangerous -fselective-scheduling2 -fsel-sched-pipelining-outer-loops -fsignaling-nans -fsplit-ivs-in-unroller -ftree-dominator-opts -fno-tree-fre -ftree-loop-distribute-patterns -ftree-ter ../adler32.c  -o adler32.o
../adler32.c:1:0: 

sorry, unimplemented: Graphite loop optimizations cannot be used
(isl is not available) (-fgraphite, -fgraphite-identity,
-floop-nest-optimize, -floop-parallelize-all)

```
