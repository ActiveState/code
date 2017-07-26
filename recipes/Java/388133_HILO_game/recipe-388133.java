public class Program12
 {
 	static int guess;
 	static int randnum;
 	static int counter;
 	static boolean finished; 		 	
 	
 	public static void main(String[] args)
 	{
 		int closest=100;
 		int tempclosest=100;
 		Instructions();
 		randnum=(int)(Math.random()*100)+1;
 		counter=1;
		EasyReader console=new EasyReader();
		
		finished=false;
		while(!finished && counter!=5)
		{
		System.out.println();
		System.out.print("What's your guess? ");
		guess=console.readInt();
		
		 if(guess<randnum)
		  {tooLow();
		   tempclosest=randnum-guess;
		   if(tempclosest<closest)
		   closest=tempclosest;
		  }
		 if(guess>randnum)
		  {tooHigh();
		   tempclosest=guess-randnum;
		   if(tempclosest<closest)
		   closest=tempclosest;
		  }
		  
		 if(guess==randnum)
		  {youWin();
		  
		  }
		 else
		 {
		 if(counter==4)
		  youLose(closest);
		 }
		 counter++;
		}
	}
	
 		
 	public static void Instructions()
 	{
 		Util.center("THE SUPER DOOPER SECRET NUMBER GAME!!!");
 		System.out.println();
 		System.out.println("Hi, and welcome to the secret number game");
 		System.out.println("The rules of this game are simple");
 		System.out.println("1. Guess a number between 1-100");
 		System.out.println("2. Then choose another number based on if you were too HIGH or too LOW");
 		System.out.println("3. Also you only have 4 guesses so BE SMART!!!");
 		System.out.println();
 		System.out.println("Ok I am thinking of a number between 1-100");
 	}

	public static void tooHigh()
	{
		System.out.println("TO HIGH TRY AGAIN(choose a lower #)");
	}
	
	public static void tooLow()
	{
			System.out.println("TO LOW TRY AGAIN(choose a higher #)");
	}
	
	public static void youWin()
	{
		System.out.println("YOU GUESSED IT in " +counter+" tries!!!");
		finished=true;
		
	}
	
	public static void youLose(int x)
	{	
		 finished=true;
		 System.out.println();
		 System.out.println("Sorry you did not guess correctly in 4 tries");
		 if(x==1)
		 {System.out.print("Now doesn't that stink, you were only one away from");
		 System.out.println(" the secret number!");}		 
		 else
		 {System.out.println("Your closest guess was "+Math.abs(x)+" away");
		 System.out.println("...PLEASE TRY AGAIN...");
		 System.out.println("The secret number was "+randnum);}
		 System.out.println();
	}
}
