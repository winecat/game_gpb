@Echo off 
color 0A
setlocal enabledelayedexpansion
title 协议号生成脚本

cd %~dp0
set CMD_PATH=%cd%

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
 

rem echo 正在生成协议号文件，请稍后
python convert_cmd.py %PROTOBUFFS_PROTO_PATH% %PROTOBUFFS_SERVER_SRC_OUTPUT% %PROTOBUFFS_SERVER_INCLUDE_OUTPUT%
rem echo 操作结束^^! & pause