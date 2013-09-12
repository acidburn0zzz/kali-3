You'll need to put the calls into separate threads (or processes, but that would be overkill) which in turn requires the code to be in a function (which is a good idea anyway: don't have substantial code at a module's top level).

For example:

import sys, os, string, threading
import paramiko

cmd = "grep -h 'king' /opt/data/horror_20100810*"

outlock = threading.Lock()

def workon(host):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='xy', password='xy')
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.write('xy\n')
    stdin.flush()

    with outlock:
        print stdout.readlines()

def main():
    hosts = ['10.10.3.10', '10.10.4.12', '10.10.2.15', ] # etc
    threads = []
    for h in hosts:
        t = threading.Thread(target=workon, args=(h,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

main()

If you had many more than five hosts, I would recommend using instead a "thread pool" architecture and a queue of work units. But, for just five, it's simpler to stick to the "dedicated thread" model (especially since there is no thread pool in the standard library, so you'd need a third party package like threadpool... or a lot of subtle custom code of your own of course;-).


I eliminated 1 machine, so I on only need 4. I forgot to mention that all data will be processed diffrently later in the script and as I can understood your code (I m PyN00b) it will print all data from all machines at once, but how can I process data just from one host then? And all the hosts have diffrent pass so can I put them all in workon()? Ty for quick replay Alex. Regards – Whit3H0rse Aug 15 '10 at 0:00
	
@konjo, you can perform the processing of the data in the thread that's just obtained the data -- I was instead printing it, only because that's what you did in your question. The processing of course can involve checks on the value of host, if you need to perform different processing for different values thereof. Or, you could write multiple functions to use as target= in your threads: there's no constraint that all threads must run the same function! – Alex Martelli Aug 15 '10 at 2:20
	
Oke i was able to grep all 4 machines, but now all data is merged. How can I extract data from to each individual host, can you give mi example, please extend example above? Regards – Whit3H0rse Aug 26 '10 at 3:37
	
Ty Alex for this, I think that you misunderstood me, I did accept you advice and example from above, but I m new at programing so I need little more hints. I did all you have written above with my modification for different cmd commands. Ty again. Regards – Whit3H0rse Aug 26 '10 at 7:25
	
@konjo, on Stack Overflow, for the asker of a question to "accept" an answer means to click on the checkmark-shaped icon to the left on the answer -- that gives the asker a few point of reputation, and the answerer more. Your "0% accepted" means you've never done that, which is baffling. – Alex Martelli Aug 26 '10 at 13:52
