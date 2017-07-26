from __future__ import print_function
import psutil

dps = psutil.disk_partitions()
fmt_str = "{:<8} {:<7} {:<7}"
print(fmt_str.format("Drive", "Type", "Opts"))
# Only show a couple of different types of devices, for brevity.
for i in (0, 2):
    dp = dps[i]
    print(fmt_str.format(dp.device, dp.fstype, dp.opts))
