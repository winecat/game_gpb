:: author:staff
@Echo off 
title windows 控制台

cd %~dp0
set CURR_PATH=%cd%
echo 文件正在生成，请稍后
python exchange.py %CURR_PATH%/sproto %CURR_PATH%/sproto2proto
echo 操作完成
pause 