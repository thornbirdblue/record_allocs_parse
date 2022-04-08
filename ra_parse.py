#!/usr/bin/env python

##########################################################################
#       CopyRight       (C)     THORNBIRD,2030  All Rights Reserved!
#
#       Module:         Parse record_alloc.txt File
#
#       File:           ra_parse.py
#
#       Author:         thornbird
#
#       Date:           2022-04-08
#
#       E-mail:         thornbird_bri@163.com
#
###########################################################################

###########################################################################
#
#       History:
#       Name            Data            Ver             Act
#--------------------------------------------------------------------------
#       thornbird       2022-04-08      v1.0            create
#
###########################################################################

import sys,os,re,string,time,datetime

SW_VERSION='0.1'

DefaultFile='record_alloc.txt'

# log var
debugLog = 0
debugLogLevel=(0,1,2,3) # 0:no log; 1:op logic; 2:op; 3:verbose

# record_allocs.txt format
ra_format={
	'malloc':'(\d+): \w+ (\w+) (\d+)',
	'realloc':'(\d+): \w+ (\w+) \w+ (\d+)',
	'free':'(\d+): (\w+)',
	'calloc':'(\d+): \w+ (\w+) (\d+) (\d+)',
	'memalign':'(\d+): \w+ (\w+) (\d+) (\d+)',
}

def tag_parse(line):
	alloc_rg='\d+: (\w+)'
	
	m = re.match(alloc_rg,line)
	if m:
		if debugLog >= debugLogLevel[-1]:
			print('Find: '+line)
		
		if debugLog >= debugLogLevel[2]:
			print('Tag: '+m.group(1))
	

def parse_file(f):
	while 1:
		line = f.readline()

		if not line:
			print("Finish Parse File!")
			break
		
		tag = tag_parse(line)


def main():
	fd = open(DefaultFile,'r')

	parse_file(fd)


if __name__=='__main__':
	print("Version: "+SW_VERSION)
	main()
