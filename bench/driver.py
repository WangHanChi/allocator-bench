#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import numpy as np
import matplotlib.pyplot as plt
import sys
import time

threads = 12

###########################################################################

 ####       ##     ######     ##      ####    ######   ######
 ## ##     ####      ##      ####    ##  ##   ##         ##
 ##  ##   ##  ##     ##     ##  ##   ##       ##         ##
 ##  ##   ######     ##     ######    ####    ####       ##
 ##  ##   ##  ##     ##     ##  ##       ##   ##         ##
 ## ##    ##  ##     ##     ##  ##   ##  ##   ##         ##
 ####     ##  ##     ##     ##  ##    ####    ######     ##


CFRAC = 'cfrac ' + str(17545186520507317056371138836327483792789528)
ESPRESSO = 'espresso ' + 'largest.espresso '
LARSON = 'larson-sized ' + ' 5 8 1000 5000 100 4141 ' + str(threads)
MSTRESS = 'mstress ' + str(threads) + ' 50 25'
RPTESTN = 'rptest ' + str(threads) + ' 0 1 2 500 1000 100 8 16000'
ALLOCTEST1 = 'alloc-test ' + ' 1'
ALLOCTESTN = 'alloc-test ' + str(threads)
SH6BENCHN = 'sh6bench ' + str(2 * threads)
SH8BENCHN = 'sh8bench ' + str(2 * threads)
XMALLOCTESTN = 'xmalloc-test ' + ' -w ' + str(threads) + ' -t 5 -s 64'
CACHESCRATCH1 = 'cache-scratch ' + '1 1000 1 2000000 12'
CACHESCRATCHN = 'cache-scratch ' + str(threads) + ' 1000 1 2000000 12'
GLIBCSIMPLE = 'glibc-simple '
GLIBCTHREAD = 'glibc-thread ' + str(threads)
MALLOOCLARGE = 'malloc-large '
MLEAK = 'mleak ' + '5'
MLEAK10 = 'mleak ' + '50'
CACHETHRASH1 = 'cache-thrash ' + '1 1000 1 2000000 12'
CACHETHRASHN = 'cache-thrash ' + str(threads) + ' 1000 1 2000000 12'

test = [CFRAC, ESPRESSO, LARSON, MSTRESS, RPTESTN, ALLOCTEST1, ALLOCTESTN, \
        SH6BENCHN, SH8BENCHN, XMALLOCTESTN, CACHESCRATCH1, CACHESCRATCHN, GLIBCSIMPLE, \
        GLIBCTHREAD, MALLOOCLARGE, MLEAK, MLEAK10, CACHETHRASH1, CACHETHRASHN]

testname = ['cfrac', 'espresso', 'larsonN-sized', 'mstress', 'rptest',\
            'alloc-test1', 'alloc-testN', 'sh6bench', 'sh8bench', 'xmalloc-testN', \
            'cache-scratch1', 'cache-scratchN', 'glibc-simple', 'glibc-thread',\
            'malloc-large', 'mleak', 'mleak10', 'cache-thrash1', 'cache-thrashN']

###########################################################################


REF_LD_command = "LD_PRELOAD=/home/hank/linux2023/rpmalloc/\
bin/linux/release/x86-64/librpmallocwrap.so "

LD_command = "LD_PRELOAD=/home/hank/linux2023/myrpmalloc/rpmalloc\
/bin/linux/release/x86-64/librpmallocwrap.so "


PERF_command = "perf stat -r 1 "
FLAG_command = " -e page-faults,minor-faults,major-faults,instructions,context-switches,cycles ./"

if __name__ == "__main__":

###########################################################################

 ######   ######    ####    ######    ####    ##  ##    ####
   ##     ##       ##  ##     ##       ##     ### ##   ##  ##
   ##     ##       ##         ##       ##     ######   ##
   ##     ####      ####      ##       ##     ######   ## ###
   ##     ##           ##     ##       ##     ## ###   ##  ##
   ##     ##       ##  ##     ##       ##     ##  ##   ##  ##
   ##     ######    ####      ##      ####    ##  ##    ####
   
###########################################################################


    path = 'result_ref.txt'
    ref = open(path, 'w')

    path = 'result.txt'
    f = open(path, 'w')
    output = str("testing") + '\t' + str("faults") + '\t' + str("minor-faults") + '\t' + str("major-faults") + '\t' + str("instructions") + '\t' + str("cycles") + '\t'+ str("time") + '\n'
    ref.writelines(output)
    f.writelines(output)

    start = time.perf_counter()
    for i in range(0, len(test)):
        command = REF_LD_command + PERF_command + FLAG_command + str(test[i])
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout, stderr = process.communicate()
            error = stderr.decode("utf-8")
            # print(error)
            lines = error.split('\n')
            
            # faults
            allfaults = lines[3].strip()
            allfaults = allfaults.split(' ')
            allfaults[0] = float(allfaults[0].replace(',', ''))

            # minor-faults
            minfaults = lines[4].strip()
            minfaults = minfaults.split(' ')
            minfaults[0] = float(minfaults[0].replace(',', ''))

            # major-faults
            majfaults = lines[5].strip()
            majfaults = majfaults.split(' ')
            majfaults[0] = float(majfaults[0].replace(',', ''))
            
            # instructions
            inst = lines[6].strip()
            inst = inst.split(' ')
            inst[0] = float(inst[0].replace(',', ''))
            
            # cycles
            cycle = lines[8].strip()
            cycle = cycle.split(' ')
            cycle[0] = float(cycle[0].replace(',', ''))


            # times
            speed_time = lines[10].strip()
            speed_time = speed_time.split(' ')
            speed_time[0] = float(speed_time[0].replace(',', ''))

            output = str(testname[i]) + '\t' + str(allfaults[0]) + '\t' + str(minfaults[0]) + '\t' + str(majfaults[0]) + '\t' + str(inst[0]) + '\t' + str(cycle[0]) + '\t'+ str(speed_time[0]) + '\n'
            # print(output)
            ref.writelines(output)
        except:
            print('Oh! no')
            output = str(testname[i]) + '\t' + str(-1) + '\t' + str(-1) + '\t' + str(-1) + '\t' + str(-1) + '\t' + str(-1) + '\t'+ str(-1) + '\n'
            # print(output)
            ref.writelines(output)
    end = time.perf_counter()
    print("rpmalloc : %f" % (end - start))
    ref.close()
    
    start = time.perf_counter()
    for i in range(0, len(test)):
        command = LD_command + PERF_command + FLAG_command + str(test[i])
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout, stderr = process.communicate()
            error = stderr.decode("utf-8")
            # print(error)
            lines = error.split('\n')
            
            # faults
            allfaults = lines[3].strip()
            allfaults = allfaults.split(' ')
            allfaults[0] = float(allfaults[0].replace(',', ''))

            # minor-faults
            minfaults = lines[4].strip()
            minfaults = minfaults.split(' ')
            minfaults[0] = float(minfaults[0].replace(',', ''))

            # major-faults
            majfaults = lines[5].strip()
            majfaults = majfaults.split(' ')
            majfaults[0] = float(majfaults[0].replace(',', ''))
            
            # instructions
            inst = lines[6].strip()
            inst = inst.split(' ')
            inst[0] = float(inst[0].replace(',', ''))
            
            # cycles
            cycle = lines[8].strip()
            cycle = cycle.split(' ')
            cycle[0] = float(cycle[0].replace(',', ''))


            # times
            speed_time = lines[10].strip()
            speed_time = speed_time.split(' ')
            speed_time[0] = float(speed_time[0].replace(',', ''))

            output = str(testname[i]) + '\t' + str(allfaults[0]) + '\t' + str(minfaults[0]) + '\t' + str(majfaults[0]) + '\t' + str(inst[0]) + '\t' + str(cycle[0]) + '\t'+ str(speed_time[0]) + '\n'
            # print(output)
            f.writelines(output)
        except:
            print('Oh! no')
            output = str(testname[i]) + '\t' + str(-1) + '\t' + str(-1) + '\t' + str(-1) + '\t' + str(-1) + '\t' + str(-1) + '\t'+ str(-1) + '\n'
            # print(output)
            f.writelines(output)
    end = time.perf_counter()
    print("my-rpmalloc : %f" % (end - start))
    f.close()


###########################################################################

 ####     #####      ##     ##   ##   ####    ##  ##    ####
 ## ##    ##  ##    ####    ##   ##    ##     ### ##   ##  ##
 ##  ##   ##  ##   ##  ##   ##   ##    ##     ######   ##
 ##  ##   #####    ######   ## # ##    ##     ######   ## ###
 ##  ##   ####     ##  ##   #######    ##     ## ###   ##  ##
 ## ##    ## ##    ##  ##   ### ###    ##     ##  ##   ##  ##
 ####     ##  ##   ##  ##   ##   ##   ####    ##  ##    ####

###########################################################################


    with open('result_ref.txt', 'r') as file_ref:
        lines_ref = file_ref.readlines()

    with open('result.txt', 'r') as file:
        lines = file.readlines()

    columns = lines[0].strip().split('\t')[1:]

    data_ref = {}
    data = {}
    for line_ref, line in zip(lines_ref[1:], lines[1:]):
        parts_ref = line_ref.strip().split('\t')
        parts = line.strip().split('\t')
        testing = parts[0]
        values_ref = [float(value.replace(',', '')) for value in parts_ref[1:]]
        values = [float(value.replace(',', '')) for value in parts[1:]]
        data_ref[testing] = values_ref
        data[testing] = values

    for i, column in enumerate(columns):
        fig, ax = plt.subplots(figsize=(8, 6))
        x = np.arange(len(data))
        width = 0.35
        rects1 = ax.bar(x - width/2, [data_ref[testing][i] for testing in data_ref], width, label='rpmalloc')
        rects2 = ax.bar(x + width/2, [data[testing][i] for testing in data], width, label='my-rpmalloc')

        ax.set_ylabel(column)
        ax.set_title(column + ' Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(list(data.keys()), rotation=90)
        ax.legend()

        ax.set_yscale('log')

        plt.tight_layout()
        plt.savefig(str(column) + '.png')