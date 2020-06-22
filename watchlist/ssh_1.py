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
                              timeout=5)
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
    def __init__(self, ssh_client):
        if not isinstance(ssh_client, SSHManager):
            raise RuntimeError('ssh_client is not SSHManager object')
        self.ssh_client = ssh_client

    def create_container(self, student_id, image_id):
        try:
            command = 'sudo docker run -itd --rm --gpus=all --name={0} {1} /bin/bash'.format(student_id, image_id)
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
            run_cmd = 'sudo docker exec -i {0} /bin/bash -c \'python {1}/{2}\''.format(self.container_id,'/data', run_file_name)
        else:
            run_cmd ='sudo docker exec -i {0} /bin/bash -c \'sh {1}/{2}\''.format(self.container_id, '/data', run_file_name)
        # print(run_cmd)
        result = self.ssh_client.ssh_exec_cmd(run_cmd)
        return result

    def stop_container(self):
        stop_cmd = 'sudo docker stop {}'.format(self.container_id)
        self.ssh_client.ssh_exec_cmd(stop_cmd)


def docker_test(user,file_name,ip,port,password):
    # clinet = SSHManager('120.78.13.73', 22, 'root', '1314ILYmm')
    clinet = SSHManager(ip, port, 'root', password)
    api = DockerApi(clinet)
    api.create_container(user, 'tensorflow/tensorflow')
    # 用户代码在服务器上的路径+代码文件名
    result = api.train_file('/root/code', file_name)
    api.stop_container()
    return result

#user = 'misaka'
#file_name = 'test.py'
#ip = '120.78.13.73'
#port = 22
#password = '1314ILYmm'
#res = docker_test(user,file_name,ip,port,password)
# 本地存储用户代码输出的文件名
#filename = 'test_tst.txt'
#with open(filename, 'w') as file_object:
#    file_object.write(res)