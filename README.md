# record_allocs_parse

1.Catch cmd:
adb shell setprop libc.debug.malloc.program app
adb shell setprop libc.debug.malloc.options "\"verbose record_allocs\""
for /f %%i in ('adb shell pidof app') do set pid=%%i
adb shell kill -9 %pid%

adb shell setenforce 0
for /f %%i in ('adb shell pidof app') do set pid=%%i
adb shell kill -46 pid
