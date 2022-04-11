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
import pandas as pd

SW_VERSION='0.1'

DefaultFile='record_allocs.txt'

# log var
debugLog = 0
debugLogLevel=(0,1,2,3) # 0:no log; 1:op logic; 2:op; 3:verbose

# record_allocs.txt format
class Allocs:
	__alloc_name=('malloc','realloc','calloc','memalign','free','thread_done')

	__ra_format={
		__alloc_name[0]:'(\d+): \w+ (\w+) (\d+)',
		__alloc_name[1]:'(\d+): \w+ (\w+) (\w+) (\d+)',
		__alloc_name[2]:'(\d+): \w+ (\w+) (\d+) (\d+)',
		__alloc_name[3]:'(\d+): \w+ (\w+) \d+ (\d+)',
		__alloc_name[4]:'(\d+): \w+ (\w+)',
		__alloc_name[5]:'(\d+): \w+',
	}

	__allocs_count=__allocs_size={
		__alloc_name[0]:0,
		__alloc_name[1]:0,
		__alloc_name[2]:0,
		__alloc_name[3]:0,
		__alloc_name[4]:0,
		__alloc_name[5]:0,
	}

	__allocs_point={}

	__tid_allocs=__tid_frees={}

	def __alloc_add(self,tag,m):
		tid = m.group(1)
		old_point = ''

		if tag == 'calloc':
			size = int(m.group(3))*int(m.group(4))
		elif tag == 'realloc':
			old_point = m.group(3)
			if old_point == '0x0':
				print('realloc old point is 0x0: '+m.group(0))

			size = int(m.group(4))
		else:
			size = int(m.group(3))
		
		if debugLog >= debugLogLevel[2]:
			print('Alloc: ',size)
		
		self.__allocs_size[tag] += size
		
		if debugLog >= debugLogLevel[-2]:
			print('Total Alloc: ',self.__allocs_size[tag])
		
		cur_point = m.group(2)
		self.__allocs_point[cur_point] = size

		if old_point and old_point != '0x0':
			self.__allocs_point[old_point] = 0

		if tid in self.__tid_allocs:
			self.__tid_allocs[tid] += size
		else:
			self.__tid_allocs[tid] = size	
	
	def __alloc_sub(self,tag,m):
		tid = m.group(1)
		cur_point = m.group(2)

		if debugLog >= debugLogLevel[-2]:
			print('Tid: ',tid,' Free: ',cur_point,'Size: ',self.__allocs_point[cur_point])

		if tid in self.__tid_frees:
			self.__tid_frees[tid] += self.__allocs_point[cur_point]
		else:
			self.__tid_frees[tid] = self.__allocs_point[cur_point]
		
		self.__allocs_point[cur_point] = 0

	def statistic_count(self,tag):
		self.__allocs_count[tag]+=1

		if debugLog >= debugLogLevel[-2]:
			print(tag+' Count: ',self.__allocs_count[tag])

	def parse_alloc_line(self,tag,line):
		rg=self.__ra_format[tag]
	
		if debugLog >= debugLogLevel[-1]:
			print('Tag Format: '+rg)

		m=re.match(rg,line)
		if m:
			if tag in self.__alloc_name[0:-2]:
				self.__alloc_add(tag,m)
			elif tag == 'free':
				self.__alloc_sub(tag,m)

	def tag_parse(self,line):
		alloc_rg='\d+: (\w+)'
	
		m = re.match(alloc_rg,line)
		if m:
			if debugLog >= debugLogLevel[-1]:
				print('Find: '+line)
		
			if debugLog >= debugLogLevel[-2]:
				print('Tag: '+m.group(1))
			
			return m.group(1)
		else:
			return None

	def output_info(self):
		df = pd.DataFrame(self.__allocs_count,index=[0])
		print('\nTotal Alloc Count:\n',df.T)		

		df = pd.DataFrame(self.__allocs_size,index=[0])
		print('\nTotal Alloc Size:\n',df.T)		
		
		df = pd.DataFrame(self.__tid_allocs,index=[0])
		print('\nTid Alloc:\n',df.T)
	
		df.T.to_excel("Tid_Allocs.xlsx")		
		
		df = pd.DataFrame(self.__allocs_point,index=[0])
		print('\nAlloc Point:\n',df.T)		
		
		print('\nAlloc Sum:\n',df.T.sum())
		df.T.to_excel("Allocs.xlsx")		
	
sta = Allocs()

def parse_file(f):
	while 1:
		line = f.readline()

		if not line:
			print("Finish Parse File!")

			sta.output_info()

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
