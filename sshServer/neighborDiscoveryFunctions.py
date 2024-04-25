import paramiko

def checkNeighborsNWTT(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='sys-admin', password='sys-admin')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo lldpcli show neighbors -f json',get_pty=True)
    ssh_stdin.write('sys-admin\n')
    ssh_stdin.flush()
    data=ssh_stdout.readlines()
    with open('neighbors/nwttNeighbors.json', 'a') as f:
        f.truncate(0)
        del data[0:2]
        for line in data:
            f.write(str(line)+'\n')
    print (data)
    return data

exec = checkNeighborsNWTT("192.168.4.52")
