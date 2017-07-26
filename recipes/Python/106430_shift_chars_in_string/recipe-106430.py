shift = lambda text,sft=1:string.joinfields(map(eval("lambda ch:chr((ord(ch)-ord('a')+%d)%%26+ord('a'))"%(sft,)),text),'')


shift2 = lambda txt,sft=1:''.join([[ch,chr((ord(ch) - ord(['A','a'][ch.islower()]) + sft)%26+ord(['A','a'][ch.islower()]))][ch.isalpha()] for ch in txt])

#test
print shift2('Ab-Phkew! 123...',7)
for i in range(26):print shift2('abcdefghijklmnopqrstuvwxyz',i)
