# record_allocs_parse

1.Catch cmd:
adb root
adb wait-for-device

adb shell setprop libc.debug.malloc.program app
adb shell setprop libc.debug.malloc.options "\"verbose record_allocs\""
for /f %%i in ('adb shell pidof app') do set pid=%%i
adb shell kill -9 %pid%
pause

adb shell setenforce 0
for /f %%i in ('adb shell pidof app') do set pid=%%i
adb shell kill -46 pid
pause

2.Get State cmd:
adb shell getenforce 
adb shell getprop libc.debug.malloc.program 
adb shell getprop libc.debug.malloc.options 
adb shell pidof app
pause
