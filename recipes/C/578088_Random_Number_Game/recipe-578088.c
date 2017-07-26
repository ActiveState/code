/********************************************************************************************
|                                 C O M M E N T S                                           |   
+-------------------------------------------------------------------------------------------+
| T I T L E:    random_number_gamev3.c							                            |
| A U T H O R:  Jacob A. Bridges                                                            |
| D A T E:      3.1.2011                                                                    |
|											                                                |
| This program will take a range of numbers from the user and randomly select one number.   |
|     Then it asks the user to guess the random number. Keeps track of times the user       |
|     tries to guess the number.							                                |
|   											                                            |
| What new in Version 3? The game keeps track of your average scores for every game then    | 				
|     displays them when the player stops playing the game. It also displays the average    |
|     of all your scores.								                                    |
|											                                                |
+-------------------------------------------------------------------------------------------+
********************************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/////////////////////////////////////////////////////////////////////////////////////////////
   // Defining some Gloabl Variables
/////////////////////////////////////////////////////////////////////////////////////////////

int iR_NUMBER = 0;
int iCHOICE   = 0;
int iCOUNTER  = 0;
int iMIN      = 0;
int iMAX      = 0;
int iRANGE    = 0;
int iSCORE    = 0;
int iSCORES   = 0;
int iTOTAL    = 0;
char NEWGAME  = 0;


int main ()
{

	int *scores;
	int *temp_storage;
	int score_index;
/////////////////////////////////////////////////////////////////////////////////////////////
   // Header
/////////////////////////////////////////////////////////////////////////////////////////////

   printf("\n\n");
   printf("\t#####################\n");
   printf("\t# THE GUESSING GAME #\n");
   printf("\t#####################\n");
   printf("\nWelcome to the Random Number Guessing Game!\n");

/////////////////////////////////////////////////////////////////////////////////////////////
   // Beginning of the "PLAY AGAIN?" loop
/////////////////////////////////////////////////////////////////////////////////////////////

do {
	 if (iTOTAL)
		temp_storage = scores;
     // iTOTAL used to keep track of games played
     iTOTAL = iTOTAL + 1;
	 scores = calloc(iTOTAL, sizeof(int));
	 if (iTOTAL != 1)
	 {
		for (score_index = 0; score_index < iTOTAL - 1; score_index++)
			scores[score_index] = temp_storage[score_index];
		free(temp_storage);
	 }
/////////////////////////////////////////////////////////////////////////////////////////////
   // Setting a range of values
/////////////////////////////////////////////////////////////////////////////////////////////

     printf("Please start by picking a range of values: \n\n");
     printf("Highest value in range: ");
     scanf(" %d", &iMAX);
     printf("Lowest value in range: ");
     scanf(" %d", &iMIN);
     printf("\n > You chose the range to be from %d  to %d. < ", iMIN, iMAX);
     iRANGE = (iMAX - iMIN);

     // Seeding the random function
     srand( time( NULL ) );

     // Setting counter to ZERO
     iCOUNTER = 0;

/////////////////////////////////////////////////////////////////////////////////////////////
   // Selecting a random value from our range
/////////////////////////////////////////////////////////////////////////////////////////////

     int iR_NUMBER = ( iMIN + ( rand() % ( iRANGE + 1 ) ) );

/////////////////////////////////////////////////////////////////////////////////////////////
   // The WHILE loop
/////////////////////////////////////////////////////////////////////////////////////////////

     printf("\n\nCan you guess the number I am thinking of?");
     do {
  	  // Starting the counter
          iCOUNTER = iCOUNTER + 1;

	  // Asks the user for a number
	  printf("\nYour Guess: ");
  	  scanf( " %d", &iCHOICE );

	  // Compares the user's input to the random number
 	  if( iCHOICE < iR_NUMBER )
		  printf( "Your guess is too low, try again!" );
	  else if( iCHOICE > iR_NUMBER )
		  printf( "Your guess is too high, try again!" );
	  else
		  printf( "\n\n\t*YOU GUESSED IT!*\n\n" );
        } while( iCHOICE != iR_NUMBER );

/////////////////////////////////////////////////////////////////////////////////////////////
   // End of game sequence
/////////////////////////////////////////////////////////////////////////////////////////////

     // Calculates player's "GRADE"
     iSCORE = (int)(100 * ((float)(iRANGE - iCOUNTER) / iRANGE));
     //printf(" %d%%\n", iSCORE);

     // Logs your score
     iSCORES = iSCORES + iSCORE;
     
     // Tells the answer
     printf( "The answer was %d.", iR_NUMBER );

     // Gives the player's "score"
     printf( "\nIt took you %d guesses.", iCOUNTER );
     if( iSCORE == 100 )
  	  printf( " AMAZING GUESS!" );
     else if( iSCORE >= 90 )
	  printf( " Great job!" );
     else if( iSCORE >= 80 )
	  printf( " Nice Work." );
     else if( iSCORE >= 70 )
	  printf( " Try harder next time." );
     else if( iSCORE >= 60 )
	  printf( " You are bad at this game." );
     else 
	  printf( " EPIC FAIL." );

/////////////////////////////////////////////////////////////////////////////////////////////
   // Option to play again
/////////////////////////////////////////////////////////////////////////////////////////////

     printf("\nWould you like to play again?    Y/N? \n >  ");
     scanf(" %c", &NEWGAME);
	 
	 scores[iTOTAL - 1] = iSCORE;

     } while (NEWGAME == 'y' || NEWGAME == 'Y');
   
   // If player chooses to end game
   printf("\n+-----------------------------------------------------+");
   printf("\n|  You played %d time(s).", iTOTAL);
   printf("\n|  Your average score was %d%%\n", (iSCORES/iTOTAL));
   
   for (score_index = 0; score_index < iTOTAL; score_index++)
		printf("|  Score for game %d: %d%%\n", score_index + 1, scores[score_index]);
   free(scores);
   printf("+-----------------------------------------------------+");
   printf("\n");
   system("pause");

   
   return 0;
}
