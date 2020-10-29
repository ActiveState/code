#include<iostream>
#include<string.h>
using namespace std;
void CalZArray(char A[], int Z[]){
	int n = strlen(A);
	int i, l = 0 , r = 0;
	for(i = 1; i < n; i++){
		if(i<=r)
			Z[i] = Z[i-l];
		while(i + Z[i] < n){
			if(A[Z[i]] == A[i+Z[i]])
				Z[i]++;
			else
				break;
		}
		if(i + Z[i] - 1 > r){
			l = i;
			r = i + Z[i] - 1;
		}
	}
}
void Search(char A[], char B[]){
	char String[100];
	strcpy(String,B);
	strcat(String,"$");
	strcat(String,A);
	int Z[strlen(String)] = {0};
	Z[0] = -1;
	CalZArray(String,Z);
	for(int i=0;i<strlen(String);i++){
		if(Z[i] == strlen(B))
			cout<<"Pattern at :"<<i - strlen(B) - 1<<"\n";
	}
}
int main(){
	char A[40];
	char Pattern[10];
	cout<<"Enter the string: ";
	gets(A);
	cout<<"Enter the pattern to search: ";
	gets(Pattern);
	Search(A,Pattern);
	return 0;
}
