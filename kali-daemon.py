#!/usr/bin/env python

import threading
import Queue
import paramiko

# need a method to keep track of open ssh connections by server name
# need a method to lock access to an open ssh connection.  DETERMINE IF MULTIPLE COMMANDS CAN SIMULTANEOUSLY BE ISSUED.
# need to run house keeping to ensure ssh connections stay active
# we need to use threading and threading queue so that if a human wants to issue a command to 1000 servers... we can satisfy all requests at once.
# threading queue will contain servernames
# during housekeeping... if a server is declared dead... it will be removed from the global tracker
# enure timeouts are used when attempting a new connection or issuing commands


servers = [
    '10.0.2.15',
    '10.0.2.15',
    '10.0.2.15',
    '10.0.2.15',
    '10.0.2.15',
    '10.0.2.15',
    '10.0.2.15',
    '10.0.2.15',
    '10.0.2.15',
]

outlock = threading.Lock()

cmd = 'grep -ih amd /tmp/zork'

def run_cmd (server, queue, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username='mhersant', password='1953Merc')
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.write('xy\n')
    stdin.flush()

    with outlock:
        queue.put(stdout.readlines())

def fetch_parallel():
    result = Queue.Queue()
    threads = []
    # Begin threads.
    for server in servers:
        t = threading.Thread(target=run_cmd, args=(server,result,cmd))
        t.start()
        threads.append(t)
    # Collect threads.
    for t in threads:
        t.join()
    return result

zork = fetch_parallel()

for epoch in zork.queue:
    print epoch

