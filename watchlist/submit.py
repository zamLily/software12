#!usr/bin/python
# coding: utf-8


import paramiko
# import json
# remotedir='/tmp/log'
# remotefile = 'bst_manager-2019-04-17-info.log'
# hostname = '120.78.13.73'
# port = 8022
# username = 'root'
# password ='1314ILYmm'
# command = """tail -n 30 /tmp/log/bst_manager-2019-04-17-info.log | grep 'other'"""


# def ssh_remote():
#     """ 1、基于用户名和密码连接
#     """
#     print ("基于用户名和密码连接")
#     # 创建SSH对象
#     ssh = paramiko.SSHClient()
#     # 允许连接不再know_host文件的主机
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     # 连接服务器
#     ssh.connect(hostname, port, username, password)
#     # 执行命令
#     stdin, stdout, stderr = ssh.exec_command(command)
#     data = stdout.readline()
#     cloud_data = json.loads(data)['other']

#     with open("../test_data_dev/data.json", 'w+', 0) as f:
#         cloud_data = json.dumps(cloud_data, indent=4, separators=(',', ':'))
#         f.write(cloud_data)
#     ssh.close()
#     print ("1. over\n\n\n")

#
# def ssh_remote_moth2():
#
#     """ 2、基于用户名和密码连接
# """
#     print ("基于用户名和密码连接，使用SSHClient, 封装Transport")
#     ssh = paramiko.SSHClient()
#     transport = paramiko.Transport(sock=(hostname, port))
#     # print transport
#     transport.connect(username=username, password=password)
#
#     ssh._transport = transport
#     stdin, stdout, stderr = ssh.exec_command(command)
#     data = json.loads(stdout.readline())["other"]
#
#     with open("../test_data_dev/data.json", 'w+', 0) as f:
#         cloud_data = json.dumps(data, indent=4, separators=(',', ':'))
#         f.write(cloud_data)
#     ssh.close()
#
#     transport.close()
#     print ('2. over \n\n\n')
#
#
# def down_device_file():
#
#     transport = paramiko.Transport(('192.168.50.34', 8022))
#     transport.connect(username='root', password='O3OwTr(01{@sVhDL')
#
#     sftp = paramiko.SFTPClient.from_transport(transport)
#     sftp.put('/tmp/location.txt', '/tmp/sensoro/server.txt')
#
#     # 检查有无上传成功
#     ssh = paramiko.SSHClient()
#     ssh._transport = transport
#     stdin, stdout, stderr = ssh.exec_command('ls -al /tmp/sensoro/')
#     print(str(stdout.read(), encoding='utf-8'))
#
#     # 将remove_path 下载到本地 local_path
#     sftp.get('/root/conf/bst_conf.json', '/Users/linyue/mywork/server_file/bst_conf.json')
#
#     transport.close()
#     print("3. over")

def submit_file(localfile,remotefile,ip,port,username,password):
    # 实例化一个trans对象# 实例化一个transport对象
    transport = paramiko.Transport((ip,port))
    # 建立连接
    transport.connect(username=username, password=password)
    # 实例化一个 sftp对象,指定连接的通道
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(localfile, remotefile)
    # LocalFile.txt 上传至服务器 /home/fishman/test/remote.txt
    #sftp.put(file_name, '/code/test.py')
    # # 将LinuxFile.txt 下载到本地 fromlinux.txt文件中
    # sftp.get('/home/fishman/test/LinuxFile.txt', 'fromlinux.txt')
    transport.close()

    # # 实例化一个trans对象# 实例化一个transport对象
    # transport = paramiko.Transport(('120.78.13.73',22 ))
    # # 建立连接
    # transport.connect(username='root', password='1314ILYmm')
    # # 实例化一个 sftp对象,指定连接的通道
    # sftp = paramiko.SFTPClient.from_transport(transport)
    
    # # LocalFile.txt 上传至服务器 /home/fishman/test/remote.txt
    # sftp.put('LocalFile.txt', '/code/remote.txt')
    # # # 将LinuxFile.txt 下载到本地 fromlinux.txt文件中
    # # sftp.get('/home/fishman/test/LinuxFile.txt', 'fromlinux.txt')
    # transport.close()

# user = 'misaka'
# file_name = 'test.py'
# ip = '120.78.13.73'
# port = 22
# username = 'root'
# password = '1314ILYmm'
# remotefile = r'/root/test.py'
# localfile = r'C:\Users\Administrator\ruangong\software12\watchlist\test.py'
# submit_file(localfile,remotefile,ip,port,username,password)