:: author:staff
@Echo off 
title windows 控制台
color 0A

cd %~dp0
set CURR_PATH=%cd%
set RULES_PATH=%CURR_PATH%/./../prot/rules
set PROTO_PATH=%CURR_PATH%/proto
echo 进入 %RULES_PATH%
echo 清理文件...
cd %RULES_PATH%\
del *.xml /f /q /a >nul
cd %CURR_PATH%
echo 转换文件开始，请稍后...
python proto2rules.py %PROTO_PATH% %RULES_PATH%
echo 操作完成
pause 