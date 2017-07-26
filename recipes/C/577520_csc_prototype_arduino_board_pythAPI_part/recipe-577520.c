//Author: Cheeng Shu Chin
#define ARRAY_SIZE(x) (sizeof(x) / sizeof(x[0]))
typedef String (*cmd_func_ptr)();
typedef String (*funcp)(String);
typedef struct
{
  String cmd;
  cmd_func_ptr func;
} command;
String cmd,cmdlck;
volatile int int0=0;
volatile int int1=0;
int dbg=1;
cmd_func_ptr func;
command commands[] = 
{
  {"echo", &echo},
  {"unknown", &unknown},
  {"pinmode", &pinmode},
  {"digitalwrite", &digitalwrite},
  {"digitalread", &digitalread},
  {"analogread", &analogread},
  {"analoreference", &analogreference},
  {"analogwrite", &analogwrite},
  {"tones", &tones},
  {"notones", &notones},
  {"shiftout", &shiftout},
  {"shiftin", &shiftin},
  {"pulsein", &pulsein},
  {"attachinterrupt", &attachinterrupt},
  {"detachinterrupt", &detachinterrupt},
  {"cinterrupts", &cinterrupts},
  {"nocinterrupts", &nocinterrupts},
  {"debug", &debug},
  {"pycall", &pycall},
  {"test", &test},
  {"nop", &nop},
};
String rdata(String cstr)
{
  readagain:
  if (dbg>0)
  {
    reply(cstr);
  }else{
    reply("?");
  }
  String cst = "";
  while(Serial.available()>0)
  {
    cst += byte(Serial.read());
  }
  if (cst.equalsIgnoreCase("!"))
  {
    sprintln("cmd = "+cmdlck);
    goto readagain;
  }
  return cst;
}
void reply(String cst)
{
  loopagain:
  if (int0 != 0)
  {
    sprintln("!INT0 ?");
    int0 = 0;
    goto loopagain;
  }
  if (int1 != 0)
  {
    sprintln("!INT1 ?");
    int1 = 0;
    goto loopagain;
  }
 sprintln(cst);
  while(Serial.available()<1)
  {
  }
}
String nop()
{
  return "";
}
String test()
{
  int intp=str2int(rdata("interrupts ?"));
  if (intp == 0)
  {
    int0 = !int0;
  }
  if (intp == 1)
  {
    int1 = !int1;
  }
  return "";
}
String debug()
{
  dbg=str2int(rdata("debug ?"));
  return "";
}  
String unknown()
{
  return "unkown command: " + cmd;
}
void sprint(String cst)
{
  Serial.print(cst);
}
void sprintln(String cst)
{
  Serial.println(cst);
}
int str2int(String dt)
{
  char str[dt.length()+1];
  dt.toCharArray(str,dt.length()+1);
  return atoi(str);
}
String pinmode()
{
  int pin=str2int(rdata("pin ?"));
  int mode=str2int(rdata("mode ?"));
  pinMode(pin,mode);
  return "";
}
String digitalwrite()
{
  int pin=str2int(rdata("pin ?"));
  int value=str2int(rdata("value ?"));
  digitalWrite(pin,value);
  return "";
}
String digitalread()
{
  int pin=str2int(rdata("pin ?"));
  return digitalRead(pin);
}
String analogreference()
{
  int pin=str2int(rdata("type ?"));
  analogReference(pin);
  return "";
}
String analogwrite()
{
  int pin=str2int(rdata("pin ?"));
  int value=str2int(rdata("value ?"));
  analogWrite(pin, value);
  return "";
}
String analogread()
{
  int pin=str2int(rdata("pin ?"));
  return analogRead(pin);
}
String tones()
{
  int pin=str2int(rdata("pin ?"));
  int frequency=str2int(rdata("frequency ?"));
  int duration=str2int(rdata("duration ?"));
  tone(pin, frequency, duration);
  return "";
}
String notones()
{
  int pin=str2int(rdata("pin ?"));
  noTone(pin);
  return "";
}
String shiftout()
{
  int dataPin=str2int(rdata("dataPin ?"));
  int clockPin=str2int(rdata("clockPin ?"));
  int bitOrder=str2int(rdata("bitOrder ?"));
  int value=str2int(rdata("value ?"));
  shiftOut(dataPin, clockPin, bitOrder, value);
  return "";
}
String shiftin()
{
  int dataPin=str2int(rdata("dataPin ?"));
  int clockPin=str2int(rdata("clockPin ?"));
  int bitOrder=str2int(rdata("bitOrder ?"));
  return shiftIn(dataPin, clockPin, bitOrder);
}
String pulsein()
{
  int pin=str2int(rdata("pin ?"));
  int value=str2int(rdata("value ?"));
  int timeout=str2int(rdata("timeout ?"));
  return pulseIn(pin, value, timeout);
}
String attachinterrupt()
{
  int interrupt=str2int(rdata("interrupt ?"));
  if (interrupt == 0)
  {
    attachInterrupt(interrupt, pycallback0, CHANGE);
  }
  if (interrupt == 1)
  {
    attachInterrupt(interrupt, pycallback1, CHANGE);
  }
  return "";
}
void pycallback0()
{
  int0 = !int0;
}
void pycallback1()
{
  int1 = !int1;
}
String detachinterrupt()
{
  int interrupt=str2int(rdata("interrupt ?"));
  detachInterrupt(interrupt);
  return "";
}
String cinterrupts()
{
  interrupts();
  return "";
}
String nocinterrupts()
{
  noInterrupts();
  return "";
}
String echo()
{
  return rdata(cmd+" ?");
}
String pycall()
{
  String fc=rdata("Func ?");
  return funcparser(fc);
}
String funcparser(String cmdc)
{
  byte i = 0;
  func = &unknown;
  for(i = 0; i != ARRAY_SIZE(commands); ++i)
  {
    if (commands[i].cmd.equalsIgnoreCase(cmdc))
    {
      func = commands[i].func;
      break;
    }
  }
  return func();
}
void setup() 
{
  Serial.begin(115200);
}
void loop()
{
  cmdlck = "";
  cmd = rdata("?");
  cmdlck = cmd;
  sprintln(funcparser(cmd));
}
