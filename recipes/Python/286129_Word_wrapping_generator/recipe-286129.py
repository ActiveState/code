strings = [
"""Deep Thoughts
   - by Jack Handy
   ===============""",
"It takes a big man to cry, but it takes a bigger man to laugh at that man.",
"When you're riding in a time machine way far into the future, don't stick your elbow out the window, or it'll turn into a fossil.",
"I wish I had a Kryptonite cross, because then you could keep both Dracula AND Superman away.",
"I don't think I'm alone when I say I'd like to see more and more planets fall under the ruthless domination of our solar system.",
"I hope if dogs ever take over the world, and they chose a king, they don't just go by size, because I bet there are some Chihuahuas with some good ideas.",
"The face of a child can say it all, especially the mouth part of the face."
]

def wordWrap(s,length):
    offset = 0
    while offset+length < len(s):
        if s[offset] in ' \n':
            offset += 1
            continue
        
        endOfLine = s[offset:offset+length].find('\n')
        if endOfLine < 0:
            endOfLine = s[offset:offset+length].rfind(' ')
        
        if endOfLine < 0:
            endOfLine = length
            newOffset = offset + endOfLine
        else:
            newOffset = offset + endOfLine + 1
        
        yield s[offset:offset+endOfLine].rstrip()
        
        offset = newOffset
    
    if offset < len(s):
        yield s[offset:].strip()
        

for s in strings:
    for l in wordWrap(s,20):
        print l
    print
