// Turns monitor off for ~10 seconds then turns back on
// LogicKills 
// Have Fun and head over to logickills.org for new code~
#include <windows.h>
#include <ctime>

int main()
{
 
  int seconds = 20;
  clock_t delay = seconds *CLOCKS_PER_SEC;
  clock_t start = clock();
  while(clock() - start < delay){
  SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, (LPARAM) 2);}
  SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, (LPARAM) 2);
 // SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, (LPARAM) 2);
// three loops are used in case if like while loop and do while loop and for loop....
    return 0;
}
