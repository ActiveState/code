public static class StringExtensions
{
    public static string Replace(this String str, char[] chars, string replacement)
    {
        StringBuilder output = new StringBuilder(str.Length);

        for (int i = 0; i < str.Length; i++)
        {
            char c = str[i];

            bool replace = false;
            for (int j = 0; j < chars.Length; j++)
            {
                if (chars[j] == c)
                {
                    replace = true;
                    break;
                }
            }

            if (replace)
                output.Append(replacement);
            else
                output.Append(c);
        }

        return output.ToString();
    }
}
