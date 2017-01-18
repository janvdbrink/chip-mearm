try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

from os import getcwd, sep
import cgi
from threading import Thread, Event
from time import sleep
from Servo import ServoSG90

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def log_message(self, format, *args):
        pass
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        if self.path=="/":
            self.path="/template.html"

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(getcwd() + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        """Respond to a POST request."""
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST"}
        )

        #print("POST request: {}".format(str(form)))
        
        for item in form.list:
            if item.value == 'end':
                self.server.thread[item.name].stop()
            else:
                self.server.thread[item.name].rotate(item.value)

        if self.path=="/":
            self.path="/template.html"

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(getcwd() + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: {}'.format(self.path))

class ServoServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, thread = {}):
        HTTPServer.__init__(self,  server_address, RequestHandlerClass)
        self.thread = thread

class ServoThread(Thread):
    MIN_DEGREE = 0
    MAX_DEGREE = 180

    def __init__(self, name=None):
        Thread.__init__(self, name=name)
        self.daemon = True
        self.event = Event()
        self.degree = 90
        self.direction = None
        self.servo = ServoSG90()
        self.channel = {'left':0, 'right':1, 'middle':2, 'claw':3}
        self.name = name
        
        self.servo.set_pwm_freq(60)
        self.servo.set_degree(self.channel[name], 90)

    def run(self):
        print("thread {} started".format(self.name))
        while True:
            if not self.event.is_set():
                self.event.wait() #block until notified

            try:
                #print("Received event {}, {} degrees".format(self.direction, self.degree))
                if self.direction == 'dir:up':
                    self.degree = int(self.degree) + 6
                    if self.degree > self.MAX_DEGREE:
                        self.degree = self.MAX_DEGREE
                elif self.direction == 'dir:down':
                    self.degree = int(self.degree) - 6
                    if self.degree < self.MIN_DEGREE:
                        self.degree = self.MIN_DEGREE
                elif 0 <= int(self.direction) <= 180:
                    self.degree = int(self.direction)
                    self.event.clear()
            except ValueError:
                pass


            self.servo.set_degree(self.channel[self.name], int(self.degree))
            sleep(0.5)
            print('Running thread {}, {} degrees'.format(self.name, self.degree))

    def rotate(self, direction):
        self.direction = direction
        self.event.set() #unblock self if waiting

    def stop(self):
        self.event.clear() #make self block and wait


if __name__ == '__main__':
    print("listening on port 8080")
    try:
        threads = {}
        servos = ('left', 'right', 'middle', 'claw')

        for servo in servos:
            t = ServoThread(name=servo)
            t.start()
            threads[servo] = t

        server = ServoServer(("", 8080), RequestHandler, threads)
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.socket.close()