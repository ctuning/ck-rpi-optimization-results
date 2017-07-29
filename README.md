[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-powered-by-ck.png)](http://cKnowledge.org)
[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-validated-by-the-community-simple.png)](http://cTuning.org)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Introduction
============

Optimization results during compiler autotuning and crowd-tuning on RPi3 in a reusable and reproducible Collective Knowledge format (CK)

License
=======
* BSD, 3-clause 

Prerequisites
=============
* Collective Knowledge framework ([@GitHub](http://github.com/ctuning/ck))
* Python 2.7 or 3.3+
* Python PIP
* Git client

Installation
============
Install CK:

```
 $ sudo pip install ck
```

Install this CK repository:

```
 $ ck pull repo --url=https://github.com/dividiti/ck-rpi-optimization
```

Update all CK repositories at any time
```
 $ ck pull all
```

Notes
=====
I could not build GCC 7.1.0 for RPi3 via CK with Graphite support (outdated libraries and missing deps).

This may reduce optimization possibilities during autotuning:


```
gcc -c    -I../ -DCK_HOST_OS_NAME2_LINUX=1 -DCK_HOST_OS_NAME_LINUX=1 -DCK_TARGET_OS_NAME2_LINUX=1 -DCK_TARGET_OS_NAME_LINUX=1 -DXOPENME -I/home/fursin/CK-TOOLS/lib-rtl-xopenme-0.3-gcc-4.9.2-linux-32/include -O3 -fcaller-saves -fcse-follow-jumps -fgcse-lm -fno-gcse-sm -fira-share-save-slots -fno-ira-share-spill-slots -floop-interchange -flto -fmodulo-sched-allow-regmoves -fpeephole -fsched-spec -freciprocal-math -fno-sched-spec-load-dangerous -fselective-scheduling2 -fsel-sched-pipelining-outer-loops -fsignaling-nans -fsplit-ivs-in-unroller -ftree-dominator-opts -fno-tree-fre -ftree-loop-distribute-patterns -ftree-ter ../adler32.c  -o adler32.o
../adler32.c:1:0: 

sorry, unimplemented: Graphite loop optimizations cannot be used
(isl is not available) (-fgraphite, -fgraphite-identity,
-floop-nest-optimize, -floop-parallelize-all)

```
