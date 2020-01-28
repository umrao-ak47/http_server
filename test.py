# testing code

from server import HTTPServer

# create and run server
try:
    s = HTTPServer()
    print("Ctrl+C to terminate....")
    s.run()
except KeyboardInterrupt:
    s.close()