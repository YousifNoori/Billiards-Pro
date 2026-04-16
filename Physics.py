HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";

FRAME_RATE = 0.01


import phylib;
import os
import sqlite3


################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS

BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER

HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS

TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH

TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH

SIM_RATE = phylib.PHYLIB_SIM_RATE

VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON

DRAG = phylib.PHYLIB_DRAG

MAX_TIME = phylib.PHYLIB_MAX_TIME

MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS







# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    def svg(self):
        # Creates and returns svg content
        color = BALL_COLOURS[self.obj.still_ball.number]
        result = '<circle cx="{}" cy="{}" r="{}" fill="{}" />\n'.format(self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, color)
        return result


################################################################################

class RollingBall( phylib.phylib_object ):

    def __init__ ( self, number, pos, vel, acc):
        # Creates a new rolling ball object
        phylib.phylib_object.__init__( self,
                                       phylib.PHYLIB_ROLLING_BALL,
                                       number,
                                       pos, vel, acc,
                                       0.0, 0.0);
        
        self.__class__ = RollingBall;

    def svg(self):
        # Creates and returns svg content
        color = BALL_COLOURS[self.obj.rolling_ball.number]
        result = '<circle cx="{}" cy="{}" r="{}" fill="{}" />\n'.format(self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, color)
        return result

################################################################################

class Hole( phylib.phylib_object ):

    def __init__( self, pos ):
        # Creates a new hole object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       None, 
                                       pos, None, None,
                                       0.0, 0.0);    
                                    
        self.__class__ = Hole;

    def svg(self):
        # Creates and returns svg content
        result = '<circle cx="{}" cy="{}" r="{}" fill="black" />\n'.format(self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)
        return result

################################################################################

class HCushion ( phylib.phylib_object ):

    def __init__( self, y ):
        # Creates a new hcushion object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION,
                                       None,
                                       None, None, None,
                                       0.0, y);

        self.__class__ = HCushion;

    def svg( self ):

        # Creates and returns svg content         
        if self.obj.hcushion.y == 0:
            y = -25
        else:
            y = 2700


        result = '<rect width="1400" height="25" x="-25" y="{}" fill="darkgreen" />\n'.format(y)
        return result

################################################################################

class VCushion ( phylib.phylib_object ):

    def __init__( self, x ):
        # Creates a new vcushion object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION,
                                       None,
                                       None, None, None,
                                       x, 0.0);

        self.__class__ = VCushion;

    def svg(self):
        # Creates and returns svg content
        if self.obj.vcushion.x == 0:
            x = -25
        else:
            x = 1350
        result = '<rect width="25" height="2750" x="{}" y="-25" fill="darkgreen" />\n'.format(x)
        return result


################################################################################



class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;


    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here

    def svg(self):
        # Creates and returns svg content
        result = HEADER

        for i in self:
            if i:
                result += i.svg()

        result += FOOTER

        return result
    

    def roll( self, t ): 
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                      Coordinate( ball.obj.still_ball.pos.x,
                                                  ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
                # return table
        return new;

    def cueBall( self, xvel, yvel ):
        for ball in self:
            if(isinstance(ball, StillBall) and ball.obj.still_ball.number == 0):
                xpos = ball.obj.still_ball.pos.x
                ypos = ball.obj.still_ball.pos.y
                print(xpos, ypos)
                ball.type = phylib.PHYLIB_ROLLING_BALL
                ball.obj.rolling_ball.number = 0
                ball.obj.rolling_ball.pos.x = xpos
                ball.obj.rolling_ball.pos.y = ypos
                ball.obj.rolling_ball.vel.x = xvel
                ball.obj.rolling_ball.vel.y = yvel

                

                vel = Coordinate(xvel, yvel)

                acc = Coordinate(0.0,0.0)
                speed = phylib.phylib_length(vel)
                acc.x = (-vel.x / speed) * DRAG
                acc.y = (-vel.y / speed) * DRAG

                ball.obj.rolling_ball.acc.x = acc.x
                ball.obj.rolling_ball.acc.y = acc.y

    def replace_ball(self, index, new_ball):
        if 0 <= index < len(self.balls):
            self.balls[index] = new_ball

class Database:
    
    def __init__(self, reset=False): # Creates / Deletes / Opens a data base called phylib.db
        if reset:
            if os.path.exists('phylib.db'):
                os.remove('phylib.db')
        self.connection = sqlite3.connect('phylib.db')
        self.cursor = self.connection.cursor()

    def createDB(self): # This method creates all the tables 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ball (
                BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                BALLNO INTEGER NOT NULL,
                XPOS FLOAT NOT NULL,
                YPOS FLOAT NOT NULL,
                XVEL FLOAT,
                YVEL FLOAT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TTable (
                TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                TIME FLOAT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BallTable (
                BALLID INTEGER NOT NULL,
                TABLEID INTEGER NOT NULL,
                FOREIGN KEY(BALLID) REFERENCES Ball(BALLID),
                FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Shot (
                SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                PLAYERID INTEGER NOT NULL,
                GAMEID INTEGER NOT NULL,
                FOREIGN KEY(PLAYERID) REFERENCES Player(PLAYERID),
                FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TableShot (
                TABLEID INTEGER NOT NULL,
                SHOTID INTEGER NOT NULL,
                FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID),
                FOREIGN KEY(SHOTID) REFERENCES Shot(SHOTID)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Game (
                GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMENAME VARCHAR(64) NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Player (
                PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMEID INTEGER NOT NULL,
                PLAYERNAME VARCHAR(64) NOT NULL,
                FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID)
            )
        ''')

        self.connection.commit()
    
    def readTable (self, tableID): # Reads the table with the given tableID

        self.cursor.execute("""
            SELECT Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
            FROM Ball
            JOIN BallTable ON Ball.BALLID = BallTable.BALLID
            WHERE BallTable.TABLEID = ?
        """, (tableID + 1,)) # Selects data to be retrivied 

        rows = self.cursor.fetchall() # Stores the data into rows

        if not rows: # Insures that data retrival was successful
            return None
        
        table = Table() # Creates a new table

        for row in rows: # Goes through the data and populates the table with balls
            ballNum, xPos, yPos, xVel, yVel = row
            pos = Coordinate(xPos, yPos)
            vel = Coordinate(0.0, 0.0)
            if xVel is not None:
                vel.x = xVel
            if yVel is not None:
                vel.y = yVel

            if xVel is None and yVel is None:
                ball = StillBall(ballNum, pos)
            else:
                acc = Coordinate(0.0,0.0)
                speed = phylib.phylib_length(vel)
                acc.x = (-vel.x / speed) * DRAG
                acc.y = (-vel.y / speed) * DRAG
                ball = RollingBall(ballNum, pos, vel, acc)
            
            table += ball

        self.cursor.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (tableID + 1,)) # Retrives the time from the table
        time = self.cursor.fetchone()

        if time: # Insures that time retrival was successful
            table.time = time[0] # sets the table time
        self.connection.commit() # commits changes
 
        return table # Returns the retrived table
 
    def writeTable (self, table): # Wrtite table method

        self.cursor.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,)) # Writes the time
        tableID = self.cursor.lastrowid # Takes the next tableID
            
        for ball in table: # Goes through objects inside the table
            if isinstance(ball,StillBall): # Checks if its a still ball if so it writes the balls attributes to the table
                self.cursor.execute("""
                    INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES (?, ?, ?, ?, ?)
                """,(ball.obj.still_ball.number,ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y, None, None))
                ballID = self.cursor.lastrowid
                self.cursor.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ballID, tableID))


            elif isinstance(ball, RollingBall): # Checks if its a rolling ball if so it writes the balls attributes to the table
                self.cursor.execute("""
                    INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES (?, ?, ?, ?, ?)
                """, (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))

                ballID = self.cursor.lastrowid
                self.cursor.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ballID, tableID))

        self.connection.commit() # Commits changes

        return (tableID - 1) # Returns the tableID - 1

    def close( self ): # Closes the connection
        self.connection.commit()
        self.connection.close()

    def getGame( self, gameID ):
        self.cursor.execute("""
            SELECT Player.PLAYERNAME
            FROM Player
            JOIN Game ON Player.GAMEID = Game.GAMEID
            WHERE Game.GAMEID = ?
        """, (gameID + 1,))

        rows = self.cursor.fetchall()




        i = 0
        data = [None, None, None]

        for row in rows:
            data[i] = row[0]
            print(data[i])
            i = i + 1



        self.cursor.execute("SELECT GAMENAME FROM Game WHERE GAMEID = ?", (gameID + 1,)) # Retrives the time from the table
        gameName = self.cursor.fetchone()
        data[2] = gameName[0]
        print(data[2])

        self.connection.commit() # commits changes

        return data
        # Take gameName, and 2 playerNames from db

        


        
    
    def setGame( self, player1Name, player2Name, gameName):

        self.cursor.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        gameID = self.cursor.lastrowid # Takes the next tableID

        self.cursor.execute("""
                        INSERT INTO Player (GAMEID, PLAYERNAME)
                        VALUES (?, ?)
                    """, (gameID, player1Name))

        self.cursor.execute("""
                        INSERT INTO Player (GAMEID, PLAYERNAME)
                        VALUES (?, ?)
                    """, (gameID, player2Name))
        
        self.connection.commit()

    def newShot( self, gameName, playerName):
        self.cursor.execute("SELECT PLAYERID FROM Player WHERE PlAYERNAME = ?", (playerName,))
        playerID = self.cursor.fetchone()
        playerID = playerID[0]
        self.cursor.execute("SELECT GAMEID FROM Player WHERE PlAYERNAME = ?", (playerName,))
        gameID = self.cursor.fetchone()
        gameID = gameID[0]

        self.cursor.execute("""
            INSERT INTO Shot (PLAYERID, GAMEID)
            VALUES (?, ?)
        """,(playerID, gameID))

        shotID = self.cursor.lastrowid


        self.connection.commit()
        return shotID

    def newTableShot(self, tableID, shotID):
        self.cursor.execute("""INSERT INTO TableShot (TABLEID, SHOTID)
                               VALUES (?, ?)
                            """,(tableID,shotID))
        self.connection.commit()








       


class Game:

    def __init__ ( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):
        
        if gameID is not None and gameName is None and player1Name is None and player2Name is None:
            db = Database( reset=False)
            gameData = db.getGame(gameID)
        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
            db = Database()
            db.createDB()

            gameID = db.setGame(player1Name, player2Name, gameName)
        else:
            raise TypeError("Invalid combination of arguments provided to Game constructor")

    def shoot( self, gameName, playerName, table, xvel, yvel ):
        db = Database( reset=False)
        shotID = db.newShot( gameName, playerName)
        print(shotID)   

        table.cueBall(xvel, yvel)

        initialTime = table.time
        
        tableCopy = table

        while table:
            newTime = table.time
            table = table.segment()
            print(table)

        segmentLength = int((newTime - initialTime) / FRAME_RATE)

        print(segmentLength)

        for i in range(segmentLength):
            nextFrame = initialTime + i * FRAME_RATE
            newTable = tableCopy.roll(nextFrame)
            newTable.time = nextFrame
            #print(newTable) 
            tableID = db.writeTable(newTable)
            db.newTableShot(tableID, shotID)







        



        


            



        



    
                




