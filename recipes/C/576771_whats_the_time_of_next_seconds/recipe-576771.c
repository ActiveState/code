#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define YEAR 0
#define MONTH 1
#define DAY 2
#define HOUR 3
#define MINUTE 4
#define SECOND 5

//the maximum value of each time region
int limit[] = {0,12,-1,23,59,59};



void nextTime(int time[], int timeRegion, int increment);

int main(int argc, char **argv){

    char *current = malloc(20);

    strcpy(current, "2004-11-30-23-59-59");


    //parsing for the values
    char *token = strtok(current,"-");

    int i = 0;
    int time[6];
    do{

              time[i] = atoi(token);
              printf("%d\t",time[i]);
              token = strtok(NULL,"-");
              i++;
    }while(token);

    printf("\n");
   //compute for the next second
    nextTime(time,SECOND,1);
     for(i=0;i<6;i++){
                   printf("%d\t",time[i]);
     }


    getchar();
}

/*recursively compute the next value for second, mins....
*/
void nextTime(int time[], int timeRegion, int increment){

    switch(timeRegion){
        //month
        case DAY:
            if(increment){
                if(time[MONTH] == 2){
                    if(time[YEAR]%4 == 0){
                        //28 days
                        increment = (time[DAY] == 28)?1:0;
                        time[DAY] = time[DAY]+1-increment*28;
                    }
                    else{
                        //29 days in this month
                        increment = (time[DAY] == 29)?1:0;
                        time[DAY] = time[DAY]+1-increment*29;
                    }


                }
                else{
                    if((time[MONTH]+time[MONTH]/8)%2 == 1){
                        increment = (time[DAY] == 31)?1:0;
                        time[DAY] = time[DAY]+1-increment*31;
                    }
                    else{
                        increment = (time[DAY] == 30)?1:0;
                        time[DAY] = time[DAY]+1-increment*30;
                    }
                 }
            }
            break;
        default:

            if(increment){
                increment = (time[timeRegion] == limit[timeRegion])?1:0;

                time[timeRegion] = time[timeRegion]+1 ;

                if(timeRegion == YEAR){
                    return;
                }
                else{
                    nextTime(time, timeRegion-1, increment);
                }
            }
            if(timeRegion != MONTH){
                time[timeRegion] -= increment*(limit[timeRegion]+1);
            }
            else{
                time[timeRegion] -= increment*(limit[timeRegion]);
            }

    }
    break;
}
