/******************************************************************/
/***	This is a counter which increments by 1 every second	***/
/******************************************************************/

public class Timer{

	public static void main(String[] args){
	
		int count = 0;
		for(;;){
			try {
				Thread.sleep(1000);
				count ++;
				System.out.println(count);
			}
			catch (InterruptedException e) {
				
				e.printStackTrace();
			}
		}
	}
}
