#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import string, os, sys
import re
from collections import defaultdict
import random

# 文件排序
def sort_files(files):
	d = {}
	for f in files:
		allfilename = os.path.basename(f)
		(filename,extension) = os.path.splitext(allfilename)
		d[f] = filename
		
	sort_kv = sorted(d.items(), lambda x, y: cmp(x[1], y[1]))
	
	sort_list = []
	for i in range(0, len(sort_kv)):
		sort_list.append(sort_kv[i][0])
	
	return sort_list
	
# 过滤文件
def filter_files(files):
	newfiles = []
	for f in files:
		if f.endswith('.proto'):
			allfilename = os.path.basename(f)
			(filename, extension) = os.path.splitext(allfilename)
			prefix = filename[0:2]
			value = re.compile(r'^[0-9]+$')
			result = value.match(prefix)
			if result:
				newfiles.append(f)
	return newfiles
	
# 过滤文件
def parse_files(files, output):
	c2s1 = ""
	c2s2 = ""
	s2c1 = ""
	s2c2 = ""
	include_str = ""
	for file in files:
		## 头文件
		allfilename = os.path.basename(file)
		(filename, extension) = os.path.splitext(allfilename)
		include_str += "-include(\"%s.hrl\").\n"%(filename)
		## 编码/解码接口
		rt = parse_each_file(file)
		c2s1 = c2s1 + rt[0]
		c2s2 = c2s2 + rt[1]
		s2c1 = s2c1 + rt[2]
		s2c2 = s2c2 + rt[3]

	c2s_str = c2s1 + c2s2 + "c2s(_) -> undefoned.\n\n"
	s2c_str = s2c1 + s2c2 + "s2c(_) -> undefoned.\n\n"
	prefix_str = """%%%%\n%%%% @author staff
%%%% 协议映射模块
%%%% 系统自动生成，请别手动修改
%%%%
-module(\'protobuf_mapping\').\n\n%s\n\n
-export([s2c/1, c2s/1]).\n\n"""%(include_str)
	output.write(prefix_str)
	output.write(c2s_str)
	output.write(s2c_str)

def parse_each_file(file):
	allfilename = os.path.basename(file)
	(filename, extension) = os.path.splitext(allfilename)
	proto = int(filename[0:3]) * 100
	r_file = open(file, "r")
	lines = r_file.readlines()
	c2s1 = ""
	c2s2 = ""
	s2c1 = ""
	s2c2 = ""
	for line in lines:
		m = re.match(r"^message (cs_\w*) \{", line)
		if m:
			message = str(m.group(1))
			rpc = filename[4:] + "_rpc"
			c2s_str1= "c2s(%d) -> {%d, \'%s\', \'%s\', \'%s\', #%s{}};\n"%(proto, proto, filename, rpc, message, message)
			c2s_str2= "c2s(%s) -> {%d, \'%s\', \'%s\', \'%s\', #%s{}};\n"%(message, proto, filename, rpc, message, message)
			c2s1 = c2s1 + c2s_str1
			c2s2 = c2s2 + c2s_str2
			proto += 1
			continue
		m = re.match(r"^message (sc_\w*) \{", line)
		if m:
			message = str(m.group(1))
			s2c_str1 = "s2c(%d) -> {%d, \'%s\', #%s{}};\n"%(proto, proto, filename, message)
			s2c_str2 = "s2c(#%s{}) -> {%d, \'%s\', #%s{}};\n"%(message, proto, filename, message)
			s2c1 = s2c1 + s2c_str1
			s2c2 = s2c2 + s2c_str2
			proto += 1
			continue
	return [c2s1, c2s2, s2c1, s2c2]

	
def convert_files(input_path, output_path):
	print "parse proto files, wait..."
	output = gen_open_file(output_path)
	files = get_all_files(input_path)
	parse_files(files, output)
	output.close()
	print "convert mapping succeed...ok"
	
	
def gen_open_file(output_path):
	filename = output_path['src'] + "\protobuf_mapping.erl"
	output = open(filename, "w")
	return output
	
	


# 解析目录下所有定义文件
def get_all_files(dirname):
	files = os.listdir(dirname)
	for i in range(0, len(files)):
		files[i] = dirname + os.sep + files[i]
	files = filter_files(files)
	return files

#生成
input_path = sys.argv[1]
output_path = {'src':sys.argv[2], 'include':sys.argv[3]}
convert_files(input_path, output_path)

