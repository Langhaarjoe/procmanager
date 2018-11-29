#!/usr/bin/env python3

import os
import psutil
import signal

class Command():
    def __init__(self, args):
        pass

class ListProcs(Command):
    def __init__(self, args):
        pass

    def run(self):
        proc = "/proc"
        for d in os.listdir("/proc"):
            if os.path.isdir(proc + "/" + d) and d.isdigit():
                print(d)
                
class SendSignal(Command): # added by Marius
    def __init__(self, args):
        pass

    def run(self, pid):
        os.kill(pid, signal.SIGUSR1)

class ShowStatus(Command):
	def __init__(self, args):
		if len(args) == 0:
			raise Exception("No pid passed!")
		self.ps = map(lambda pid: psutil.Process(int(pid)), args);

class ListVars(Command):
    def __init__(self, args):
        self.args = args

    def run(self):
        keys = []
        values = []
        with open("/proc/" + self.args[0] + "/environ") as f:
            vars = f.read().split('=')
            for var in vars:
                val = ''
                key = ''
                for v in var:
                    if v.isupper():
                        key += v
                    else:
                        val += v
                keys.append(key)
                if val:
                    values.append(val.strip('\x00_'))
        print(dict(zip(keys, values)))

	def run(self):
		print([p.status() for p in self.ps])

class showMem:
    def __init__(self, args):
        self.arg = args

    def run(self):
        DIR = '/proc/'
        process = self.arg[0]
        path = DIR + process + '/status'
        exst = False
        for n,line in enumerate(open(path)):
            if line[:6] == 'VmSize':
                exst = True
                print (line[10:])
        if not exst: 
                print ('No status')

class ListFiles(Command):

    def __init__(self, args):
        self.args = args
        self.description = {
                "--all, -a": "list all open files",
                "--pid, -p": "list all the files opened by a process",
                "--user, -u": "list all the files owned by a user",
                "--directory, -d": "list all the files opened in a directory, not descending",
                "--Directory, -D": "list all the files opened in a direcotry, descending"
                }
        self.commands = {
                ("--pid", "-p", 2): "lsof -p ",
                ("--all", "-a", 1): "lsof",
                ("--user", "-u", 2): "lsof -u ",
                ("--directory", "-d", 2): "lsof +d ",
                ("--Direcotiry", "-D", 2): "lsof +D "
                }

    def run(self):
        if self.args:
            for command in self.commands.keys():
                if self.args[0] in command and len(self.args) == command[2]:
                    os.system(self.commands[command])
                elif self.args[0] in command and len(self.args) == command[2]:
                    os.system(self.commands[command] + self.args[1])
        else:
            for i, x in self.description.items():
                print(f"{i}: {x}")
                  
commands = {
    "listfiles": lambda args: ListFiles(args),
    "list" : lambda args: ListProcs(args),
    "show_status": lambda args: ShowStatus(args), 
    "send_signal": lambda pid: SendSignal(pid),  # added by Marius
    "env"  : lambda args: ListVars(args),
    "memory_usage": lambda args: showMem(args)
}

def get_command():
    strs = input("> ").split()
    try:
        cmd = commands[strs[0]](strs[1:])
    except KeyError as e:
        print("Unknown command")
    return cmd

while True:
    cmd = get_command()
    cmd.run()
