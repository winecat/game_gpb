:: author:staff
@Echo off 
title windows ����̨

cd %~dp0
set CURR_PATH=%cd%
echo �ļ��������ɣ����Ժ�
python exchange.py %CURR_PATH%/sproto %CURR_PATH%/sproto2proto
echo �������
pause 