:: author:staff
@Echo off 
title windows ����̨
color 0A

cd %~dp0
set CURR_PATH=%cd%
set RULES_PATH=%CURR_PATH%/./../prot/rules
set PROTO_PATH=%CURR_PATH%/proto
echo ���� %RULES_PATH%
echo �����ļ�...
cd %RULES_PATH%\
del *.xml /f /q /a >nul
cd %CURR_PATH%
echo ת���ļ���ʼ�����Ժ�...
python proto2rules.py %PROTO_PATH% %RULES_PATH%
echo �������
pause 