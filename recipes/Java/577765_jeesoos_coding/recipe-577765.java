import java.awt.*;
import java.awt.event.*;

import javax.swing.*;
import javax.swing.Timer;



public class Game extends JApplet // swing applet
{
    /////// SCREENS

    boolean titleScreen = true; // implements the menu screen when true
    boolean gameBegin = false; // Begins the game screen when true
    boolean instruction = false; // Begins the game screen when true

    /////// IMAGE

    Dimension dim; // buffering
    Image offscreen; // buffering
    static Graphics bufferGraphics; // buffering

    static Image h1, h2; // Cursor image
    static Image bg, button1a, button1b, button2a, button2b; // image for menu screen (background, buttons)
    static Image instrbg; // instruction background
    static Image gamebg, m1, m1a, m1b; // image for game screen (background, monkey sprite)
    static Image[] mk = new Image [9]; // image variable for the 9 "moles"

    /////// MOUSE

    Cursor c; // cursor variable
    boolean myButtonPressed = false; // mouse button pressed (true or false)
    boolean myButtonEntered = false; // mouse enter the screen (true or false)
    int myMouseX = 0, myMouseY = 0; // mouse coordinates x and y from top left
    int myRow = -1, myCol = -1; // mouse coordinate outside of the screen

    /////// GAME VARIABLES

    private static final int[] mX = {5, 170, 335, 5, 170, 335, 5, 170, 335}; // "mole" (monkey) x coordinates on the game screen
    // grid format going from left to right & down the rows
    private static final int[] mY = {5, 5, 5, 170, 170, 170, 335, 335, 335}; // "mole" y coordinates on the game screen
    // grid format going from left to right & down the rows
    int randm; // randomizes which "mole" will activate
    int rand; // randomizes the time space between the mole activation/deactivation

    static boolean mup = false; // a "mole" is activated (true/false)
    static boolean[] mhit = {false, false, false, false, false, false, false, false, false}; // monkey (1 to nine in same grid format as above) hit

    private int[] respawnCounter = {0, 0, 0, 0, 0, 0, 0, 0, 0};
    private int[] removeCounter = {0, 0, 0, 0, 0, 0, 0, 0, 0};

    static int score = 0; // score counter

    /////// IPLEMENTING CLASSES

    GameScreen g1 = new GameScreen (); // instantiates the GameScreen Class
    Timer repaintM = null; // sets the repaint timer for monkey

    public void init ()  // instantiating variables
    {
        /////// Screen variables
        setSize (600, 500); // sets screensize to 600 by 500 pixels

        /////// Buffering variables
        dim = getSize (); // gets the dimension of the screen
        setBackground (Color.white); // sets the background of screen to white
        offscreen = createImage (dim.width, dim.height); // buffering method to the applet screen
        bufferGraphics = offscreen.getGraphics (); // new object for instantiating images on the paint()

        /////// Receiving images
        m1a = getImage (getCodeBase (), "m1a.gif"); // monkey up image
        m1b = getImage (getCodeBase (), "m1b.gif"); // monkey hit image
        m1 = getImage (getCodeBase (), "m1.gif"); // monkey none image

        h1 = getImage (getCodeBase (), "hammer.gif"); // hammer cursor
        h2 = getImage (getCodeBase (), "hammer2.gif"); // hammer hit cursor
        bg = getImage (getCodeBase (), "mainbg.gif"); // main menu background
        gamebg = getImage (getCodeBase (), "gbg.gif"); // game background
        instrbg = getImage (getCodeBase (), "instruction.gif"); // game background

        button1a = getImage (getCodeBase (), "button1a.gif"); // start button
        button1b = getImage (getCodeBase (), "button1b.gif"); // instruction button
        button2a = getImage (getCodeBase (), "button2a.gif"); // start pressed button
        button2b = getImage (getCodeBase (), "button2b.gif"); // instruction pressed button

        for (int x = 0 ; x < 9 ; x++) // loops 9 times for each monkey image array
        {
            mk [x] = m1; // monkey [x] is equal to "monkey none image"
        }

        /////// MOUSE
        Toolkit tk = Toolkit.getDefaultToolkit ();
        c = tk.createCustomCursor (tk.getImage (""), new Point (0, 0), "invisible"); // creates an invalid cursor thus appears like there is no cursor
        setCursor (c); // activates the cursor

        addMouseListener (new MyMouseListener ()); // adds mouse listener class which moniters the status of the mouse button
        addMouseMotionListener (new MyMouseMotionListener ());  // adds mouse motion listener class which moniters the movement of the mouse

    } // end init method



    /////////////////////////////////////
    /////// MOUSELISTENER CLASS /////////
    /////////////////////////////////////

    public class MyMouseListener implements MouseListener // Mouse Listener Class: "status of mouse button"
    {
        public void mousePressed (MouseEvent me)  // mouse pressed method
        {
            myButtonPressed = true; // mouse pressed becomes true (mouse pressed)
            myMouseX = me.getX (); // returns x coordinate of mouse
            myMouseY = me.getY (); // returns y coordinate of mouse
            handleMouseEvents (); // values are implemented into the handleMouseEvents ()
        }

        public void mouseReleased (MouseEvent me)  // mouse released method
        {
            myButtonPressed = false; // mouse pressed becomes false (mouse released)
            myMouseX = me.getX (); // returns x coordinate of mouse
            myMouseY = me.getY (); // returns y coordinate of mouse
            handleMouseEvents (); // values are implemented into the handleMouseEvents ()
        }

        public void mouseEntered (MouseEvent me)  // mouse entered method
        {
            myButtonEntered = true; // mouse enters the screen becomes true
            myMouseX = me.getX (); // returns x coordinate of mouse
            myMouseY = me.getY (); // returns y coordinate of mouse
            handleMouseEvents (); // values are implemented into the handleMouseEvents ()
        }

        public void mouseExited (MouseEvent me)  // mouse excited method
        {
            myButtonEntered = false; // mouse pressed becomes true
            myMouseX = me.getX (); // returns x coordinate of mouse
            myMouseY = me.getY (); // returns y coordinate of mouse
            handleMouseEvents (); // values are implemented into the handleMouseEvents ()
        }

        public void mouseClicked (MouseEvent me)  // mouse clicked method
        {
            // must access all the methods in an interface
        }
    } // end MyMouseListener class


    public class MyMouseMotionListener implements MouseMotionListener // Mouse Motion Listener class: "movement of mouse"
    {
        public void mouseMoved (MouseEvent me)  // mouse moved class
        {
            myMouseX = me.getX (); // returns x coordinate of mouse
            myMouseY = me.getY (); // returns y coordinate of mouse
            handleMouseEvents (); // values are implemented into the handleMouseEvents ()
        } // end mouseMoved method

        public void mouseDragged (MouseEvent me)  // mouse dragged class (pressed and moved simultaneously)
        {
            myMouseX = me.getX (); // returns x coordinate of mouse
            myMouseY = me.getY (); // returns y coordinate of mouse
            handleMouseEvents (); // values are implemented into the handleMouseEvents ()
        } // end mouseDragged method
    } // end MyMouseListener class


    public Image getMouseImage ()  // method that returns mouse image
    {
        if (myButtonPressed) // when mouse button is pressed
        {
            return h2; // cursor changes to hammer hit image
        }
        return h1; // cursor returns to original hammer image
    }


    public void handleMouseEvents ()  // the coordinates of the mouse on screen
    {
        int nCol = myMouseX - 50; // variable for x coordinate of mouse
        // variable is subtracted to place the x coordinate of the cursor in the center of the hammer image (size = 100 by 100)
        int nRow = myMouseY - 50; // variable for y coordinate of mouse
        // variable is subtracted to place the x coordinate of the cursor in the center of the hammer image (size = 100 by 100)

        if (!myButtonEntered) // if mouse has not entered the screen
            nCol = nRow = -1; // the coordinates of the mouse is out of bounds
        if (nCol != myCol || nRow != myRow) // if the mouse has entered the screen
        {
            myRow = nRow; // cursor x coordinate
            myCol = nCol; // cursor y coordinate
        }
        repaint (); // repaints the cursor as coordinates of the mouse moves
    } // end handleMouseEvents method


    public void mouse ()  // draws hammer cursor
    {
        if (myRow != -1 && myCol != -1) // if mouse is in the boundaries of the screen
        {
            Image mouseImage = getMouseImage (); // mouse image is rendered depending on the situation
            // see getMouseImage ()
            bufferGraphics.drawImage (mouseImage, myCol, myRow, 100, 100, null, this); // draws the cursor
        } // end if
    }


    public void paint (Graphics g)  // paint method - handles images
    {
        // buffering tool
        bufferGraphics.clearRect (0, 0, dim.width, dim.height);

        if (titleScreen == true) // if screen title is true
        {
            mainScreen (); // main screen appears
        }
        if (gameBegin == true) // if game begin is true
        {
            repaint ();
            game (); // game screen appears
        }
        if (instruction == true) // if game begin is true
        {
            instruction (); // game screen appears
        }
        mouse (); // mouse hammer cursor is repeatedly drawn

        // buffering tool
        g.drawImage (offscreen, 0, 0, this);
    } // end Paint method


    public void update (Graphics g)  // double buffering method
    {
        paint (g);
    }


    public void instruction ()
    {
        /////// IMAGE
        bufferGraphics.drawImage (instrbg, 0, 0, 600, 500, Color.red, this); // background
        if (myButtonPressed && myRow > (384 - 50) && myRow < (433 - 50)
                && myCol > (427 - 50) && myCol < (586 - 50)) // if mouse button is pressed and hits start button coordinates
        {
            instruction = false; // instruction screen closes
            gameBegin = true; // game begins
        }
    }


    public void mainScreen ()  // main screen method
    {
        /////// IMAGE
        bufferGraphics.drawImage (bg, 0, 0, 600, 500, Color.red, this); // background
        bufferGraphics.drawImage (button1a, 427, 384, 159, 49, Color.red, this); // start button
        bufferGraphics.drawImage (button2a, 427, 440, 159, 49, Color.red, this); // instruction button

        if (myButtonPressed == true) // if mouse button is pressed
        {
            if (myRow > (384 - 50) && myRow < (433 - 50)
                    && myCol > (427 - 50) && myCol < (586 - 50)) // and hits start button coordinates
            {
                titleScreen = false; // title screen closes
                gameBegin = true; // game begins
            }
            else if (myRow > (340 - 50) && myRow < (489 - 50)
                    && myCol > (427 - 50) && myCol < (586 - 50)) // and hits instruction button coordinates
            {
                titleScreen = false; // title screen closes
                instruction = true;
            }
        }
    }


    public void game ()  // Game method
    {
        // new ReminderBeep (5);

        Monkey m = new Monkey (); // randomizing which monkey becomes activated
        m.randmonkey ();

        /////// IMAGE
        bufferGraphics.drawImage (gamebg, 0, 0, 600, 500, Color.red, this); // game background
        for (int i = 0 ; i < 9 ; i++) // 9 arrays of monkey image
        {
            bufferGraphics.drawImage (mk [i], mX [i], mY [i], 160, 160, Color.red, this);
            // draws the monkey arrays in order from left to right in grid format
        }


        bufferGraphics.setFont (new Font ("Arial", Font.BOLD, 20));
        bufferGraphics.drawString (String.valueOf (score), 560, 160); // score
    }


    class Monkey extends JApplet
    {
        public void monkeyhit ()  // monkey collision detector method
        {
            if (myButtonPressed == true) // if mouse button is pressed and...
            {
                for (int hit = 0 ; hit < 9 ; hit++) // for 9 arrays of monkey image
                    if (mk [hit] == m1a && myRow > (mY [hit] - 50) && myRow < (mY [hit] + 160 - 50)
                            && myCol > (mX [hit] - 50) && myCol < (mX [hit] + 160 - 50))
                        // ... button is in the boundaries of monkey that is activated
                        {
                            mk [hit] = m1b; // monkey image changes to monkey hit image
                            mhit [hit] = false; // monkey that is hit is no longer activated
                            score += 10; // score counts up 10 pts.
                        }
            }
        }


        public void randmonkey ()  // randomizaing monkey activation method
        {
            repaintM = new Timer (2000, new RepaintAction (this)); // creates a new timer that will delay the repaint of the monkeys (2 seconds
            rand = ((int) (Math.random () * 100)) + 1000; // monkey activation delay in between
            randm = ((int) (Math.random () * 500)); // randomizes the number from 1 to 500 to determine which monkey becomes activated
            // 9 out of 500 chance of monkey appearing

            if (randm <= 8) // if random number is between 0 to 8
            {
                for (int a = 0 ; a < 9 ; a++) // for 9 monkey arrays
                {
                    if (randm == a) // if random number matches up with the corect monkey coordinates
                    {
                        mhit [randm] = true; // activates the monkey
                        mk [randm] = m1a; // monkey none image changes to monkey image
                    }
                    else if (randm != a) // if random number does not match up
                    {
                        mhit [a] = false; // monkey stays deactivated
                        mk [a] = m1; // monkey none stays monkey none
                    }
                }

                for (int i = 0 ; i < rand * 100 ; i++) // monkey is activated for a certain time of delay
                {
                    monkeyhit (); // monkey hit method is activated for player to hit the "mole"
                    if (mhit [randm] = false) // when monkey deactivates (monkey is hit)
                    {
                        mk [randm] = m1; // monkey hit image is changed to money none image
                        break; // the loop discontinues
                    }
                }
            }
        }
    }


    class RepaintAction implements ActionListener // Repaint method
    {
        Monkey randmonkey;

        public RepaintAction (Monkey randmonkey)
        {
            this.randmonkey = randmonkey; // random monkey is equal to random monkey here
        }


        public void actionPerformed (ActionEvent e)
        {
            randmonkey.repaint (); // repaints randmonkey method
        }
    }
}
