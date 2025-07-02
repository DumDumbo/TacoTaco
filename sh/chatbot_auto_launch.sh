#!/bin/bash

Target="8.8.8.8"

# Check WIFI Connected Or Not
while true; do
	if /bin/ping -c 1 $Target &> /dev/null; then
		echo "网络已连接"
		aplay /home/dumbo/yd_workspace/config/Minions.wav
		break
	else
		echo "网络已连接, 无法访问互联网"
		aplay /home/dumbo/yd_workspace/config/please_check_network_connection.wav
		sleep 10
	fi
done




# 激活虚拟环境
source /home/dumbo/yd_workspace/yd_workspace_env/bin/activate

/home/dumbo/yd_workspace/scripts/wakeup_pvrecorder.py
