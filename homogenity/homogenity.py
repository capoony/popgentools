#!/usr/bin/python
import os
import argparse
import time
import Modules.homogenity


parser = argparse.ArgumentParser(description="""
                                 
Description
-----------
    This script calculates Woolf and Breslow-Day homogeneity tests p-values for population data stored in CMH-TEST output file""",
                                                formatter_class=argparse.RawDescriptionHelpFormatter,
epilog="""Prerequisites
-------------
    (1) python 2.7.2
    (2) rpy2 [http://rpy.sourceforge.net/rpy2.html]
    (3) R version >= 2.13
    (4) R packages: "Formula", "metafor" The packages can be found on these locations:
    Formula package: http://cran.r-project.org/web/packages/Formula/index.html
    metafor package: http://cran.r-project.org/web/packages/metafor/index.html
                                                                    
    You can install the packages by using the following two commands in a terminal window:
                                                                    
    R CMD INSTALL "path_to_Formula_package.tar.gz
    R CMD INSTALL "path_to_metafor_package.tar.gz

Input data
----------
    Input file is a tab delimited file that contains a lightweight representation of all pileup files of interest and CMH-test p-value.
    X	13103593	A	36:0:23:0:0:0	21:0:24:0:0:0	11:0:10:0:0:0	140:0:2:0:0:0	130:0:3:0:0:0	130:0:4:0:0:0	5.061228e-36
    X	11047682	A	26:0:10:0:0:0	18:0:11:0:0:0	10:0:11:0:0:0	154:0:0:0:0:0	156:0:3:0:0:0	132:0:0:0:0:0	2.81229e-35
    3L	10887969	C	0:0:52:23:0:0	0:0:48:23:0:0	0:0:26:10:0:0	0:0:178:0:0:0	0:0:165:1:0:0	0:0:172:0:0:0	2.825701e-35
    3R	3663650	        G	27:0:0:42:0:0	36:0:0:36:0:0	14:0:0:19:0:0	0:0:0:96:0:0	2:0:0:110:0:0	0:0:0:118:0:0	2.017181e-34
    X	3189168	        G	0:0:26:39:0:0	0:0:27:33:0:0	0:0:12:16:0:0	0:0:0:96:0:0	0:0:0:112:0:0	0:0:0:106:0:0	3.682282e-33
    2R	15696127	A	53:0:16:0:0:0	41:0:16:0:0:0	16:0:13:0:0:0	174:0:0:0:0:0	145:0:1:0:0:0	188:0:2:0:0:0	1.751376e-32
    2L	7155362	        A	41:0:18:0:0:0	36:0:15:0:0:0	16:0:11:0:0:0	158:0:0:0:0:0	170:0:1:0:0:0	156:0:4:0:0:0	1.974774e-32
    2L	9775409	        A	32:0:18:0:0:0	19:0:19:0:0:0	11:0:9:0:0:0	126:0:4:0:0:0	148:0:0:0:0:0	104:0:4:0:0:0	1.92833e-31
    2R	4915797	        C	38:0:52:0:0:0	37:0:33:0:0:0	4:0:16:0:0:0	4:0:136:0:0:0	5:0:129:0:0:0	2:0:128:0:0:0	6.845953e-31
    2R	5231725	        A	44:1:26:0:0:0	44:0:14:0:0:0	12:1:8:0:0:0	164:0:2:0:0:0	120:0:0:0:0:0	156:2:0:0:0:0	5.731342e-30

    col 1: reference chromosome
    col 2: position in the reference chromosome
    col 3: reference genome base
    col 4: population 1
    col 5: population 2
    col 6: population 3
    col 7: population 4
    col 8: population 5
    col 9: population 6
    col 10: cmh p-value
    
    population data are in the form
    A:T:C:G:N:*
    A: count of character A
    T: count of character T
    C: count of character C
    G: count of character G
    N: count of character N
    *: deletion, count of deletion

                                
Output data
-----------
    Output file is same as input file with two additional coilumns 1) Woolf test p-value and 2) Breslow-Day test p-value
    X	13103593	A	36:0:23:0:0:0	21:0:24:0:0:0	11:0:10:0:0:0	140:0:2:0:0:0	130:0:3:0:0:0	130:0:4:0:0:0	5.061228e-36	0.865610355017	0.863767344187
    X	11047682	A	26:0:10:0:0:0	18:0:11:0:0:0	10:0:11:0:0:0	154:0:0:0:0:0	156:0:3:0:0:0	132:0:0:0:0:0	2.81229e-35	0.275577970881	0.215741344956
    3L	10887969	C	0:0:52:23:0:0	0:0:48:23:0:0	0:0:26:10:0:0	0:0:178:0:0:0	0:0:165:1:0:0	0:0:172:0:0:0	2.825701e-35	0.746034899145	0.736944120517
    3R	3663650	        G	27:0:0:42:0:0	36:0:0:36:0:0	14:0:0:19:0:0	0:0:0:96:0:0	2:0:0:110:0:0	0:0:0:118:0:0	2.017181e-34	0.608586299755	0.586645022144
    X	3189168	        G	0:0:26:39:0:0	0:0:27:33:0:0	0:0:12:16:0:0	0:0:0:96:0:0	0:0:0:112:0:0	0:0:0:106:0:0	3.682282e-33	0.98462788699	0.984768786767
    2R	15696127	A	53:0:16:0:0:0	41:0:16:0:0:0	16:0:13:0:0:0	174:0:0:0:0:0	145:0:1:0:0:0	188:0:2:0:0:0	1.751376e-32	0.816453669185	0.810516164131
    2L	7155362	        A	41:0:18:0:0:0	36:0:15:0:0:0	16:0:11:0:0:0	158:0:0:0:0:0	170:0:1:0:0:0	156:0:4:0:0:0	1.974774e-32	0.49029265516	0.415315837035
    2L	9775409	        A	32:0:18:0:0:0	19:0:19:0:0:0	11:0:9:0:0:0	126:0:4:0:0:0	148:0:0:0:0:0	104:0:4:0:0:0	1.92833e-31	0.167305601504	0.0719135336096
    2R	4915797	        C	38:0:52:0:0:0	37:0:33:0:0:0	4:0:16:0:0:0	4:0:136:0:0:0	5:0:129:0:0:0	2:0:128:0:0:0	6.845953e-31	0.808311137824	0.804750514933
    2R	5231725	        A	44:1:26:0:0:0	44:0:14:0:0:0	12:1:8:0:0:0	164:0:2:0:0:0	120:0:0:0:0:0	156:2:0:0:0:0	5.731342e-30	0.566449701581	0.555541274347

    col 1: reference chromosome
    col 2: position in the reference chromosome
    col 3: reference genome base
    col 4: population 1
    col 5: population 2
    col 6: population 3
    col 7: population 4
    col 8: population 5
    col 9: population 6
    col 10: cmh p-value
    col 11: woolf test p-value
    col 12: Breslow-Day test p-value


Parameters
---------- 
    Script homogenity.py expects three mandatory input parameters: --input, --output, and --populations.            
    The first two parameters are names of input and output file. 
                                                                    
    --populations 
    the parameter specifies pairs of populations for which the odds ratio will be calculated. 
    Each pair of populations has to be separated by a "," and the two populations for which 
    the odds ratio will be calculated by a "-". For example when user provides 1-4,2-5,3-6 the script 
    will calculate odds ratio for populations in fourth and sixth column and  odds ratio 
    for populations in fifth and seventh column. The columns are numbered from 1.

Execution time
-------------- 
    A synchronized file with 6 populations and 9,380,622 SNP took ~8 hours to run            

Authors
-------
Martina Visnovska
Ram Vinay Pandey

Example of a usage
------------------
python PopGenTools/homogenity/homogenity.py -i PopGenTools/homogenity/test_data/cmh-output -o PopGenTools/homogenity/test_data/cmh-output-homogenity-test -p 1-4,2-5,3-6

python PopGenTools/homogenity/homogenity.py --input PopGenTools/homogenity/test_data/cmh-output --output PopGenTools/homogenity/test_data/cmh-output-homogenity-test --population 1-4,2-5,3-6

Try to use the script on files in test_data folder.

    """)

parser.add_argument("-i","--input", required=True, dest="input", type=str, default=None, help="An output of cmh-test.pl from popoolation2 respository as input; Mandatory parameter")
parser.add_argument("-o", "--output", required=True, dest="output", type=str, default=None, help="An output file; Mandatory parameter")
parser.add_argument("-p", "--population", required=True, dest="population", type=str, default=None, help="Give population number from cmh-test output file [--population 1-4,2-5,3-6]; Mandatory parameter")

args = parser.parse_args()
input = args.input
output = args.output
population = args.population



localtime = time.asctime( time.localtime(time.time()) )
print "Started at :", localtime

### write param file
paramfile = output+".param"
pfh=open(paramfile,"w")
print >> pfh, "Using input\t"+str(input)
print >> pfh, "Using output\t"+str(output)
print >> pfh, "Using population\t"+str(population)
pfh.close()


pop_pair = Modules.homogenity.homogenity.read_populations(population,input)
Modules.homogenity.homogenity.SyncReader(input,output,pop_pair)

localtime = time.asctime( time.localtime(time.time()) )
print "Finshed at :", localtime