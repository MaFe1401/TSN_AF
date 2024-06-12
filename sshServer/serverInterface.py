import paramiko,time
import channelSingleton
class SshServerInterface(paramiko.ServerInterface):
    
    # This will allow the SSH server to provide a
    # channel for the client to communicate over.
    # By default, this will return OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED,
    # so  we have to override it to return OPEN_SUCCEEDED 
    # when the kind of channel requested is "session"
    def check_channel_request(self, kind, chanid):
        
        print("KIND IS:")
        print(kind)
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    # AFAIK, pty (pseudo-tty (TeleTYpewriter)) will allow our
    # client to interact with our shell.
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    # This allows us to provide the channel with a shell we can connect to it.
    def check_channel_shell_request(self, channel):
        writemessage = channel.makefile("wb")
        #writemessage.write("SOME COMMAND SUBMITTED")
        writemessage.channel.send_exit_status(0)
        #time.sleep(2)
        #channel.close()
        return True
    
    def check_channel_exec_request(self, channel, command):
        try:
            command = command.decode()
        except:
            pass
        #print(time.time())
        #writemessage = channel.makefile("wb")
        print(command)
        #print(command.decode())
        
        #writemessage.write("SOME COMMAND SUBMITTED")
        #writemessage.channel.send_exit_status(0)
        #time.sleep(3)
        #channel.close()
        #return True
    # This let's us setup password authentication.
    # There are better ways to do this than using plain text.
    # For posterity, you could setup a database that encrypts
    # passwords and will grab them to decrypt here.
    def check_auth_password(self, username, password):
        if (username == "sys-admin") and (password == "sys-admin"):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
    # String that will display when a client connects,
    # before authentication has happened. This is different
    # than the shell's intro property, which is displayed 
    # after the authentication.
    def get_banner(self):
        return ('TSN AF SSH Server\r\n', 'en-US')