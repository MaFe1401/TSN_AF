from sshServer import SshServer

if __name__ == '__main__':
    server = SshServer('rsa')
    server.start()