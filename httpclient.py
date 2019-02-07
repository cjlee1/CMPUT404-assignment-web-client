#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust, Calvin Lee
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
import urllib
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        if not data:
            code = 400
        else:
            code = int(data.split(" ")[1])
        return code

    def get_headers(self,data):
        if not data:
            headers = ""
        else:
            headers = data.split("\r\n\r\n")[0]
        return headers

    def get_body(self, data):
        #print(data)
        if not data:
            body = ""
        else:
            body = data.split("\r\n\r\n")[1]
        #print(body)
        return body

    def sendall(self, data):
        # data = "GET / HTTP/1.1\nHost: {}\n\n".format(self.url_parse.netloc)
        self.socket.sendall(bytearray(data,'utf-8'))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        # print(url)
        try:
            if "http" in url or "https" in url:
              #  print("hi")
                self.url_parse = urllib.parse.urlparse(url)
            else:
             #   print("bye")
                url = "http://"+ url
                self.url_parse = urllib.parse.urlparse(url)

            self.path = self. url_parse.path
            if not self.path:
                self.path = "/"
            #print(self.url_parse.hostname)
            #print(self.url_parse.port)
            self.port = self.url_parse.port
            if not self.url_parse.port:
                self.port = 80

            self.connect(self.url_parse.hostname, self.port)


            request = "GET {} HTTP/1.1\r\nHost: {}\r\nAccept: */*\r\nConnection: Close\r\n\r\n".format(self.path,self.url_parse.hostname)
            self.sendall(request)
            buffer = self.recvall(self.socket)
            #   print(url_parse.netloc)s
            # print(buffer)
            # print(buffer.split("\r\n\r\n"))
            body = self.get_body(buffer)
            code = self.get_code(buffer)
        except Exception as e:
            code = 404
            body = 'HTTP/1.1 404 Page Not Found\r\n\r\n'
            print(body)
            return HTTPResponse(code,body)
        print(str(code)+"\n"+body)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        try:
            if "http" in url or "https" in url:
              #  print("hi")
                self.url_parse = urllib.parse.urlparse(url)
            else:
             #   print("bye")
                url = "http://"+ url
                self.url_parse = urllib.parse.urlparse(url)

            # self.url_parse = urllib.parse.urlparse(url)
            self.path = self. url_parse.path
            if not self.path:
                self.path = "/"
            # print(self.url_parse.hostname)
            # print(self.url_parse.port)
            self.connect(self.url_parse.hostname, self.url_parse.port)
            content_type = "application/x-www-form-urlencoded"
            if args == None:
                encode_content =""
                content_len = 0
            else:
                encode_content=""
                for key in args:
                #     print(key,args[key],20000)
                     content= "{}={}&".format(key,args[key])
                 #    print(content,11111111)
                     encode_content += content

                #print(encode_content,"be")
                encode_content = encode_content.rstrip("&")
                #print(encode_content,"FE")
                #encode_content = urllib.parse.urlencode(args)
                content_len = str(len(encode_content))
            #print("\n"+encode_content,100000000000000000000)
            #print(args)
            request = "POST {} HTTP/1.1\r\nHost: {}\r\nAccept: */*\r\nContent-Length: {}\r\nContent-Type:{}\r\nConnection: Close\r\n\r\n{}\r\n\r\n".format(self.path,self.url_parse.hostname,content_len, content_type,encode_content)
            #request = request + encode_content + "\r\n\r\n"
            #print(request,2000000000000000000000000000)
            self.sendall(request)
            buffer = self.recvall(self.socket)
            #   print(url_parse.netloc)s
            #print(buffer, 00)
            # print(buffer.split("\r\n\r\n"))
            body = self.get_body(buffer)
            code = self.get_code(buffer)
        except Exception as e:
            code = 404
            body= 'HTTP/1.1 404 Page Not Found\r\n\r\n'
            print(body)
            return HTTPResponse(code,body)
        print(str(code)+"\n"+body)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
