#!/bin/python
from os import chmod
from Crypto.PublicKey import RSA
import sys
args = sys.argv[1:]
hosts = []
with open(args[0], 'r') as f:
    hosts = f.read().splitlines()
count = int(hosts[0])
hosts = hosts[1:]
print(hosts)
for host in hosts:
    key = RSA.generate(2048)
    fname = "/tmp/"+str(count)+'-'+host+".priv"
    with open(fname, 'wb') as content_file:
        chmod(fname, 0o600)
        content_file.write(key.exportKey('PEM'))
    pubkey = key.publickey()
    with open("/tmp/"+str(count)+"-"+host+".pub", 'wb') as content_file:
        content_file.write(pubkey.exportKey('OpenSSH'))
    count = count + 1
with open(args[0], 'w') as f:
    f.write(str(count)+"\n")
    for host in hosts:
        f.write(host+"\n")