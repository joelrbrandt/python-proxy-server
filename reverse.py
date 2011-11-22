import SocketServer
import threading
from time import sleep

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        print "Starting to handle connection..."

        try:
            while True:
                data = self.request.recv(4096)
                if len(data) == 0:
                    raise Exception("endpoint closed")
                print "Received: " + data
                self.request.send(data[::-1])
        except:
            pass


        print "..finishing handling connection"

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Reverse server loop running on port ", port
    try:
        while True:
            sleep(1)
    except:
        pass
    print "...server stopping."
    server.shutdown()
