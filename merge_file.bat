:: author:staff
@Echo off 
title windows ����̨

cd %~dp0
set CURR_PATH=%cd%
echo �����ļ�...
cd %CURR_PATH%\proto
del *.proto /f /s /q /a >nul
cd %CURR_PATH%
echo �ļ��������ɣ����Ժ�
python merge_file.py %CURR_PATH%/sproto2proto %CURR_PATH%/proto
echo �������
pause 