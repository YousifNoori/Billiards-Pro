import sys
import cgi
import os
import Physics
import math

from http.server import HTTPServer, BaseHTTPRequestHandler

from urllib.parse import urlparse, parse_qsl;

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):   
        parsed = urlparse(self.path) # takes the url and makes it a string
        if parsed.path in [ '/homePage.html' ]:
            fp = open( '.'+self.path)
            content = fp.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write( bytes(content, "utf-8"))
            fp.close()

        if parsed.path in [ '/shoot.html' ]: # checks to see if the url is directing to /shoot.html
            fp = open( '.'+self.path) # opens the shoot.html file
            content = fp.read() # reads the data in the file

            self.send_response(200) # sends 200 message
            self.send_header("Content-type", "text/html") # sends the content type
            self.send_header("Content-length", len(content)) # sends the content
            self.end_headers() # finish

            self.wfile.write( bytes(content, "utf-8")) # writes the content in bytes
            fp.close() # closes the file
        elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'): # checks if the url is a table link
            try: # trys to open the file and send the data 
                fp = open('.'+self.path) 
                content = fp.read()

                self.send_response(200)
                self.send_header("Content-type", "image/svg+xml")
                self.send_header("Content-length", len(content))
                self.end_headers()

                self.wfile.write( bytes(content, "utf-8"))
                fp.close()

            except: # cannot open file
                self.send_response( 404 ) # sends error response
                self.end_headers()
                self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );
        else: # if the url is not one of the two sends an error
            self.send_response( 404 ) # sends error response
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

    def do_POST(self): # Handles the post request
        parsed = urlparse(self.path) # parses the url to get the path

        if parsed.path in ['/display.html']:  # checks if the path is display.html        
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } ) # takes the input data and stores it in form

            
            sb_number = form.getvalue('sb_number') # these lines take the data from form and store them in variables
            sb_x = form.getvalue('sb_x')
            sb_y = form.getvalue('sb_y')
            rb_number = form.getvalue('rb_number')
            rb_x = form.getvalue('rb_x')
            rb_y = form.getvalue('rb_y')
            rb_dx = form.getvalue('rb_dx')
            rb_dy = form.getvalue('rb_dy')

            # The next 22 lines are input validiation if the input is not valid it redirects them back to shoot.html to put new data
            if sb_number is None or int(sb_number) < 1 or int(sb_number) > 15:
                self.redirect()
                return
            
            if sb_x is None or float(sb_x) > 1321.5 or float(sb_x) < 28.5: 
                self.redirect()
                return

            if sb_y is None or float(sb_y) > 2671.5 or float(sb_y) < 28.5: 
                self.redirect()
                return

            if rb_x is None or float(rb_x) > 1321.5 or float(rb_x) < 28.5: 
                self.redirect()
                return

            if rb_y is None or float(rb_y) > 2671.5 or float(rb_y) < 28.5: 
                self.redirect()
                return

            if rb_dx is None or rb_dy is None:
                self.redirect()
                return

            
            # Deletes all table-x.svg files
            for file_name in os.listdir('.'):
                if file_name.startswith('table-') and file_name.endswith('.svg'):
                    os.remove(file_name)  

            # Creates a velocity coordinate using the data from the form
            vel = Physics.Coordinate(0.0,0.0)
            vel.x = float(rb_dx)
            vel.y = float(rb_dy)

            speed = Physics.phylib.phylib_length(vel) # Calculates the speed

            # Creates a acceleration coordinate and calculates its values
            acc = Physics.Coordinate(0.0,0.0)
            acc.x = (-vel.x / speed) * Physics.DRAG
            acc.y = (-vel.y / speed) * Physics.DRAG

            table = Physics.Table() # Creates a new Table

            # Creates a position coordinate for the still balls and gives it data from the form
            sb_pos = Physics.Coordinate(0.0,0.0) 
            sb_pos.x = float(sb_x)
            sb_pos.y = float(sb_y)            

            sb_n = int(sb_number) # creates a nummber variable and casts it to int for the ball number
            sb = Physics.StillBall(sb_n, sb_pos) # Creates a new still ball object

            
            # Creates a new pos coordinate for the rolling ball
            rb_pos = Physics.Coordinate(0.0,0.0)
            rb_pos.x = float(rb_x)
            rb_pos.y = float(rb_y)

            # Takes the rolling ball number and casts it to int 
            number = int(rb_number)
            rb = Physics.RollingBall(number, rb_pos, vel, acc)

            # Populates the table with the new balls created

            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2, Physics.TABLE_LENGTH/4)
            nextBall = Physics.StillBall(8, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2, Physics.TABLE_LENGTH/4 + 230)
            nextBall = Physics.StillBall(1, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 + 90, Physics.TABLE_LENGTH/4 + 130)
            nextBall = Physics.StillBall(11, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 - 90, Physics.TABLE_LENGTH/4 + 130)
            nextBall = Physics.StillBall(5, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 + 150, Physics.TABLE_LENGTH/4)
            nextBall = Physics.StillBall(2, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 - 150, Physics.TABLE_LENGTH/4)
            nextBall = Physics.StillBall(10, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 + 90, Physics.TABLE_LENGTH/4 - 130)
            nextBall = Physics.StillBall(7, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 - 90, Physics.TABLE_LENGTH/4 - 130)
            nextBall = Physics.StillBall(14, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 + 210, Physics.TABLE_LENGTH/4 - 130)
            nextBall = Physics.StillBall(6, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 - 210, Physics.TABLE_LENGTH/4 - 130)
            nextBall = Physics.StillBall(4, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2, Physics.TABLE_LENGTH/4 - 230)
            nextBall = Physics.StillBall(13, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 + 105, Physics.TABLE_LENGTH/4 - 230)
            nextBall = Physics.StillBall(3, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 - 105, Physics.TABLE_LENGTH/4 - 230)
            nextBall = Physics.StillBall(15, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 + 270, Physics.TABLE_LENGTH/4 - 230)
            nextBall = Physics.StillBall(6, nextBallPos)
            table+=nextBall
            nextBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2 - 270, Physics.TABLE_LENGTH/4 - 230)
            nextBall = Physics.StillBall(12, nextBallPos)
            table+=nextBall

            table += rb 



            # Counter variable for svg file names, creates filename and stores the name of the file
            index = 0
            filename = "table-{}.svg".format(index) 
            fileNames = "" # Creates accumulator variable for the images to store their src tags

            with open(filename, "w") as svg_file: # Opens a svg file and writes out the html code from the table
                svg_file.write(table.svg())
                fileNames += '<img src= "{}"/>'.format(filename) # Saves the image tag
                fileNames += "  " # Spacing
                svg_file.close() # closes the file
                index += 1 # Increases the count by 1

            while table and index != 100: # While the table is populated
                
                table = table.segment() # Calls the segment function

                if table is not None: # Makes sure there is data in the table

                    filename = "table-{}.svg".format(index) # Creates a string storing the next filename
                    with open(filename, "w") as svg_file: # Opens the svg file 
                        svg_file.write(table.svg()) # Writes the html code into the file
                        fileNames += '<img src= "{}"/>'.format(filename) # Stores image tag
                        fileNames += "  " # spacing
                        svg_file.close() # closes file
                        index += 1 # INcreases count by 1


            # The next 12 lines are formating the return string which is the html code for /display.html
            returnString = "<html><head><title>Ball Information</title></head><body>"
            returnString += "<h1>Ball Information</h1>"
            returnString += "<p>Still Ball: ({}, {})</p>".format(sb_x, sb_y)
            returnString += "<p>Rolling Ball: ({}, {})</p>".format(rb_x,rb_y)
            returnString += "<p>Rolling Ball Velocity: ({}, {})</p>".format(rb_dx, rb_dy)
            returnString += "<p>Rolling Ball Acceleration: ({}, {})</p>".format(acc.x, acc.y)
            returnString += "<h2>SVG Files:</h2>"
            returnString += fileNames
            returnString += "<br>"
            # Back link
            returnString += "<a href=\"/shoot.html\">Back</a>"

            returnString += "</body></html>"

            # Send the HTML response with 200 status
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(returnString))
            self.end_headers()
            self.wfile.write(bytes(returnString, "utf-8"))

                        
        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )     

    def redirect(self): # This is for input validiation reddirects user back to shoot.html to input new values
        self.send_response(303)  # 303 return message
        self.send_header('Location', '/shoot.html')
        self.end_headers()                                          

            

if __name__ == "__main__": # Creates the port
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    httpd.serve_forever()

