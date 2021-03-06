#!/bin/sh

# Driver script for RCU testing under Nidhugg.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, you can access it online at
# http://www.gnu.org/licenses/gpl-2.0.html.
#
# Author: Michalis Kokologiannakis <mixaskok@gmail.com>

unroll=5
preems=$2
method=$1

# runfailure <kernel_version> <memory_model> <source_file> CFLAGS
#
# Run Nidhugg on the specified <source_file>, under the memory model
# specified by <memory_model>, on Linux kernel version <kernel_version>,
# with the expectation that verification will fail.
# Additional arguments will be passed to the clang compiler (see test
# files for more information).
runfailure() {
    k_version=$1
    mem_model=$2
    test_file=$3
    shift 3
    
    echo '--------------------------------------------------------------------'
    echo '--- Preparing to run tests on kernel' ${k_version} under ${mem_model}
    echo '--- Expecting verification failure'
    echo '--------------------------------------------------------------------'
    if nidhuggc -I ${k_version} -std=gnu99 $* -- --${mem_model}  \
		--extfun-no-race=fprintf --extfun-no-race=memcpy --bound=${preems} --preemption-bounding=${method} \
		--print-progress-estimate --disable-mutex-init-requirement \
		--unroll=${unroll} ${test_file}
    then
	echo '^^^ Unexpected verification success'
	failure=1
    fi
}

# runsuccess <kernel_version> <memory_model> <source_file> CFLAGS
#
# Run Nidhugg on the specified <source_file>, under the memory model
# specified by <memory_model>, on Linux kernel version <kernel_version>,
# with the expectation that verification will succeed.
# Additional arguments will be passed to the clang compiler (see test
# files for more information).
runsuccess() {
    k_version=$1
    mem_model=$2
    test_file=$3
    shift 3
    
    echo '--------------------------------------------------------------------'
    echo '--- Preparing to run tests on kernel' ${k_version} under ${mem_model}
    echo '--- Expecting verification success'
    echo '--------------------------------------------------------------------'
    if nidhuggc -I ${k_version} -std=gnu99 $* -- --${mem_model}  \
		--extfun-no-race=fprintf --extfun-no-race=memcpy --preemption-bounding=${method} --bound=${preems}\
		--print-progress-estimate --disable-mutex-init-requirement \
		--unroll=${unroll} ${test_file}
    then
	:
    else
	echo '^^^ Unexpected verification failure'
	failure=1
    fi
}

# Synchronization issues for rcu_process_gp_end()
# runfailure v2.6.31.1 sc gp_end_bug.c
# runfailure v2.6.32.1 sc gp_end_bug.c
# runsuccess v3.0 sc gp_end_bug.c -DKERNEL_VERSION_3
# exit
# Alleged bug between grace-period forcing and initialization
#runsuccess v2.6.31.1 tso init_bug.c -DCONFIG_NR_CPUS=3 \
#	   -DCONFIG_RCU_FANOUT=2 -DFQS_NO_BUG


# Grace-Period guarantee -- RCU tree litmus test
# Linux kernel v3.0
# Linux kernels v3.19, v4.3, v4.7, and v4.9.6
for version in v3.19 v4.3 v4.7 v4.9.6
do
    for mm in sc
    do
	runfailure ${version} ${mm} litmus.c -DFORCE_FAILURE_3
    done
done


if test -n "$failure"
then
    echo '--------------------------------------------------------------------'
    echo '--- ' UNEXPECTED VERIFICATION RESULTS
    echo '--------------------------------------------------------------------'
    exit 1
else
    echo '--------------------------------------------------------------------'
    echo '--- ' Verification proceeded as expected
    echo '--------------------------------------------------------------------'
    exit 0
fi
