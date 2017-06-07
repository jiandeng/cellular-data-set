import os, time, socket, struct, signal, sys
from threading import Thread
from SocketServer import TCPServer, BaseRequestHandler, ThreadingMixIn, ForkingMixIn, StreamRequestHandler

class Watcher():
    def __init__(self):
        self.child = os.fork()
        if self.child == 0:
            return
        else:
            self.watch()

    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError:
            pass

class Server(ThreadingMixIn, TCPServer):
    pass

class Handler(StreamRequestHandler):
    def handle(self):
        #addr = self.request.getpeername()
        #print 'connected from ', addr
        while True:
            data = None
            try:
                data = self.rfile.readline()
            except:
                pass
            if data is None or data == '':
                break

            if not data.startswith('AAAAAAAA'):
                d = time.strftime('%Y-%m-%dT%H:%M:%S -->> ', time.localtime()) + data
                print d
                f = open(file, 'a')
                f.write(d)
                f.close()

            if data is not None and data != '':
                err = False
                try:
                    self.wfile.write(data)
                except:
                    err = True
                if err:
                    break

Watcher()
file = time.strftime('CT-%Y%m%dT%H%M%S.txt')
server = Server(('', 9528), Handler)
server.allow_reuse_address = True
server_thread = Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
print 'server running'
server_thread.join()
