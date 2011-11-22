import socket
import SocketServer
import threading
from time import sleep

class Forwarder(threading.Thread):
    def __init__(self, source):
        threading.Thread.__init__(self)
        self.source = source
        self.dest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dest.connect(("smtp.gmail.com", 587))

    def run(self):
        print "starting forwarder... " 

        try:
            while True:
                data = self.dest.recv(4096)
                if len(data) == 0:
                    raise Exception("endpoint closed")
                print "Received from dest: " + str(len(data))
                self.source.write_to_source(data)
        except Exception, e:
            print "EXCEPTION reading from forwarding socket"
            print e

        self.source.stop_forwarding()
        print "...ending forwarder."
        
    def write_to_dest(self, data):
        print "Sending to dest: " + str(len(data))
        self.dest.send(data)

    def stop_forwarding(self):
        print "...closing forwarding socket"
        self.dest.close()

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        print "Starting to handle connection..."

        f = Forwarder(self)
        f.start()

        try:
            while True:
                data = self.request.recv(4096)
                if len(data) == 0:
                    raise Exception("endpoint closed")
                print "Received from source: " + str(len(data))
                f.write_to_dest(data)
        except Exception, e:
            print "EXCEPTION reading from main socket"
            print e

        f.stop_forwarding()
        print "...finishing handling connection"


    def write_to_source(self, data):
        print "Sending to source: " + str(len(data))
        self.request.send(data)        

    def stop_forwarding(self):
        print "...closing main socket"
        self.request.close()



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "", 8080

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running on port ", port
    try:
        while True:
            sleep(1)
    except:
        pass
    print "...server stopping."
    server.shutdown()
