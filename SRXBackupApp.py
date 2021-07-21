from netmiko import ConnectHandler
from netmiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException
import os
import os.path
import re
import getpass
import time
import sys


print("-"*80)
cmd_file = input("Enter path for operational mode commands : ")

if os.path.isfile(cmd_file) is True:
        with open(cmd_file, 'r') as f:
            cmd = f.readlines()
else:
    print("\nOops....Invalid path input....Please try again!")
    sys.exit()

print("-"*80)
ip_list = []
ip_file = input("\nEnter path for ip addresses : ")
with open(ip_file,'r') as f:
	r = f.readlines()
	for i in r:
		ip_list.append(i.strip('n'))


print("-"*80)
username = input("Enter your username : ")
pswd = getpass.getpass("And your password : ")



    
def ssh_connect(ip, username, pswd):

        try:
                
                device = {
                          'ip':ip, 
                          'username':username,
                          'password':pswd,
                          'device_type':'juniper'
                         }
                #Establishing connection
                connection = ConnectHandler(**device)
                #Getting into enable mode
                connection.enable()
                # Getting device hostname
                host = connection.find_prompt()
                gethost = re.split('@',host)
                hname = gethost[2].strip('>')
                filename = hname+'.txt'
                for each_cmd in cmd:
                        print("Reading output of '{}'".format(each_cmd.strip('\n').strip()))
                        output = connection.send_command(each_cmd.strip('\n').strip())
                        with open(filename,'a') as f:
                                f.write(each_cmd.strip('\n').strip())
                                f.write('\n')
                                f.write(output)
                                f.write('\n\n\n\n')
                        print("\nBackup completed for {}".format(hname))
                        connection.disconnect()
                        
        except (AuthenticationException):
                print("\nOops! Authentication fails    Try again....")
        except (NetMikoTimeoutException):
                print("\nSession timed out....Try again")
        except (EOFError):
                print("\nSomething else occurred....Try again")
        

#Starting couting secs
start = time.time()

for ip in ip_list:
    print("-"*80)
    print("Getting in {}\n".format(ip))
    ssh_connect(ip, username, pswd)
    
stop = time.time()
consume = stop - start

print("-"*80)
print("Activity is completed in {} secs".format(consume))
print("-"*80)
	




