import socket
import select
import sys
from os import path
from request import RequestParser
from resource import ResourseManager


PORT = 9000
HOST = 'localhost'
HEADER_SIZE = 1024


class HTTPServer:
    def __init__(self):
        """
        Initialize Server directory for html pages
        """
        self.parser = RequestParser()
        file_path = path.abspath(__file__)
        dir_path, _ = path.split(file_path)
        dir_ = path.join(dir_path, 'web')
        self.manager = ResourseManager(dir_)
        print(f"Using {dir_} for HTML directory", end='\n')
    
    def close(self):
        """
        Shutdown socket
        """
        print("Shutting down Server.....")
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
    
    def bind(self):
        """
        Bind socket to localhost and a port
        """
        self.socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
        try:
            self.socket.bind((HOST, PORT))
            self.socket.listen()
            print(f"Started Server at {HOST}:{PORT}")
        except Exception as e:
            print(f"Failed: Cound not start server on {HOST}:{PORT}")
            print("Error: ",e)
            self.close()
            sys.exit(1)
    
    def listen(self):
        """
        Wait for connection
        """
        read, _, _ = select.select([self.socket],[],[])
        for s in read:
            if s == self.socket:
                self.handle_client()
    
    def run(self):
        """
        Run Server
        """
        self.bind()
        while True:
            self.listen()
    
    def handle_client(self):
        """
        Handle the new client
        """
        client, _ = self.socket.accept()
        # print(f"Accepted connectiom from {addr}")
        request = client.recv(HEADER_SIZE).decode('utf-8')
        if not len(request):
            return
        # get response
        res = self.handle_request(request)
        # sending resopnse
        client.sendall(res)
        client.shutdown(socket.SHUT_WR)
    
    def handle_request(self, request):
        """
        Handle the request
        """
        # printing requested page to terminal
        _req = request.split('\r\n')[0]
        print(_req, end=" ")
        # parsing contents of request
        self.parser.parse(request)
        req = self.parser.get_request()
        # fetching data
        res = self.manager.fetch(file_name = req['path'], http_ver=req['http-ver'])
        return res

if __name__=="__main__":
    try:
        s = HTTPServer()
        print("Press Ctrl+C to terminate...")
        s.run()
    except KeyboardInterrupt:
        s.close()
        sys.exit(0)
        
        