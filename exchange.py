#!/usr/bin/env python
# -*- coding: UTF-8 -*-


## 信息参考:
## https://blog.codingnow.com/2014/07/ejoyproto.html
## https://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html
## https://github.com/cloudwu/sproto
## https://blog.csdn.net/yi_ya/article/details/40404231


import string, os, sys
import re
from collections import defaultdict
import random

# 过滤文件
def filter_files(files):
	newfiles = []
	for f in files:
		if f.endswith('.sproto'):
			newfiles.append(f)
	return newfiles

# 解析一个错误码定义文件
cmd = 0
def parse_each_file(f, output_path):
	allfilename = os.path.basename(f)
	(filename,extension) = os.path.splitext(allfilename)
	text_file = open(f, "r")
	outfile_name = output_path + "/" + filename + ".proto"
	print "filename is %s, output file is %s" % (allfilename, outfile_name)
	outfile = open(outfile_name, 'w')
	lines = text_file.readlines()
	file_str = "import \"protomacro.proto\";\n\n"
	calc_left = 0
	reponse_skip = 0
	for line in lines:
		#print line
		#print "line is %s" % (line)
		#######################################
		## parse start ########################
		#######################################
		m = re.match(r"^\s*\}", line)
		# print "calc left is %d"%(calc_left)
		## skip  request {*}
		if m:
			if reponse_skip == 1:
				reponse_skip = 0
				continue
		if reponse_skip == 1:
			continue
		## skip reponse mark
		m = re.match(r"^\s*response\s{", line)
		if m:
			reponse_skip = 1
			continue
		## match empty message
		m = re.match(r"^(\w*)\s*\d*\s*\{\s*\}", line)
		if m:
			#准备文件
			message = str(m.group(1))
			file_str += "message %s {}\n"%(message)
			continue
			
		## match message
		m = re.match(r"^\.(\w*)\s*\{\s*", line)
		if m:
			#准备文件
			message = str(m.group(1))
			file_str += "message %s {\n"%(message)
			continue
		## match message
		m = re.match(r"^(\w*)\s*\d*\s*\{\s*", line)
		if m:
			#准备文件
			message = str(m.group(1))
			file_str += "message %s {\n"%(message)
			continue
		## match request {}
		m = re.match(r"^\s*request\s*\{\s*\}", line)
		if m:
			continue
		## match request
		m = re.match(r"^\s*request\s{", line)
		if m:
			calc_left += 1
			continue
		## required int32
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*integer\s*\#\s*(\S*)", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			p_comment = str(m.group(3))
			file_str += "	required     int32     %s = %d;     // %s \n"%(p_name, p_num, p_comment)
			continue
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*integer", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			file_str += "	required     int32     %s = %d;\n"%(p_name, p_num)
			continue
		## optional int32
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*\*integer\s*\#\s*(\S*)", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			p_comment = str(m.group(3))
			file_str += "	optional     int32     %s = %d;     // %s \n"%(p_name, p_num, p_comment)
			continue
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*\*integer", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			file_str += "	optional     int32     %s = %d;\n"%(p_name, p_num)
			continue
		## required bool
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*boolean\s*\#\s*(\S*)", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			p_comment = str(m.group(3))
			file_str += "	required     bool     %s = %d;     // %s \n"%(p_name, p_num, p_comment)
			continue
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*boolean", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			file_str += "	required     bool     %s = %d;\n"%(p_name, p_num)
			continue
		## optional bool
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*\*boolean\s*\#\s*(\S*)", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			p_comment = str(m.group(3))
			file_str += "	optional     bool     %s = %d;     // %s \n"%(p_name, p_num, p_comment)
			continue
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*\*boolean", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			file_str += "	optional     bool     %s = %d;\n"%(p_name, p_num)
			continue
		## required string
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*string\s*\#\s*(\S*)", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			p_comment = str(m.group(3))
			file_str += "	required     string     %s = %d;     // %s \n"%(p_name, p_num, p_comment)
			continue
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*string", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			file_str += "	required     string     %s = %d;\n"%(p_name, p_num)
			continue
		## optional string
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*\*string\s*\#\s*(\S*)", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			p_comment = str(m.group(3))
			file_str += "	optional     string     %s = %d;     // %s \n"%(p_name, p_num, p_comment)
			continue
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*\*string", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			file_str += "	optional     string     %s = %d;\n"%(p_name, p_num)
			continue
			
		## repeated message
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*\*(\w*)", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			p_type = str(m.group(3))
			file_str += "	repeated     %s     %s = %d;\n"%(p_type, p_name, p_num)
			continue
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*\*(\w*)\s*\#\s*(\S*)", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			p_type = str(m.group(3))
			p_comment = str(m.group(4))
			file_str += "	repeated     %s     %s = %d;     // %s\n"%(p_type, p_name, p_num, p_comment)
			continue
		## required message
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*(\w*)", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			p_type = str(m.group(3))
			file_str += "	required     %s     %s = %d;\n"%(p_type, p_name, p_num)
			continue
		m = re.match(r"^\s*(\w*)\s*(\d*)\s*\:\s*(\w*)\s*\#\s*(\S*)", line)
		if m:
			p_name = str(m.group(1))
			p_num = int(m.group(2))
			p_type = str(m.group(3))
			p_comment = str(m.group(4))
			file_str += "	required     %s     %s = %d;     // %s\n"%(p_type, p_name, p_num, p_comment)
			continue

			
		m = re.match(r"^\s*\}", line)
		# print "calc left is %d"%(calc_left)
		## skip  request {*}
		if m:
			if calc_left > 0:
				calc_left -= 1
				continue
			else:
				file_str += line
				continue
		
		new_line = line.replace("#", "//")
		file_str += new_line
		
	outfile.write(file_str)
	outfile.close()


# 解析目录下所有定义文件
def get_all_files(dirname):
	files = os.listdir(dirname)
	for i in range(0, len(files)):
		files[i] = dirname + os.sep + files[i]
	
	files = filter_files(files)
	return files
	

def parse_files(input_path, output_path):
    files = get_all_files(input_path)
    for f in files:
        print "parse file :" + f
        parse_each_file(f, output_path)
    
    
    
    
#生成
input_path = sys.argv[1]
output_path = sys.argv[2]
parse_files(input_path, output_path)

