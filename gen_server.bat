@echo off
color 0A
setlocal enabledelayedexpansion
title Makefile
rem 加载配置
set CONF=conf.ini
if not exist %CONF% (
    echo can not find conf.ini, please copy conf.ini.sample to conf.ini first
    pause
    goto:eof
)
for /f "tokens=1,2 delims==" %%i in (conf.ini) do (
  if "%%i"=="PROTOBUFFS_PROTO_PATH" set PROTOBUFFS_PROTO_PATH=%%j
  if "%%i"=="PROTOBUFFS_SERVER_SRC_OUTPUT" set PROTOBUFFS_SERVER_SRC_OUTPUT=%%j
  if "%%i"=="PROTOBUFFS_SERVER_INCLUDE_OUTPUT" set PROTOBUFFS_SERVER_INCLUDE_OUTPUT=%%j
 )
echo 协议文件目录
echo %PROTOBUFFS_PROTO_PATH%
echo 生成的服务端目录 
echo %PROTOBUFFS_SERVER_SRC_OUTPUT% 
echo %PROTOBUFFS_SERVER_INCLUDE_OUTPUT%
echo 操作开始...
set CURRENT_PATH=%~dp0
set PROTOBUFF_FILES=%PROTOBUFFS_PROTO_PATH%\*.proto
set PROTOC_ERL=%CURRENT_PATH%/gpb/bin/protoc-erl
for %%I in (erl.exe) do if "%%~$PATH:I"=="" (
	echo cannot find erl.exe, please install erlang and put the path into PATH
    pause
    goto:eof
)
echo .1.
echo clean all *.erl files...
cd %PROTOBUFFS_SERVER_SRC_OUTPUT%
del *.erl /f /q /a >nul
echo clean all *.hrl files...
cd %PROTOBUFFS_SERVER_INCLUDE_OUTPUT%
del *.hrl /f /q /a >nul

echo .2.
echo begin compile protobuf files...
cd %PROTOBUFFS_PROTO_PATH%
erl -make
for /f "delims=" %%I in ('dir /b /a-d /s %PROTOBUFF_FILES%') do (
	set filename=%%I
	for %%a in ("!filename!") do echo compile: %%~na%%~xa
    escript.exe %PROTOC_ERL% -o-erl %PROTOBUFFS_SERVER_SRC_OUTPUT% -o-hrl %PROTOBUFFS_SERVER_INCLUDE_OUTPUT% %%I
)
cd %CURRENT_PATH%
echo compile protobuf files end...ok

echo .3.
call convert_cmd

echo ---------------------------------
echo 服务端操作结束^^!
echo ---------------------------------
pause 
