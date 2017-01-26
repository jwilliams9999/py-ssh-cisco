#!/usr/bin/python

#Importing modules
import paramiko
import sys
import time

print "Usage: Create 2 files called hosts and commands in the directory of the Python script."
print "Put each host IP or Hostname one per line."
print "Put each command you want to run one per line."
#setting parameters like host IP, username, passwd and number of iterations to gather cmds
with open('hosts', 'r') as myfile:
    host=myfile.read().splitlines()

USER = raw_input("Enter your username: ")
PASS = raw_input("Enter your password: ")
ITERATION = 1

#A function that set the term length to 0, so not paging. 
def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

#A function that logins and execute commands
def fn(hostn):
  client1=paramiko.SSHClient()
  #Add missing client key
  client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #connect to switch
  client1.connect(hostn,username=USER,password=PASS,allow_agent=False,look_for_keys=False)
  print "SSH connection to %s established" %hostn
  #invoke interactive shell
  remote_conn = client1.invoke_shell()
  #strip prompt
  output = remote_conn.recv(1000)
  print output
  #set term len 0
  disable_paging(remote_conn)
  with open('commands', 'r') as myfile:
    commands=myfile.readlines()
  for each in commands:
    remote_conn.send(each)
    time.sleep(2)
    output = remote_conn.recv(5000)
    print output
  #remote_conn.close()    
  client1.close()
  print "Logged out of device %s" %hostn


#for loop to call hosts for SSH 
for x in host:
  fn(x)
  time.sleep(5) #sleep for 5 seconds
