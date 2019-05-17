@Echo off 
color 0A
setlocal enabledelayedexpansion
title Э������ɽű�

cd %~dp0
set CMD_PATH=%cd%

rem ��������
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
 

rem echo ��������Э����ļ������Ժ�
python convert_cmd.py %PROTOBUFFS_PROTO_PATH% %PROTOBUFFS_SERVER_SRC_OUTPUT% %PROTOBUFFS_SERVER_INCLUDE_OUTPUT%
rem echo ��������^^! & pause