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
            print("ssh connected to [host:%s, usr:%s, passwd:%s] succeed" %
                               (self._host, self._usr, self._passwd))
        except Exception:
            raise RuntimeError("ssh connected to [host:%s, usr:%s, passwd:%s] failed" %
                               (self._host, self._usr, self._passwd))

    def ssh_exec_cmd(self, cmd):
        try:
            result = self._exec_command(cmd)
            #print(result)
            # print("exec cmd [%s] succeed" % cmd)
            return result[0]
        except Exception:
            raise RuntimeError('exec cmd [%s] failed' % cmd)

    def _exec_command(self, cmd):
        try:
            _, stdout, stderr = self._ssh.exec_command(cmd)
            # print("Exec command [%s] succeed" % str(cmd))
            return stdout.read().decode(), stderr.read().decode()
        except Exception:
            raise RuntimeError('Exec command [%s] failed' % str(cmd))


class DockerApi():
    """
    docker class
    """
    def __init__(self, ssh_client, student):
        if not isinstance(ssh_client, SSHManager):
            raise RuntimeError('ssh_client is not SSHManager object')
        self.ssh_client = ssh_client
        self.student = student

    def run_container(self, gpu_num, image_name, file_name):
        # self.ssh_client.ssh_exec_cmd('cd /home/dc2-user')

        # run a container
        run_cmd = 'sudo docker run -itd --gpus={0} --name={1} -v $PWD/{2}/:/data -w /data {3} python {4}'.format(
            gpu_num, self.student, self.student, image_name, file_name)
        # print(run_cmd)
        self.ssh_client.ssh_exec_cmd(run_cmd)
        print("running the container...")

        save_rm_cmd = 'sudo docker logs {0} > {1}/{2}.txt && sudo docker rm -v {3}'.format(
            self.student, self.student, self.student, self.student)

        # save the container log and delete the container
        while True:
            status = self.ssh_client.ssh_exec_cmd('sudo docker ps | grep {0} | wc -l'.format(self.student))
            if int(status) == 1:
                print("status is {}, the code is running".format(int(status)))
            else:
                print("finished running")
            if int(status) == 0:
                print("saving now")
                self.ssh_client.ssh_exec_cmd(save_rm_cmd)
                break


def docker_test(file_name, ip, port, password, gpu_user, gpu_num, student_id):
    clinet = SSHManager(ip, port, gpu_user, password)
    api = DockerApi(clinet, student_id)
    api.run_container(gpu_num, 'tensorflow/tensorflow:latest-gpu', file_name)
    # 释放占用的gpu
    free_gpu_list.append(gpu)

# gpu列表
num = 1
free_gpu_list = []
for i in range(num):
    free_gpu_list.append(i)
gpu = None

file_name = '11.py'
ip = '116.85.38.198'
port = 22
gpu_user = 'dc2-user'
password = 'Hx1021$&@'
stu = '1111'

# 获取空闲的gpu
if free_gpu_list:
    gpu = free_gpu_list.pop(0)
    print(gpu)
    docker_test(file_name, ip, port, password, gpu_user, gpu, stu)
else:
    print('暂无空闲gpu')

