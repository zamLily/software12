import paramiko


class SSHManager:
    '''
    ssh connect class
    '''
    def __init__(self, host, port, usr, passwd):
        self._host = host
        self._usr = usr
        self._passwd = passwd
        self._port = port
        self._ssh = None
        self._ssh_connect()

    def __del__(self):
        if self._ssh:
            self._ssh.close()

    def _ssh_connect(self):
        try:
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh.connect(hostname=self._host,
                              port=self._port,
                              username=self._usr,
                              password=self._passwd,
                              timeout=60)
        except Exception :
            raise RuntimeError("ssh connected to [host:%s, usr:%s, passwd:%s] failed" %
                               (self._host, self._usr, self._passwd))

    def ssh_exec_cmd(self, cmd):
        try:
            result = self._exec_command(cmd)
            # print(result)
            return result[0]
        except Exception:
            raise RuntimeError('exec cmd [%s] failed' % cmd)

    def _exec_command(self, cmd):
        try:
            _, stdout, stderr = self._ssh.exec_command(cmd)
            return stdout.read().decode(), stderr.read().decode()
        except Exception:
            raise RuntimeError('Exec command [%s] failed' % str(cmd))


class DockerApi():
    """
    docker class
    """
    def __init__(self, ssh_client):
        if not isinstance(ssh_client, SSHManager):
            raise RuntimeError('ssh_client is not SSHManager object')
        self.ssh_client = ssh_client

    def create_container(self,image_id, gpu_num):
        try:
            command = 'sudo docker run -itd --rm --gpus={0} {1} /bin/bash'.format(gpu_num, image_id)
            # print(command)
            self.container_id = self.ssh_client.ssh_exec_cmd(command)[:12]
        except Exception as e:
            print(e.args)
            print('start container error')

    def train_file(self, remote_file_dir, run_file_name):
        # copy file to container
        copy_command = 'sudo docker cp {0} {1}:/data/'.format(remote_file_dir, self.container_id)
        # print(copy_command)
        self.ssh_client.ssh_exec_cmd(copy_command)
        # run python file
        if run_file_name.endswith('py'):
            run_cmd = 'sudo docker exec -i {0} /bin/bash -c \'python {1}/{2}\''.format(self.container_id, '/data', run_file_name)
        else:
            run_cmd ='sudo docker exec -i {0} /bin/bash -c \'sh {1}/{2}\''.format(self.container_id, '/data', run_file_name)
        # print(run_cmd)
        result = self.ssh_client.ssh_exec_cmd(run_cmd)
        return result

    def stop_container(self):
        stop_cmd = 'sudo docker stop {}'.format(self.container_id)
        self.ssh_client.ssh_exec_cmd(stop_cmd)


def docker_test(file_name, ip, port, password, gpu_user, gpu_num):
    """
    :param student_id:
    :param file_name:
    :param ip:
    :param port:
    :param password:
    :param gpu_user:
    :param gpu_num:
    :return:
    """
    # clinet = SSHManager('120.78.13.73', 22, 'root', '1314ILYmm')
    clinet = SSHManager(ip, port, gpu_user, password)
    api = DockerApi(clinet)
    api.create_container('tensorflow/tensorflow:latest-gpu', gpu_num)
    # 用户代码在服务器上的路径+代码文件名
    result = api.train_file('/home/dc2-user', file_name)
    api.stop_container()
    # 释放占用的gpu
    free_gpu_list.append(gpu)
    return result

# gpu列表
num = 1
free_gpu_list = []
for i in range(num):
    free_gpu_list.append(i)
gpu = None

file_name = 'mnist.py'
ip = '116.85.38.198'
port = 22
gpu_user = 'dc2-user'
password = 'Hx1021$&@'

# 获取空闲的gpu
if free_gpu_list:
    gpu = free_gpu_list.pop(0)
    print(gpu)
    res = docker_test(file_name, ip, port, password, gpu_user, gpu)
    print(res)
    # 本地存储用户代码输出的文件名
    filename = 't_t.txt'
    with open(filename, 'w') as file_object:
        file_object.write(res)
else:
    print('暂无空闲gpu')

