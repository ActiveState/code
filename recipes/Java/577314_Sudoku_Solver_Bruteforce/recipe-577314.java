/**
 * 
 */
package org.mechaevil.util.Misc;

/**
 * @author st0le
 *
 */
public class SudokuSolver {
	
	public static boolean solvePuzzle9(int [][]matrix)
	{
		int x=0,y=0;
		boolean found = false;
		for(x = 0;x < 9; x ++)
		{
			for(y = 0;y < 9; y++)
			{
				if(matrix[x][y] == 0)
				{
					found = true;
					break;
				}
			}
			if( found ) break;
		}
		if(!found) return true;
		
		boolean digits[] = new boolean[11];
		for(int i = 0; i < 9; i++)
		{
			digits[matrix[x][i]] = true;
			digits[matrix[i][y]] = true;
		}
		int bx = 3 * (x/3), by = 3 * (y/3);
		for(int i =0;i<3;i++)
			for(int j = 0; j < 3; j++)
				digits[matrix[bx+i][by+j]] = true;
		
		for(int i = 1 ; i <= 9; i++)
		{
			if(!digits[i] )
			{
				matrix[x][y] = i;
				if(solvePuzzle9(matrix))
					return true;
				matrix[x][y] = 0;
			}
		}
		return false;
	}
}
