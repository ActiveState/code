def dis(a,b):
    return (  (b[0]-a[0])**2 + (b[1]-a[1])**2   )**.5
def lineDis(m,y,point):
    """slope in decimal, y intercept, (x,y)"""
    a = m
    b = -1
    c = y
    m = point[0]
    n = point[1]
    return abs(a*m+b*n+c)/((a)**2+(b)**2)**.5
def findMY(a,b):
    """return slope(m), y intercept(y)"""
    x1,y1,x2,y2 = a[0],a[1],b[0],b[1]
    x1 = float(x1)
    y1 = float(y1)
    slope = (x2-x1)/(y2-y1)
    x,y=a[0],a[1]
    while x != 0:
        if x < 0:
            x+=1
            y += slope
        if x > 0:
            x-=1
            y-=slope
    yint = y
    return slope, yint
def triArea(a,b,c):
    h=dis(a,b)
    m,y = findMY(a,b)
    b=lineDis(m,y,c)
    return .5*h*b

    
