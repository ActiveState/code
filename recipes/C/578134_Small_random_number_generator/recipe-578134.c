int random(int start,int end){
	int h;
	float k;
	h=(int)malloc(sizeof(int));
	h=h%10000;
	k=((float)h)/10000;
	k=start+(end-start)*k;
	return k;
}
