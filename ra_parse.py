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

DefaultFile='record_allocs.txt'

# log var
debugLog = 0
debugLogLevel=(0,1,2,3) # 0:no log; 1:op logic; 2:op; 3:verbose

# record_allocs.txt format
class Allocs:
	__alloc_name=('malloc','realloc','calloc','memalign','free')
	__ra_format={
		alloc_name[0]:'(\d+): \w+ (\w+) (\d+)',
		alloc_name[1]:'(\d+): \w+ (\w+) \w+ (\d+)',
		alloc_name[3]:'(\d+): \w+ (\w+) (\d+) (\d+)',
		alloc_name[4]:'(\d+): \w+ (\w+) \d+ (\d+)',
		alloc_name[2]:'(\d+): (\w+)',
	}

	__tid_allocs=__tid_frees={}

	__allocs_count=__allocs_size={
		alloc_name[0]:0,
		alloc_name[1]:0,
		alloc_name[2]:0,
		alloc_name[3]:0,
		alloc_name[4]:0,
	}

	__allocs_point={}

	def __alloc_add(tag,m):
		if tag == 'calloc':
			size = int(m.group(3))*int(m.group(4))
		else
			size = int(m.group(3))
		
		if debugLog >= debugLogLevel[2]:
			print('Alloc: ',size)
	
	def __alloc_sub(tag,m):
		if debugLog >= debugLogLevel[2]:
			print('Free: ',m.group(2))

	def statistic_count(self,tag):
		self.__	allocs_count[tag]+=1

		if debugLog >= debugLogLevel[2]:
			print(tag+' Count: ',self.__allocs_count[tag])

	def parse_alloc_line(self,tag,line):
		rg=ra_format[tag]
	
		if debugLog >= debugLogLevel[2]:
			print('Tag Format: '+rg)

		m=re.match(rg,line)
		if m:
			if debugLog >= debugLogLevel[1]:
				print('Tag Format: '+rg)

			if tag in self.__alloc_name[0:-2]:
				self.__alloc_add(tag,m)
			else:
				self.__alloc_sub(tag,m)

	def tag_parse(self,line):
		alloc_rg='\d+: (\w+)'
	
		m = re.match(alloc_rg,line)
		if m:
			if debugLog >= debugLogLevel[-1]:
				print('Find: '+line)
		
			if debugLog >= debugLogLevel[2]:
				print('Tag: '+m.group(1))
			
			return m.group(1)
		else:
			return None
	
Allocs sta

def parse_file(f):
	while 1:
		line = f.readline()

		if not line:
			print("Finish Parse File!")
			break
		
		tag = sta.tag_parse(line)

		if tag is not None:
			sta.statistic_count(tag)
			
			sta.parse_alloc_line(tag,line)


def main():
	fd = open(DefaultFile,'r')

	parse_file(fd)


if __name__=='__main__':
	print("Version: "+SW_VERSION)
	main()
