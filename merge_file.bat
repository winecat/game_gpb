:: author:staff
@Echo off 
title windows 控制台

cd %~dp0
set CURR_PATH=%cd%
echo 清理文件...
cd %CURR_PATH%\proto
del *.proto /f /s /q /a >nul
cd %CURR_PATH%
echo 文件正在生成，请稍后
python merge_file.py %CURR_PATH%/sproto2proto %CURR_PATH%/proto
echo 操作完成
pause 