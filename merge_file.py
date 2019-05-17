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
def parse_files(input_path, output_path):
	files = get_all_files(input_path)
	## 排序
	files = sort_files(files)
	proto = 100
	for f in files:
		if f.endswith('.proto'):
			allfilename = os.path.basename(f)
			(filename,extension) = os.path.splitext(allfilename)
			prefix = filename[:-4]
			suffix = filename[-3:]
			#print "prefix is  " + prefix
			#print "suffix is  " + suffix
			if suffix == "s2c":
				merge_file(proto, prefix, input_path, output_path)
				proto += 1
			elif suffix == "c2s":
				continue;
			else:
				#print "file is %s"%(filename)
				single_file(filename, output_path)
	return 

def single_file(filename, output_path):
	file = input_path + "\\" + filename + ".proto"
	mergefile_name = output_path + "\\" + filename + ".proto"
	#print "file is %s\nmergefile_name is %s"%(file, mergefile_name)
	r_file = open(file, "r")
	w_mergefile = open(mergefile_name, "w")
	lines = r_file.readlines()
	append_file(False, lines, w_mergefile)
	r_file.close()
	w_mergefile.close()
	
	
def merge_file(proto, prefix, input_path, output_path):
	file_name1 = prefix + "_s2c.proto"
	file_name2 = prefix + "_c2s.proto"
	mergefile_name = str(proto) + "_" + prefix.lower() + ".proto"
	file1 = input_path + "\\" + file_name1
	file2 = input_path + "\\" + file_name2
	mergefile = output_path + "\\" + mergefile_name
	##print "file1 is %s\nfile2 is %s"%(file1, file2)
	r_file1 = open(file1, "r")
	r_file2 = open(file2, "r")
	w_mergefile = open(mergefile, "w")
	lines1 = r_file1.readlines()
	lines2 = r_file2.readlines()
	check1 = check_macro(lines1[0])
	check2 = check_macro(lines2[0])
	#print "check1 is %s\ncheck2 is %s"%(check1, check2)
	if check1 or check2:
		w_mergefile.write("import \"protomacro.proto\";")
	append_file(check1, lines1, w_mergefile)
	append_file(check2, lines2, w_mergefile)
	r_file1.close()
	r_file2.close()
	w_mergefile.close()
	
def append_file(check, lines, w_mergefile):
	count = 0
	for line in lines:
		if count == 0 and check:
			count += 1
			continue
		line = line.lower()
		w_mergefile.write(line)
		count += 1
		
def check_macro(line):
	#print "line is %s\n"%(line)
	m = re.match(r"^import \"protomacro.proto\";", line)
	if m:
		return True
	else:
		return False

	
	


# 解析目录下所有定义文件
def get_all_files(dirname):
	files = os.listdir(dirname)
	for i in range(0, len(files)):
		files[i] = dirname + os.sep + files[i]
	return files

#生成
input_path = sys.argv[1]
output_path = sys.argv[2]
parse_files(input_path, output_path)

