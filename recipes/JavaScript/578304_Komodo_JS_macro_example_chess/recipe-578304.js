/**
 * JavaScript macro to run a chess game, showing board, pieces and moves played.
 *
 * Author: Todd Whiteman
 * Revision: 1.0
 * Date: October 2012
 */

var board = "\
       Garry Kasparov                                                                                                                          \n\
    8║♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜     Move: 0                                                                                                         \n\
    7║♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟                                                                                                                     \n\
    6║                                                                                                                                         \n\
    5║                                                                                                                                         \n\
    4║                                                                                                                                         \n\
    3║                                                                                                                                         \n\
    2║♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙                                                                                                                     \n\
    1║♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖                                                                                                                     \n\
     ╚═══════════════                                                                                                                          \n\
      a b c d e f g h                                                                                                                          \n\
        Deep Blue                                                                                                                              \n\
";


var gameintro = [
   "Site: Philadelphia, PA USA                                                                                                                 \n\
    Date: 1996.02.10                                                                                                                           \n\
    Round: 1                                                                                                                                   \n\
    White: Deep Blue                                                                                                                           \n\
    Black: Kasparov, Garry                                                                                                                     \n\
    Result: 1-0                                                                                                                                \n\
    Opening: Sicilian Defense 2.c3                                                                                                             \n\
    Annotator: Wheeler, David A.                                                                                                               \n\
    ",                                                                                                                                        

   "This game is world-famous, because it was the first game                                                                                   \n\
    won by a computer against a reigning world champion under                                                                                  \n\
    normal chess tournament conditions (in particular, normal time controls).                                                                  \n\
    ",                                                                                                                                        

   "Deep Blue was a computer developed by IBM to win against Kasparov.                                                                         \n\
    Deep Blue won this game, but Kasparov rebounded over the following 5                                                                       \n\
    games to win 3 and draw 2, soundly beating Deep Blue in the 1996 match.                                                                    \n\
    ",                                                                                                                                        

   "In the 1997 rematch, Deep Blue managed to win the entire match.                                                                            \n\
    Garry Kasparov is considered to be one of the greatest human chess players                                                                  \n\
    of all time, so both this single game and the later win of a match showed                                                                  \n\
    that computer-based chess had truly arrived at the pinnacle of chess play.                                                                 \n\
    "
];


var movelist = "\
1. e2e4 c7c5                                                                                                                                   \n\
2. c2c3                                                                                                                                        \n\
{It's more common to play 2. Nf3, but Kasparov has deep experience with                                                                        \n\
that line, so white's opening book goes in a different direction.}                                                                             \n\
                                                                                                                                               \n\
2.... d7d5                                                                                                                                     \n\
3. e4xd5 Qd8xd5                                                                                                                                \n\
4. d2d4 Ng8f6                                                                                                                                  \n\
5. Ng1f3 Bc8g4                                                                                                                                 \n\
6. Bf1e2 e7e6                                                                                                                                  \n\
7. h2h3 Bg4h5                                                                                                                                  \n\
8. e1g1h1f1 Nb8c6                                                                                                                              \n\
9. Bc1e3 c5xd4                                                                                                                                 \n\
10. c3xd4 Bf8b4                                                                                                                                \n\
{A more common move here is Be7.  This was a new approach by Kasparov,                                                                         \n\
developing the bishop in an unusual way.  Whether or not it's a good                                                                           \n\
approach is debated. After this move, the computer left its opening book                                                                       \n\
and began calculating its next move.}                                                                                                          \n\
                                                                                                                                               \n\
11. a2a3 Bb4a5                                                                                                                                 \n\
12. Nb1c3 Qd5d6                                                                                                                                \n\
13. Nc3b5 Qd6e7?!                                                                                                                              \n\
{This allows white to make its pieces more active.                                                                                             \n\
Other moves, which would probably be better, include Qb8 and Qd5.}                                                                             \n\
                                                                                                                                               \n\
14. Nf3e5! Bh5xe2                                                                                                                              \n\
15. Qd1xe2 e8g8h8f8                                                                                                                            \n\
16. Ra1c1 Ra8c8                                                                                                                                \n\
17. Be3g5                                                                                                                                      \n\
{Black now has a problem, especially with the pinned knight on f6.}                                                                            \n\
                                                                                                                                               \n\
17.... Ba5b6                                                                                                                                   \n\
18. Bg5xf6 g7xf6                                                                                                                               \n\
{Kasparov avoids ... Qxf6? because white would gain material with 19. Nd7.                                                                     \n\
Note that Kasparov's king is now far more exposed.}                                                                                            \n\
                                                                                                                                               \n\
19. Ne5c4! Rf8d8                                                                                                                               \n\
20. Nc4xb6! a7xb6                                                                                                                              \n\
21. Rf1d1 f6f5                                                                                                                                 \n\
22. Qe2e3!                                                                                                                                     \n\
{This is an excellent place for the white queen.}                                                                                              \n\
                                                                                                                                               \n\
22... Qe7f6                                                                                                                                    \n\
23. d4d5!                                                                                                                                      \n\
{Kasparov commented that he might have offered this pawn                                                                                       \n\
sacrifice himself in this position, since it hurt black's pawn                                                                                 \n\
structure, opened up the board, and black's exposed king suggested                                                                             \n\
that there was probably a way to exploit the result.                                                                                           \n\
Kasparov has been attacking the d4 pawn, and the computer wisely                                                                               \n\
decided to advance it for an attack instead of trying to defend it.}                                                                           \n\
                                                                                                                                               \n\
23... Rd8xd5                                                                                                                                   \n\
24. Rd1xd5 e6xd5                                                                                                                               \n\
25. b2b3! Kg8h8?                                                                                                                               \n\
{Kasparov attempts to prepare a counter-attack, by preparing to                                                                                \n\
move his rook to file g, but it won't work.                                                                                                    \n\
Burgess suggests that 25.... Ne7 Rxc8+ would have better, though                                                                               \n\
white would still have some advantage.                                                                                                         \n\
Indeed, after this point on it's difficult to identify                                                                                         \n\
any move that will dramatically help black.}                                                                                                   \n\
                                                                                                                                               \n\
26. Qe3xb6 Rc8g8                                                                                                                               \n\
27. Qb6c5 d5d4                                                                                                                                 \n\
28. Nb5d6 f5f4                                                                                                                                 \n\
29. Nd6xb7                                                                                                                                     \n\
{This is a very 'computerish'/materialistic move; white is grabbing                                                                            \n\
an undeveloped pawn for a small gain in material.                                                                                              \n\
However, the computer has not identified any threat of checkmate or                                                                            \n\
other risks from black, so it simply acquires the material.}                                                                                   \n\
                                                                                                                                               \n\
29.... Nc6e5                                                                                                                                   \n\
30. Qc5d5                                                                                                                                      \n\
{The move 30. Qxd4?? would be terrible, because Nf3+                                                                                           \n\
would win the white queen.}                                                                                                                    \n\
                                                                                                                                               \n\
30.... f4f3                                                                                                                                    \n\
31. g2g3 Ne5d3                                                                                                                                 \n\
{The move 31... Qf4 won't work, because of 32. Rc8! Qg5 33. Rc5!}                                                                              \n\
                                                                                                                                               \n\
32. Rc1c7 Rg8e8                                                                                                                                \n\
{Kasparov is attacking, but the computer has correctly determined that                                                                         \n\
the attack is not a real threat.}                                                                                                              \n\
                                                                                                                                               \n\
33. Nb7d6 Re8e1+                                                                                                                               \n\
34. Kg1h2 Nd3xf2                                                                                                                               \n\
35. Nd6xf7+ Kh8g7                                                                                                                              \n\
36. Nf7g5 Kg7h6                                                                                                                                \n\
37. Rc7xh7+                                                                                                                                    \n\
{Kasparov resigns - expecting ... Kg6 38. Qg8+ Kf5 Nxf3 and white's                                                                            \n\
strength is overwhelming. White will have lots of ways to defeat black,                                                                        \n\
while black has no real way to attack white.}                                                                                                  \n\
";



/******************************
 * Komodo macro contents begin.
 ******************************/

var moveDisplayTime = 2000; // milliseconds
var messageDisplayTime = 6000; // milliseconds

// Indicator values, range from 8..30 - though Komodo uses a lot of these
// numbers for special purposes.
var indicWhiteSquare = 10;
var indicBlackSquare = 11;
var indicMoveFrom = 12;
var indicMoveTo = 13;

/**
 * Highlight the black/white chess squares.
 *
 * @param {Components.interfaces.ISciMoz} scimoz - The editor control.
 */
function HighlightSquares(scimoz) {
    for (var line=1; line < 9; line++) {
        for (var col=6; col < 21; col+=2) {
            var pos = scimoz.findColumn(line, col);
            var charlength = scimoz.positionAfter(pos) - pos;
            var isBlackSquare = (line % 2) == 0 ? (col % 4) == 0 : (col % 4) == 2;
            if (isBlackSquare) {
                scimoz.indicatorCurrent = indicBlackSquare;
            } else {
                scimoz.indicatorCurrent = indicWhiteSquare;
            }
            scimoz.indicatorFillRange(pos, charlength);
        }
    }
}

/**
 * Draw the starting board layout.
 *
 * @param {Components.interfaces.ISciMoz} scimoz - The editor control.
 */
function DrawInitialBoard(scimoz) {
    // Set board styling.
    scimoz.setMarginWidthN(0, 0); // Remove the line number margin.
    scimoz.caretStyle = scimoz.CARETSTYLE_INVISIBLE; // Hide the caret
    scimoz.indicSetStyle(indicWhiteSquare, scimoz.INDIC_STRAIGHTBOX);  // See Scintilla docs for others
    scimoz.indicSetAlpha(indicWhiteSquare, 40);
    scimoz.indicSetOutlineAlpha(indicWhiteSquare, 30);
    scimoz.indicSetFore(indicWhiteSquare, 0xFFFFFF);  // Colour is BGR format!!
    scimoz.indicSetStyle(indicBlackSquare, scimoz.INDIC_STRAIGHTBOX);  // See Scintilla docs for others
    scimoz.indicSetAlpha(indicBlackSquare, 40);
    scimoz.indicSetOutlineAlpha(indicBlackSquare, 30);
    scimoz.indicSetFore(indicBlackSquare, 0x000000);  // Colour black - it's BGR format!!
    scimoz.indicSetStyle(indicMoveFrom, scimoz.INDIC_ROUNDBOX);  // See Scintilla docs for others
    scimoz.indicSetAlpha(indicMoveFrom, 40);
    scimoz.indicSetOutlineAlpha(indicMoveFrom, 90);
    scimoz.indicSetFore(indicMoveFrom, 0x00EEEE);  // Colour is BGR format!!
    scimoz.indicSetStyle(indicMoveTo, scimoz.INDIC_ROUNDBOX);  // See Scintilla docs for others
    scimoz.indicSetAlpha(indicMoveTo, 40);
    scimoz.indicSetOutlineAlpha(indicMoveTo, 90);
    scimoz.indicSetFore(indicMoveTo, 0x00EEEE);  // Colour is BGR format!!
    // Add the board text.
    scimoz.addText(ko.stringutils.bytelength(board), board);
    // Make it a large board - valid range is +-20.
    scimoz.zoom = 15;
    // Highlight the black/white squares.
    HighlightSquares(scimoz);
}

/**
 * Display the given message beside the board. Clears any previous message.
 *
 * @param {Components.interfaces.ISciMoz} scimoz - The editor control.
 * @param {String} message - The message to display.
 */
function DisplayMessage(scimoz, message, nosplit) {
    try {
        // Clear existing message lines.
        for (var line=1; line < scimoz.lineCount; line++) {
            var pos = scimoz.findColumn(line, 26);
            var eolpos = scimoz.getLineEndPosition(line);
            if (eolpos > pos) {
                scimoz.targetStart = pos;
                scimoz.targetEnd = eolpos;
                scimoz.replaceTarget(0, "");
            }
        }
        // Format the message.
        var textUtils = Components.classes["@activestate.com/koTextUtils;1"]
                            .getService(Components.interfaces.koITextUtils);
        var lines = message.split("\n");
        for (var i=0; i < lines.length; i++) {
            lines[i] = ko.stringutils.strip(lines[i]);
        }
        if (!nosplit) {
            message = lines.join(" ");
            message = textUtils.break_up_lines(message, 26);
            lines = message.split("\n");
        }
        // Display new message - limit lines to 
        for (var i=0; i < lines.length; i++) {
            var line = lines[i];
            if (i+1 >= scimoz.lineCount) {
                scimoz.currentPos = scimoz.length;
                scimoz.newLine();
            }
            var pos = scimoz.findColumn(i+1, 26);
            var lineStart = scimoz.positionFromLine(i+1);
            var lineDiff = pos - lineStart;
            while (lineDiff < 26) {
                // Add space padding to the start of the line.
                line = " " + line;
                lineDiff += 1;
            }
            scimoz.currentPos = pos;
            scimoz.addText(ko.stringutils.bytelength(line), line);
        }
    } catch(ex) {
        // Exception handling - show problems to the user.
        alert("Error: " + ex + "\n\n" + ex.stack.toString());
    }
}

/**
 * Play the introduction strings.
 *
 * @param {Components.interfaces.ISciMoz} scimoz - The editor control.
 */
function PlayIntro(scimoz, callback) {
    for (var i=0; i < gameintro.length; i++) {
        setTimeout(DisplayMessage, messageDisplayTime * i, scimoz, gameintro[i], i == 0);
    }
    setTimeout(callback, (messageDisplayTime * gameintro.length), scimoz);
}

/**
 * Highlight the chess move.
 *
 * @param {Components.interfaces.ISciMoz} scimoz - The editor control.
 * @param {Integer} indicator - The indicator to use for highlighting.
 * @param {Integer} pos - The position to highlight.
 */
function HighlightMove(scimoz, indicator, pos) {
    scimoz.indicatorCurrent = indicator;
    scimoz.indicatorClearRange(0, scimoz.length);
    var charlength = scimoz.positionAfter(pos) - pos;
    scimoz.indicatorFillRange(pos, charlength);
}

/**
 * Determine the position in the document for the co-ordinates.
 *
 * @param {Components.interfaces.ISciMoz} scimoz - The editor control.
 * @param {String} move - The coded chess move to make.
 */
function GetBoardPosition(scimoz, chesscode) {
    var col = chesscode.charCodeAt(0) - 'a'.charCodeAt(0);
    var row = '8'.charCodeAt(0) - chesscode.charCodeAt(1);
    return scimoz.findColumn(row+1, (col*2)+6);
}    

/**
 * Make the given chess move.
 *
 * @param {Components.interfaces.ISciMoz} scimoz - The editor control.
 * @param {String} move - The coded chess move to make.
 */
function MakeMove(scimoz, move) {
    var isTake = (move.indexOf("x") >= 0);
    move = move.replace("x", "");
    if (move.length == 8) {
        // Special double move for castling.
        MakeMove(scimoz, move.substr(4));
        move = move.substr(0, 4);
    }
    if (move.length >= 5) {
        move = move.substr(1);
    }
    var fromPos = GetBoardPosition(scimoz, move.substr(0, 2));
    scimoz.targetStart = fromPos;
    scimoz.targetEnd = scimoz.positionAfter(fromPos);
    piece = scimoz.getTextRange(fromPos, scimoz.targetEnd);
    scimoz.replaceTarget(" ".length, " ");
    HighlightMove(scimoz, indicMoveFrom, fromPos);
    var toPos = GetBoardPosition(scimoz, move.substr(2));
    scimoz.targetStart = toPos;
    scimoz.targetEnd = scimoz.positionAfter(toPos);
    scimoz.replaceTarget(piece.length, piece);
    HighlightSquares(scimoz);
    HighlightMove(scimoz, indicMoveTo, toPos);
    // Clear old messages.
    DisplayMessage(scimoz, "", false);
}    

/**
 * Make the given chess move.
 *
 * @param {Components.interfaces.ISciMoz} scimoz - The editor control.
 * @param {String} move - The coded chess move to make.
 */
function ProcessMove(scimoz, move) {
    move = move.replace("!", "");
    move = move.replace("?", "");
    move = move.replace("+", "");
    var match = move.match(/(\d+)\.\s*([\w\.]+)\s*(\w+)?/);
    if (!match.length) {
        dump("Unrecognized move: " + move + "\n");
    }
    var moveWhite = match[2];
    var moveBlack = match[3];
    if (moveWhite[0] != ".") {
        MakeMove(scimoz, moveWhite);
    } else {
        MakeMove(scimoz, moveBlack);
        return;
    }
    setTimeout(MakeMove, moveDisplayTime, scimoz, moveBlack);
}

/**
 * Play all of the chess moves and display the move commentary.
 *
 * @param {Components.interfaces.ISciMoz} scimoz - The editor control.
 */
function PlayMoves(scimoz) {
    var moves = movelist.split("\n");
    var state = "move";
    var message = "";
    var nexttimeout = 0;
    for (var i=0; i < moves.length; i++) {
        var move = ko.stringutils.strip(moves[i]);
        if (!move) {
            continue;
        }
        switch (state) {
            case "move":
                if (move.match(/^[0-9]+\./)) {
                    // Piece to move.
                    setTimeout(ProcessMove, nexttimeout, scimoz, move);
                    nexttimeout += moveDisplayTime;
                    nexttimeout += moveDisplayTime;
                    break;
                } else if (move[0] == "{") {
                    state = "message";
                    message = "";
                    move = move.substr(1);
                    // Fallthrough.
                } else {
                    continue;
                }
            case "message":
                if (move.indexOf("}") >= 0) {
                    move = move.substring(0, move.indexOf("}"));
                    state = "move";
                }
                if (message) message += " ";
                message += move;
                if (state == "move") {
                    setTimeout(DisplayMessage, nexttimeout, scimoz, message, false);
                    message = "";
                    nexttimeout += messageDisplayTime;
                }
                break;
        }
    }
}

/**
 * Play the chess game in the given editor.
 *
 * @param {Components.interfaces.koIScintillaView} view - The editor view.
 */
function PlayChess(view) {
    try {
        /**
         * @type {Components.interfaces.ISciMoz} - The editor control.
         */
        var scimoz = view.scimoz;
        DrawInitialBoard(scimoz);
        PlayIntro(scimoz, PlayMoves);
    } catch(ex) {
        // Exception handling - show problems to the user.
        alert("Error: " + ex + "\n\n" + ex.stack.toString());
    }
}

// Create a new text file asynchronously and start playing chess.
ko.views.manager.doNewViewAsync("Text", "editor", PlayChess);
