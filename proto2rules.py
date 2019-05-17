#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import string, os, sys
import re
from collections import defaultdict
import random

## 协议集合
class protos:
	def __init__(self):
		self.name = ""
		self.requests = []
		self.responses = []
## 协议体
class proto:
	def __init__(self):
# 		self.cmd = ""
		self.fields = []
		self.desc = ""
## 数据域		
class field:
	def __init__(self):
		self.type = ""
		self.name = ""
		self.desc = ""
		self.is_array = False
		
## 宏 数据域
class macro:
	def __init__(self):
		self.name = ""
		self.desc = ""
		self.lists = []
		

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
	
# 遍历文件
def parse_files(input_path, output_path):
	files = get_all_files(input_path)
	global golbal_macro_list
	golbal_macro_list = []
	for each_file in files:
		allfilename = os.path.basename(each_file)
		(filename, extension) = os.path.splitext(allfilename)
		prefix = filename[0:3]
		value = re.compile(r'^[0-9]+$')
		result = value.match(prefix)
		if result:##有协议号的
			golbal_macro_list = parse_proto_file(each_file, filename, int(prefix) * 100, output_path, golbal_macro_list)
		else:
			golbal_macro_list = parse_proto_file(each_file, filename, 0, output_path, golbal_macro_list)
	## 写_macro.xml
	macro_file = output_path + "/" + "_macro.xml"
	generate_macro_file(golbal_macro_list, "_macro", output_path)
	return

def parse_proto_file(file, filename, calc_proto, output_path, golbal_macro_list):
	## 分析协议
	result = analyze_proto(file, golbal_macro_list)
	analyse_protos = result[0]
	golbal_macro_list = result[1]
	if len(analyse_protos.requests) or len(analyse_protos.responses):
		generate_proto_file(analyse_protos, calc_proto, filename, output_path)
	return golbal_macro_list

def analyze_proto(file, golbal_macro_list):
	allfilename = os.path.basename(file)
	print "analyze file:%s"%(allfilename)
	read_file = open(file, "r")
	lines = read_file.readlines()
	## 赋值模块命名
	tmp_protos = protos()
	(filename, extension) = os.path.splitext(allfilename)
	tmp_protos.name = filename[4:]
	mark = 99##	0 request 1 response -1 list
	start = 0
	line_number = 0
	for line in lines:
		line_number += 1
		## 识别sc 空协议
		m = re.match(r"^message\s*(sc_\w*) {\s*}", line)
		if m:
			tmp_proto = proto()
			tmp_proto.desc = replace_space(m.group(1))
			tmp_proto.fields = []
			tmp_protos.responses.append(tmp_proto)
			mark = 99
			start = 0
			continue
		## 识别sc 协议
		m = re.match(r"^message\s*(sc_\w*) {", line)
		if m:
			mark = 1
			tmp_proto = proto()
			tmp_proto.desc = replace_space(m.group(1))
			tmp_proto.fields = []
			start = 1
			continue
		
		## 识别cs 空协议
		m = re.match(r"^message\s*(cs_\w*) {\s*}", line)
		if m:
			tmp_proto = proto()
			tmp_proto.desc = replace_space(m.group(1))
			tmp_proto.fields = []
			tmp_protos.requests.append(tmp_proto)
			mark = 99
			start = 0
			continue
		## 识别cs 协议
		m = re.match(r"^message\s*(cs_\w*) {", line)
		if m:
			mark = 0
			tmp_proto = proto()
			tmp_proto.desc = replace_space(m.group(1))
			tmp_proto.fields = []
			start = 1
			continue
		## 识别  空宏
		m = re.match(r"^message\s*(\w*) {\s*}", line)
		if m:
			tmp_macro = macro()
			tmp_macro.desc = replace_space(m.group(1))
			tmp_macro.name = replace_space(m.group(1))
			tmp_macro.lists = []
			golbal_macro_list.append(tmp_macro)
			mark = 99
			start = 0
			continue
		## 识别 宏
		m = re.match(r"^message\s*(\w*) {", line)
		if m:
			mark = -1
			tmp_macro = macro()
			tmp_macro.desc = replace_space(m.group(1))
			tmp_macro.name = replace_space(m.group(1))
			tmp_macro.lists = []
			start = 1
			continue
		## 识别 fields required optional has comment
		m = re.match(r"^\s*(required|optional)\s*(\w*)\s*(\w*)\s*=\s*\d*;\s*//([\S*|\s*]*)\n$", line)
		if m:
			tmp_field = field()
			tmp_field.type = data_type(m.group(2))
			tmp_field.name = replace_space(m.group(3))
			tmp_field.desc = replace_space(m.group(4))
			if mark == -1:
				tmp_macro.lists.append(tmp_field)
			elif mark == 0:
				tmp_proto.fields.append(tmp_field)
			elif mark == 1:
				tmp_proto.fields.append(tmp_field)
			else:
				print "file:%s, line number:%d error mark:%d"%(allfilename, line_number, mark)
			continue
		## 识别 fields required optional has no comment
		m = re.match(r"^\s*(required|optional)\s*(\w*)\s*(\w*)\s*=\s*\d*;", line)
		if m:
			tmp_field = field()
			tmp_field.type = data_type(m.group(2))
			tmp_field.name = replace_space(m.group(3))
			if mark == -1:
				tmp_macro.lists.append(tmp_field)
			elif mark == 0:
				tmp_proto.fields.append(tmp_field)
			elif mark == 1:
				tmp_proto.fields.append(tmp_field)
			else:
				print "file:%s, line number:%d error mark:%d"%(allfilename, line_number, mark)
			continue
		## 识别 fields repeated has comment
		m = re.match(r"^\s*repeated\s*(\w*)\s*(\w*)\s*=\s*\d*;\s*//([\S*|\s*]*)\n$", line)
		if m:
			tmp_field = field()
			tmp_field.type = data_type(m.group(1))
			tmp_field.name = replace_space(m.group(2))
			tmp_field.desc = replace_space(m.group(3))
			tmp_field.is_array = True
			if mark == -1:
				tmp_macro.lists.append(tmp_field)
			elif mark == 0:
				tmp_proto.fields.append(tmp_field)
			elif mark == 1:
				tmp_proto.fields.append(tmp_field)
			else:
				print "file:%s, line number:%d error mark:%d"%(allfilename, line_number, mark)
			continue
		## 识别 fields repeated has no comment
		m = re.match(r"^\s*repeated\s*(\w*)\s*(\w*)\s*=\s*\d*;", line)
		if m:
			tmp_field = field()
			tmp_field.type = data_type(m.group(1))
			tmp_field.name = replace_space(m.group(2))
			tmp_field.is_array = True
			if mark == -1:
				tmp_macro.lists.append(tmp_field)
			elif mark == 0:
				tmp_proto.fields.append(tmp_field)
			elif mark == 1:
				tmp_proto.fields.append(tmp_field)
			else:
				print "file:%s, line number:%d error mark:%d"%(allfilename, line_number, mark)
			continue
		## 协议包结束
		m = re.match(r"}", line)
		if m:
			if mark == -1:
				golbal_macro_list.append(tmp_macro)
			elif mark == 0:
				tmp_protos.requests.append(tmp_proto)
			elif mark == 1:
				tmp_protos.responses.append(tmp_proto)
			else:
				print "error mark:%d"%(mark)
			mark = 99
			start = 0
			continue
	return [tmp_protos, golbal_macro_list]
			
## 生成协议文件
def generate_proto_file(protos, calc_proto, filename, output_path):
	file_str = """<?xml version="1.0\"?>
<document name=\"%s\" desc=\"\">\n"""%(protos.name)
	## 分析 requests
	file_str += "%s<requests>\n"%(tab(1))
	for request in protos.requests:
		file_str += "%s<request cmd=\"%d\" desc=\"%s\""%(tab(2), calc_proto, request.desc)
		calc_proto += 1
		if len(request.fields):
			file_str += ">\n"
			for field in request.fields:
				if field.is_array:
					file_str += "%s<field type=\"%s\" name=\"%s\" array=\"true\" desc=\"%s\" />\n"%(tab(3), replace_array_type(field.type), field.name, field.desc)
				else:
					file_str += "%s<field type=\"%s\" name=\"%s\" desc=\"%s\" />\n"%(tab(3), field.type, field.name, field.desc)
			file_str += "%s</request>\n"%(tab(2))
		else:
			file_str += "/>\n"
	file_str += "%s</requests>\n"%(tab(1))
	## 分析 responses
	file_str += "%s<responses>\n"%(tab(1))
	for response in protos.responses:
		file_str += "%s<response cmd=\"%d\" desc=\"%s\""%(tab(2), calc_proto, response.desc)
		calc_proto += 1
		if len(response.fields):
			file_str += ">\n"
			for field in response.fields:
				if field.is_array:
					file_str += "%s<field type=\"%s\" name=\"%s\" array=\"true\" desc=\"%s\" />\n"%(tab(3), replace_array_type(field.type), field.name, field.desc)
				else:
					file_str += "%s<field type=\"%s\" name=\"%s\" desc=\"%s\" />\n"%(tab(3), field.type, field.name, field.desc)
			file_str += "%s</response>\n"%(tab(2))
		else:
			file_str += "/>\n"
	file_str += "%s</responses>\n"%(tab(1))
	file_str += "</document>\n"
	## 写文件
	output_file = output_path + "/" + filename + ".xml"
	outfile = open(output_file, 'w')
	outfile.write(file_str)
	outfile.close()
	return

##  生成宏文件
def generate_macro_file(golbal_macro_list, filename, output_path):
	file_str = """<?xml version="1.0"?>
<document name="global_list" desc="全局变量宏">\n"""
	file_str += "%s<lists>\n"%(tab(1))
	for macro in golbal_macro_list:
		file_str += "%s<list name=\"%s\" desc=\"%s\""%(tab(2), macro.name, macro.desc)
		if len(macro.lists):
			file_str += ">\n"
			for field in macro.lists:
				if field.is_array:
					file_str += "%s<field type=\"%s\" name=\"%s\" array=\"true\" desc=\"%s\" />\n"%(tab(3), replace_array_type(field.type), field.name, field.desc)
				else:
					file_str += "%s<field type=\"%s\" name=\"%s\" desc=\"%s\" />\n"%(tab(3), field.type, field.name, field.desc)
			file_str += "%s</list>\n"%(tab(1))
		else:
			file_str += "/>\n"
	file_str += "%s</lists>\n"%(tab(1))
	file_str += "</document>\n"
	## 写文件
	output_file = output_path + "/" + filename + ".xml"
	outfile = open(output_file, 'w')
	outfile.write(file_str)
	outfile.close()
	return
 
# 解析目录下所有定义文件
def get_all_files(dirname):
	files = os.listdir(dirname)
	for i in range(0, len(files)):
		files[i] = dirname + os.sep + files[i]
	files = filter_files(files)
	files = sort_files(files)
	return files

# 过滤文件
def filter_files(files):
	newfiles = []
	for f in files:
		if f.endswith('.proto'):
			newfiles.append(f)
	return newfiles

# 制表符tab换成4个空格
def tab(n):
	return " " * 4 * n;

## 映射数据类型 
def data_type(proto_type):
	proto_type = str(proto_type).replace(' ', '')
	#print "proto_type is %s"%(proto_type)
	proto2rules = {
		"int32":"int32",
		"string":"string",
		"bool":"int8"
	}
	return proto2rules.get(proto_type, proto_type)
	
## 过滤所有空格
def replace_space(maybe_str):
	return str(maybe_str).replace(' ', '')

## 替换整型列表
def replace_array_type(type_str):
	proto2rules = {
		"int32":"integer_list",
	}
	return proto2rules.get(type_str, type_str)

#生成
input_path = sys.argv[1]
output_path = sys.argv[2]
parse_files(input_path, output_path)

