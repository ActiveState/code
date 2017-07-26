#GPL3

def regex_for_range(min,max):
    """A recursive function to generate a regular expression that matches
    any number in the range between min and max inclusive.

    Usage / doctests:
    >>> regex_for_range(13,57)
    '4[0-9]|3[0-9]|2[0-9]|1[3-9]|5[0-7]'
    >>> regex_for_range(1983,2011)
    '200[0-9]|199[0-9]|198[3-9]|201[0-1]'
    >>> regex_for_range(99,112)
    '99|10[0-9]|11[0-2]'

    Note: doctests are order sensitive, while regular expression engines don't care.  So you may need to rewrite these
    doctests if making changes.
    """
    #overhead
    #assert (max>=min) and (min>=0)
    _min,_max=str(min),str(max)
    #calculations
    if min==max:
        return '%s' % str(max)
    if len(_max)>len(_min):
        #more digits in max than min, so we pair it down into sub ranges
        #that are the same number of digits.  If applicable we also create a pattern to
        #cover the cases of values with number of digits in between that of
        #max and min.
        re_middle_range=None
        if len(_max)>len(_min)+2:
            #digits more than 2 off, create mid range
            re_middle_range='[0-9]{%s,%s}' % (len(_min)+1,len(_max)-1)
        elif len(_max)>len(_min)+1:
            #digits more than 1 off, create mid range
            #assert len(_min)+1==len(_max)-1 #temp: remove
            re_middle_range='[0-9]{%s}' % (len(_min)+1)
        #pair off into sub ranges
        max_big=max
        min_big=int('1'+('0'*(len(_max)-1)))
        re_big=regex_for_range(min_big,max_big)
        max_small=int('9'*len(_min))
        min_small=min
        re_small=regex_for_range(min_small,max_small)
        if re_middle_range:
            return '|'.join([re_small,re_middle_range,re_big])
        else:
            return '|'.join([re_small,re_big])
    elif len(_max)==len(_min):
        def naive_range(min,max):
            """Simply matches min, to max digits by position.  Should create a
            valid regex when min and max have same num digits and has same 10s
            place digit."""
            _min,_max=str(min),str(max)
            pattern=''
            for i in range(len(_min)):
                if _min[i]==_max[i]:
                    pattern+=_min[i]
                else:
                    pattern+='[%s-%s]' % (_min[i],_max[i])
            return '%s' % pattern
        if len(_max)==1:
            patterns=[naive_range(min,max)]
        else:
            #this is probably the trickiest part so we'll follow the example of
            #1336 to 1821 through this section
            patterns=[]
            distance=str(max-min) #e.g., distance = 1821-1336 = 485
            increment=int('1'+('0'*(len(distance)-1))) #e.g., 100 when distance is 485
            if increment==1:
                #it's safe to do a naive_range see, see def since 10's place is the same for min and max
                patterns=[naive_range(min,max)]
            else:
                #create a function to return a floor to the correct digit position
                #e.g., floor_digit_n(1336) => 1300 when increment is 100
                floor_digit_n=lambda x:int(round(x/increment,0)*increment)
                #capture a safe middle range
                #e.g., create regex patterns to cover range between 1400 to 1800 inclusive
                #so in example we should get: 14[0-9]{2}|15[0-9]{2}|16[0-9]{2}|17[0-9]{2}
                for i in range(floor_digit_n(max)-increment,floor_digit_n(min),-increment):
                    len_end_to_replace=len(str(increment))-1
                    if len_end_to_replace==1:
                        pattern='%s[0-9]' % str(i)[:-(len_end_to_replace)]
                    else:
                        pattern='%s[0-9]{%s}' % (str(i)[:-(len_end_to_replace)],len_end_to_replace)
                    patterns.append(pattern)
                #split off ranges outside of increment digits, i.e., what isn't covered in last step.
                #low side: e.g., 1336 -> min=1336, max=1300+(100-1) = 1399
                patterns.append(regex_for_range(min,floor_digit_n(min)+(increment-1)))
                #high side: e.g., 1821 -> min=1800 max=1821
                patterns.append(regex_for_range(floor_digit_n(max),max))
        return '|'.join(patterns)
    else:
        raise ValueError('max value must have more or the same num digits as min')
