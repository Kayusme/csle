#!/bin/bash

while [ 1 ]
do
    sleep 2
    timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1
    sleep 2
    (sleep 2; echo testpycruser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1
    sleep 2
done