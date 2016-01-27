# PyRDP
配置文件对应相对路径为 config/config.ini
	server：瘦客户端服务器内容
		host：瘦客户端服务器IP
		port：瘦客户端服务器端口号
	blacklist：瘦客户端远程桌面连接窗口下“本地设备”栏目下配置过滤项
		drives：驱动黑名单（多个以“;”隔开）
			可选项：无根目录;可移动磁盘;本地磁盘;网络驱动器;CD 驱动器;虚拟内存盘
		devices：设备黑名单（多个以“;”隔开）
