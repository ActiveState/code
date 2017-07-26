/**
    @author   Thomas Lehmann
    @file     queen.js
 */
var OCCUPIED = 1; // field is in use
var FREE     = 0; // field is not in use
var OUTPUT   = 1; // when 1 show solutions

function log(text) {
    // this can be used when running with "node.js"
    // console.log(text);

    // this can be used inside of html
    document.write(text + "<br/>");
}

function Queen(width) {
    this.width      = width;
    this.lastRow    = this.width - 1;
    this.columns    = new Array(this.width);
    this.rcolumns   = new Array(this.width);

    var numberOfDiagonals = 2 * this.width - 1
    this.diagonals1 = new Array(numberOfDiagonals);
    this.diagonals2 = new Array(numberOfDiagonals);
    this.solutions  = new Array();

    for (var index = 0; index < numberOfDiagonals; ++index) {
        if (index < this.width) {
            this.columns[index] = -1;
        }
        this.diagonals1[index] = FREE;
        this.diagonals2[index] = FREE;
    }

    // starts the search with initial parameters
    this.run = function() {
        this.calculate(0);
    }

    // searches for all possible solutions
    this.calculate = function(row) {
        for (var column=0; column < this.width; ++column) {
            // current column blocked?
            if (this.columns[column] >= 0) {
                continue;
            }

            // relating diagonale '\' depending on current row and column
            var ixDiag1 = row + column;
            if (this.diagonals1[ixDiag1] == OCCUPIED) {
                continue;
            }

            // relating diagonale '/' depending on current row and column
            var ixDiag2 = this.width - 1 - row + column;
            if (this.diagonals2[ixDiag2] == OCCUPIED) {
                continue;
            }

            // occupying column and diagonals depending on current row and column
            this.columns[column]     = row;
            this.diagonals1[ixDiag1] = OCCUPIED;
            this.diagonals2[ixDiag2] = OCCUPIED;

            if (row == this.lastRow) {
                this.solutions.push(this.columns.slice());
            } else {
                this.calculate(row + 1);
            }

            this.columns[column]     = -1;
            this.diagonals1[ixDiag1] = FREE;
            this.diagonals2[ixDiag2] = FREE;
        }
    }
}

function main() {
    var instance = new Queen(8);
    log("Queen raster (" + instance.width + "x" + instance.width + ")");
    var start = new Date().getTime();
    instance.run();
    log("...calculation took " + (new Date().getTime() - start) + " ms");
    log("...with " + instance.solutions.length + " solutions");

    if (OUTPUT == 1) {
        for (var indexA=0; indexA < instance.solutions.length; ++indexA) {
            var solution = instance.solutions[indexA];
            line = "";
            for (var indexB=0; indexB < solution.length; ++indexB) {
                line += "(" + (indexB+1) + "," + (solution[indexB]+1) + ")";
            }
            log(line);
        }
    }
}

main();
