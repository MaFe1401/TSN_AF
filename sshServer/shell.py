from cmd import Cmd
from neighborDiscoveryFunctions import *
nwttIp="192.168.4.52"
dsttIp="192.168.4.51"
class Shell(Cmd):
    
    # Message to be output when cmdloop() is called.
    intro='TSN-AF SSH Shell'
    
    # Instead of using input(), this will use stdout.write() and stdin.readline(),
    # this means we can use any TextIO instead of just sys.stdin and sys.stdout.
    use_rawinput=False
    
    # The prompt property can be overridden, allowing us to use a custom 
    # string to be displayed at the beginning of each line. This will not
    # be included in any input that we get.
    prompt='TSN-AF Shell> '
    
    # Constructor that will allow us to set out own stdin and stdout.
    # If stdin or stdout is None, sys.stdin or sys.stdout will be used
    def __init__(self, stdin=None, stdout=None):
        # call the base constructor of cmd.Cmd, with our own stdin and stdout
        super(Shell, self).__init__(completekey='tab', stdin=stdin, stdout=stdout)
    
    # These are custom print() functions that will let us utilize the given stdout.
    def print(self, value):
        # make sure stdout is set and not closed
        # we could add an else which uses the default print(), but I will not
        if self.stdout and not self.stdout.closed:
            self.stdout.write(value)
            self.stdout.flush()

    def printline(self, value):
        self.print(value + '\r\n')
    
    # To create a command that is executable in our shell, we create functions
    # that are prefixed with do_ and contains the argument arg.
    # For example, if we want the command 'greet', we create do_greet().
    # If we want greet to take a name as well, we pass it as an arg.
    def do_greet(self, arg):
        if arg:
            self.printline('Hey {0}! Nice to see you, mate!'.format(arg))
        else:
            self.printline('Hello, customer!')
    
    def do_sudo(self, arg):
        if arg:
            #self.printline('looking for lldp neighbors')
            neighborsNWTT = checkNeighborsNWTT(nwttIp)
            neighborsDSTT = checkNeighborsDSTT(dsttIp)
            delete_value('PORT_1','neighbors/nwttNeighbors.json')
            updatedNWTT=delete_value('PORT_PCIe','neighbors/nwttNeighbors.json') 
            delete_value('PORT_0','neigbors/dsttNeighbors.json')
            updatedDSTT=delete_value('PORT_PCIe','neighbors/dsttNeighbors.json')
            mergedNeighbors=merge_neighbors('neighbors/dsttNeighbors.json','neighbors/nwttNeighbors.json')
            self.print(mergedNeighbors)
            #print (neighborsNWTT)
            #print (neighborsDSTT)
            #mergeNeighbors(neighborsDSTT,neighborsNWTT)
        else:
            self.printline('Use sudo only to ask for lldp neighbors')
            
    # even if you don't use the arg parameter, it must be included.
    def do_bye(self, arg):
        self.printline('See you later!')
        # if a command returns True, the cmdloop() will stop.
        # this acts like disconnecting from the shell.
        return True
    
    # If an empty line is given as input, we just print out a newline.
    # This fixes a display issue when spamming enter.
    def emptyline(self):
        self.print('\r\n')
        