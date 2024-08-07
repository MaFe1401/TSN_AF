import paramiko

from serverBase import ServerBase
from serverInterface import SshServerInterface
from shell import Shell

class SshServer(ServerBase):
    
    def __init__(self, host_key_file, host_key_file_password=None):
        super(SshServer, self).__init__()
        self._host_key = paramiko.RSAKey.from_private_key_file(host_key_file, host_key_file_password)
    
    def connection_function(self, client):
        try:
            # create the SSH transport object
            session = paramiko.Transport(client)
            session.add_server_key(self._host_key)

            # create the server
            server = SshServerInterface()
            
            # start the SSH server
            try:
                session.start_server(server=server)
            except paramiko.SSHException:
                return

            # create the channel and get the stdio
            channel = session.accept()
            stdio = channel.makefile('rwU')

            # create the client shell and start it
            # cmdloop() will block execution of this thread.
            self.client_shell = Shell(stdio, stdio)
            print("ENTERING THE LOOP")
            self.client_shell.cmdloop()
            print("EXITING LOOP")
            # After execution continues, we can close the session
            # since the only way execution will continue from
            # cmdloop() is if we explicitly return True from it,
            # which we do with the bye command.
            writemessage = channel.makefile("wb")
            #writemessage.write("SOME COMMAND SUBMITTED")
            writemessage.channel.send_exit_status(0)
            print("CLOSING")
            session.close()
        except:
            print ("EXCEPT")
            pass

