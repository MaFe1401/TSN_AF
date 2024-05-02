from sshServerConn import SshServer
import subprocess
if __name__ == '__main__':
    subprocess.call(["ssh-keygen", "-t rsa", "-b 2048", "-m PEM", "-f rsa"])
    server = SshServer('rsa')
    server.start()