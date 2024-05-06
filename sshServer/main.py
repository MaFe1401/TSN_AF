from sshServerConn import SshServer
import subprocess
if __name__ == '__main__':
    server = SshServer('rsa')
    server.start()