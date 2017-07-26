	
	public static String nextLexographicWord(String txt)
	{
		char [] letters = txt.toCharArray();
		int l = letters .length - 1;
		while(l >= 0)
		{
			if(letters[l] == 'z')
				letters[l] = 'a';
			else
			{
				letters[l]++;
				break;
			}
			l--;
		}
		if(l < 0) return 'a' + (new String(letters));
		return new String(letters); 
	}
