# record_allocs_parse

1.Catch cmd:
adb shell setprop libc.debug.malloc.program app
adb shell setprop libc.debug.malloc.options "\"verbose record_allocs\""
adb shell kill -9 pid

adb shell setenforce 0
adb shell kill -46 pid
