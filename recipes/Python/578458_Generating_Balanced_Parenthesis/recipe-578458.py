def pargen(left,right,ans):
    if(left==0 and right==0):
        print ans;
    if(left>0):
        pargen(left-1,right+1,ans+'(');
    if(right>0):
        pargen(left,right-1,ans+')');        
pargen(3,0,''); #can pass any starting value as left,initial value of right is always 0.
