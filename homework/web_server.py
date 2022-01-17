# create a web server to keep a list of books
# when we call POST we can add a book to the list, we specify the name & how many pages it has
# when we call DELETE we just specify the name & remove the book from the list
# we can record our reading progress, how many pages we read, we use PUT and specify the name of the book and
# how many pages we read since our last input (we need to keep a value of pages_read and add to it the new number)
# GET returns a list of the book names & the percentage of how much we read

from http.server import HTTPServer, BaseHTTPRequestHandler
import json  # dumps & loads


#define how to handle the request
class Handler(BaseHTTPRequestHandler):
    books = {}  # initialize the list of books, empty list

    def do_POST(self):
        # first, read the input
        new_book = self.read_input()
        # validate the input
        if new_book["name"] in self.books.keys():
            self.send_response(409, message="The book already exists!")
        else:
            self.books[new_book["name"]] = new_book
            self.books[new_book["name"]]["pages_read"] = 0
            self.send_response(200, message="We added the book to your library")
        self.add_headers()

    def do_DELETE(self):
        a_book = self.read_input()
        if a_book["name"] in self.books.keys():
            self.books.pop(a_book["name"])
        self.send_response(200, message="We remove the book")
        self.add_headers()

    def do_PUT(self):
        a_book = self.read_input()
        name = a_book["name"]
        if name in self.books.keys():
            self.books[name]["pages_read"] += a_book["pages"]
            self.send_response(200, message="We added the read pages!")
        else:
            self.send_response(404, message="The book was not added to inventory!")
        self.add_headers()

    def do_GET(self):
        # write the code of the response
        self.send_response(200)
        # write the headers
        self.add_headers()
        # write the body
        d_json = json.dumps(self.books)
        self.wfile.write(bytes(d_json, encoding="ISO-8859-1"))

    def read_input(self):
        length = self.headers['Content-Length']
        input = self.rfile.read(int(length)).decode(encoding="utf8")
        return json.loads(input)

    def add_headers(self):
        self.send_response(200, message="We added the book to your library")
        self.end_headers()

# tell python what to execute
if __name__ == "__main__":
    # ip is like the building address, the port is the apartment
    hostname_and_port = ("127.0.0.1", 7776)
    web_server = HTTPServer(hostname_and_port, Handler)
    web_server.serve_forever()
