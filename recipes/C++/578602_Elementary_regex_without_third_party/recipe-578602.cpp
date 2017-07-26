#include <fstream>
#include <iostream>
#include <windows.h>
#include <wininet.h>

using namespace std;

#pragma comment(lib, "wininet")

int main() {
  HINTERNET hNet, hUrl;
  DWORD dwBytesRead;
  char szData[1024];
  
  hNet = InternetOpen(NULL, INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);
  hUrl = InternetOpenUrl(hNet, "http://internet.yandex.ru/", NULL, 0, INTERNET_FLAG_RELOAD, 0);
  ofstream f("out.txt"); //temporary file

  //storing data into file  
  for (;;) {
    BOOL bRead = InternetReadFile(hUrl, szData, sizeof(szData - 1), &dwBytesRead);
    if (bRead == FALSE || dwBytesRead == 0) break;
    szData[dwBytesRead] = 0;
    f << szData;
  }

  //closing handles  
  f.close();
  InternetCloseHandle(hUrl);
  InternetCloseHandle(hNet);

  //getting needed string with findstr command :)
  system("for /f \"tokens=2* delims= \" %i in ('findstr /r /c:\"IPv4:\" out.txt') do @echo %i %j");
  DeleteFile("out.txt"); //removing temporary file
  
  return 0;
}
