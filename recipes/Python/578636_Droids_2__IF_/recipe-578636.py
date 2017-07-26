# -For learner's and beginner's like myself    -#
# -or for anyone who may have enjoyed Droids. -#
import time
import random
from random import randint

print('\n' * 110)
print('=============================')
print('DROIDS 2 - by jay - type help')
print('=============================')
print('\n\nCytek inc. 02.10.2214')
time.sleep(2) 
print('\nCMBT645 Re-Boot Sequence..')
time.sleep(1)
print('\nInitalizing Combat Droid 645..')
time.sleep(1)
print('....')
time.sleep(1)
print('\nTwin laser offline..')
time.sleep(1)
print('Motion tracker offline..')
time.sleep(1)
print('Disruptor offline..')
time.sleep(1)
print('\nService port avaliable..')
time.sleep(1)
print('\nNo Software Installed..')
time.sleep(1)
print('\nCombat Droid active')
time.sleep(1)
print('\nCMBT645 ONLINE >> ')
time.sleep(2)
print('''\n\nYou are the 645 Combat Droid aboard 
the Droid Cruiser PROXY. Enemy droids have boarded
and have taken over flight path. You are damaged & have been 
re-initialized but your Twin laser , Disruptor
and Motion Tracker are offline.''')

def start(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('\n[-MAIN ELEVATOR-]')
	print('\n1.)   deck 1  - Cargo Hold')
	print('2.)   deck 2  - Docking') 
	print('3.)   deck 3  - Droid Hangar')
	print('4.)   deck 4  - Security')
	print('5.)   deck 5  - Re-Charge')
	print('6.)   deck 6  - Power Core')
	print('7.)   deck 7  - Shield Generator')
	print('8.)   deck 8  - Cruiser Control')
	print('9.)   deck 9  - Observation')
	print('10.)  deck 10 - Droid Software System')
	cmdlist = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
	cmd = getcmd(cmdlist)
	if cmd == '1':
		if 'PBE111' in droids:
			print('\n- DECK 1 SECURED - ACCESS LOCKED -')
			time.sleep(2)
			start(armory, programs, droids)
		else:
			cargo_hold(armory, programs, droids)
	elif cmd == '2':
		if 'zx4e9q' not in programs:
			print('\n<< MEECDT1000 DROID OVER-RIDE - ACCESS DENIED >>')
			time.sleep(2)
			start(armory, programs, droids)
		else:
			docking(armory, programs, droids)
	elif cmd == '3':
		if 'CMBT646' in droids and 'CMBT647' in droids:
			print('\n- DECK 3 SECURED - ACCESS LOCKED -')
			time.sleep(2)
			start(armory, programs, droids)
		else:
			droid_hangar(armory, programs, droids)
	elif cmd == '4':
		if 'MEECDT1000' in programs and 'zx4e9q' in programs:
			print('\n- DECK 4 SECURED - ACCESS LOCKED -')
			time.sleep(2)
			start(armory, programs, droids)
		else:
			security(armory, programs, droids)
	elif cmd == '5':
		if 'MEECDT1000' in programs and 'zx4e9q' in programs:
			print('\n- DECK 5 SECURED - ACCESS LOCKED -')
			time.sleep(2)
			start(armory, programs, droids)
		else:
			recharging(armory, programs, droids)
	elif cmd == '6':
		if 'twin laser' in armory:
			print('\n- DECK 6 SECURED - ACCESS LOCKED -')
			time.sleep(2)
			start(armory, programs, droids)
		else:
			power_core(armory, programs, droids)
	elif cmd == '7':
		if 'console hack' in programs:
			print('\n- DECK 7 SECURED - ACCESS LOCKED -')
			time.sleep(2)
			start(armory, programs, droids)
		else:
			shield(armory, programs, droids)
	elif cmd == '8':
		if 'MEECDT1000' in programs and 'zx4e9q' in programs:
			print('\n- DECK 8 SECURED - ACCESS LOCKED -')
			time.sleep(2)
			start(armory, programs, droids)
		else:
			cruiser_control(armory, programs, droids)
	elif cmd == '9':
		if 'droid hack' in programs:
			print('\n- DECK 9 SECURED - ACCESS LOCKED -')
			time.sleep(2)
			start(armory, programs, droids)
		else:
			observation(armory, programs, droids)
	elif cmd == '10':
		if 'motion tracker' in armory and 'disruptor' in armory:
			print('\n- DECK 10 SECURED - ACCESS LOCKED -')
			time.sleep(2)
			start(armory, programs, droids)
		else:
			droid_software(armory, programs, droids)
		
def shield(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nYou are on the Shield Generator Deck
Sentry Droid 529 is defending the Shield Generator
but has been Disrupted by Enemy Sentry Droid 771.
You have seconds before your next.. ''')
	print('\n[-SHIELD GENERATOR-]\n')
	print('1.) Terminate Enemy Sentry droid 771')
	print('2.) Retreat to main elevator')
	cmdlist =['1', '2']
	cmd = getcmd(cmdlist)
	if cmd == '1':
		if 'twin laser' in armory:
			print('\nTwin laser active...')
			time.sleep(1)
			print('Targeting SEN771...')
			time.sleep(1)
			print('\nTarget locked...')
			time.sleep(1)
			print('...')
			time.sleep(1)
			print('\nTARGET TERMINATED\n')
			time.sleep(2)
			print('''Enemy Sentry Droid 771 has been terminated
and it's connection outlet is destroyed.''')
			hackdroid(programs)
		else:
			enemysen(armory, programs, droids)
	elif cmd == '2':
			time.sleep(1)
			print('\nYou try to retreat but its to late..')
			time.sleep(2)
			print('\nEnemy Sentry Droid 771 has you Locked on.')
			time.sleep(2)
			print('\nSEN771:> 0011100000001000000011100000')
			time.sleep(1)
			print('\n....')
			time.sleep(1)
			print('\nShutdown imminent...')
			time.sleep(1)
			print('CMBT645 offline.')
			time.sleep(1)
			print('Droid terminated.')
			print('\n- GAME OVER -\n')
			exit(0)
		
def security(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nYou are on the Security Deck. This is where all
Surveillance aboard the Cruiser is done. 
Sentry Droid 529 is absent from the Console.''')
	print('\n[-SECURITY-]\n')
	print('1.) View Surveillance monitors on other decks')
	print('2.) Access Main Console')
	print('3.) Return to Main Elevator')
	cmdlist = ['1', '2', '3', 'console hack']
	cmd = getcmd(cmdlist)
	if cmd == '1':
		print('\n----------')
		print('\nBooting Monitors....')
		time.sleep(1)
		print('....')
		time.sleep(1)
		print('...')
		time.sleep(1)
		print('\nMonitors active.')
		time.sleep(1)
		print('\n[-SURVEILLANCE FEED-]')
		print('''\nDECK 1  - This Deck appears to be clear.
\nDECK 2  - A Enemy Droid Shuttle is docked here.
\nDECK 3  - MONITOR OFFLINE - NO LIVE FEED.
\nDECK 5  - MONITOR OFFLINE - NO LIVE FEED.
\nDECK 6  - MONITOR OFFLINE - NO LIVE FEED.
\nDECK 7  - MONITOR OFFLINE - NO LIVE FEED.
\nDECK 8  - A T1000 Master Elite Enemy Command Droid. 
\nDECK 9  - A small Low Class Enemy Scouter Droid.
\nDECK 10 - This Deck appears to be clear''')
		time.sleep(2)
		security(armory, programs, droids)
	elif cmd == '2':
		print('\n - ACCESS TO MAIN CONSOLE DENIED -')
		time.sleep(2)
		security(armory, programs, droids)
	elif cmd == '3':
		start(armory, programs, droids)
	elif cmd == 'console hack':
		if 'console hack' in programs:
			print('\nloading console hack....')
			time.sleep(2)
			print('....')
			time.sleep(2)
			print('10000101010101010101010' * 1000)
			time.sleep(1)
			print('....')
			time.sleep(1)
			print('Accessing encrypted files...')
			time.sleep(2)
			print('Decrypting....')
			time.sleep(2)
			print('\n[- SECURITY MAIN CONSOLE -]')
			time.sleep(1)
			print('\nDAILY OVER-RIDE CODES- HANGAR DROIDS')
			time.sleep(1)
			print('\n-Combat Droids  -  zx71vbq')
			time.sleep(1)
			print('\n-Sentry Droids  -  9jt2zm5')
			time.sleep(1)
			print('\n-Repair Droids  -  lk0sa8c')
			time.sleep(1)
			print('\n-Control Droids -  44qaz5x')
			time.sleep(1)
			print('\nCODES WILL BE RESET EVERY 24 HOURS')
			time.sleep(2)
			print('\n=====================================')
			print('\nDROID SOFTWARE SYSTEM - SECURE CODES')
			time.sleep(1)
			print('\n-Sentry Droids  -  qiy25az')
			time.sleep(1)
			print('\n-Combat Droids  -  w7md3sx')
			time.sleep(1)
			print('\n-Repair Droids  -  zp11dcy')
			time.sleep(1)
			print('\n-Control Droids -  kkx2s3q')
			time.sleep(1)
			print('\nCODES WILL BE RESET EVERY 24 HOURS')
			time.sleep(4)
			security(armory, programs, droids)
		else:
			print('\n - CONSOLE HACK PROGRAM NOT DETECTED -')
			time.sleep(2)
			security(armory, programs, droids)
			
def hackdroid(programs, items=['console hack']):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nSentry droid 529 is disrupted
but has a Console Hack program installed.
You MUST connect to this droid with service port 
and download the program.''')
	if len(items) > 0:
		for item in items:
			print('\n--> %s' % (item))
	cmdlist = ['service port']
	cmd = getcmd(cmdlist)
	if cmd == 'service port':
			programs.append('console hack')
			items = ['console hack']
			print('\nservice port connected.')
			time.sleep(1)
			print('accessing file..')
			time.sleep(1)
			print('downloading..')
			time.sleep(1)
			print('....')
			time.sleep(1)
			print('\ndownload complete.')
			time.sleep(1)
			print('\nYou have the Console Hack program')
			print('and return to the Main Elevator')
			time.sleep(2)
			start(armory, programs, droids)
	
def recharging(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nThis is the Re-Charge deck where all droids dock
at charging stations to restore power cells. 
There are currently two droids docked.''')
	print('\n[-RECHARGE STATIONS-]\n')
	print('1.) Scan 866 Control Droid')
	print('2.) Scan 444 Enemy Sentinel Droid')
	print('3.) Return to Main Elevator')
	cmdlist = ['1', '2', '3']
	cmd = getcmd(cmdlist)
	if cmd == '1':
		if 'influence' in programs:
			print('\n- SCAN COMPLETE INFLUENCE PROGRAM ALREADY INSTALLED -')
			time.sleep(2)
			recharging(armory, programs, droids)
		else:
			ctrl_droid(programs)
	elif cmd == '2':
		sentinel_droid(armory, programs, droids)
	elif cmd == '3':
			start(armory, programs, droids)

def ctrl_droid(programs, items=['influence']):
	print('\n----------')
	time.sleep(1)
	print('\nscanning.....')
	time.sleep(1)
	print('''\nThe scan indicates the 866 Control Droid 
has a Influence program. You MUST connect to this droid 
with service port and download the program.  
This program will bring Droids under your Command.''')
	if len(items) > 0:
		for item in items:
			print('\n--> %s' % (item))
	cmdlist = ['service port']
	cmd = getcmd(cmdlist)
	if cmd == 'service port':
			programs.append('influence')
			items = ['influence']
			print('\nservice port connected.')
			time.sleep(1)
			print('accessing file..')
			time.sleep(1)
			print('downloading..')
			time.sleep(1)
			print('....')
			time.sleep(1)
			print('\ndownload complete.')
			print('\nYou have the Influence program.')
			time.sleep(2)
			recharging(armory, programs, droids)
			
def sentinel_droid(armory, programs, droids):
	print('\n----------')
	time.sleep(1)
	print('\nscanning.....')
	time.sleep(1)
	print('''\nThe scan has activated the Sentinel Droid's 
Pulse wave device. The pulse wave will shutdown any 
droids on this deck. You MUST abort the sequence.\n''')
	time.sleep(2)
	print('''\n       << STNL444 ABORT PAD >> ''')
	print('''\n  WARNING PULSE WAVE SEQUENCE INITIATED ''')
	print('''\n    PRESS KEY 0, 1, 2, OR 3 TO ABORT ''')
	time.sleep(1)
	code = '%d' % (randint(0,3))
	guess = input('\n[ABORT]> ')
	guesses = 0
	while guess != code and guesses <1:
		print('\n << ABORT KEY INVALID >>')
		time.sleep(1)
		guesses += 1
		guess = input('\n[ABORT]> ')
	if guess == code:
		print('\n----------')
		time.sleep(1)
		print('\n << PULSE WAVE SEQUENCE ABORTED >>')
		time.sleep(2)
		recharging(armory, programs, droids)
	else:
		print('\n....')
		time.sleep(2)
		print('\nPULSE WAVE SEQUENCE COMPLETE')
		time.sleep(1)
		print('\nPULSE WAVE ACTIVE...')
		time.sleep(1)
		print('\nshutdown imminent...')
		time.sleep(1)
		print('CMBT645 offline.')
		time.sleep(1)
		print('Droid terminated.\n')
		time.sleep(1)
		print('- GAME OVER -\n')
		exit(0)
		
def docking(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nThis is the Docking Port where all incoming craft
dock to access the main Cruiser. There is a
Enemy Droid Shuttle currently docked''')
	print('\n[-DOCKING-]')
	print('\n1.) Escape in Enemy Droid Shuttle')
	print('2.) Return to Main Elevator')
	cmdlist = ['1', '2']
	cmd = getcmd(cmdlist)
	if cmd == '1':
		fighter_ship(armory, programs, droids)
	elif cmd == '2':
		nuke_death(armory, programs, droids)
		
def fighter_ship(armory, programs, droids):
	print('\n <<[ ENEMY DROID SHUTTLE ]>>')
	code = '%d%d%d%d%d%d' % (randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9))
	guess = input('\n[STARTUP-CODE]> ')
	guesses = 0
	while guess != code and guess != 'zx4e9q' and guesses <0:
		#print('\n* ACCESS - DENIED *')
		guesses += 1
		guess = input('\n[STARTUP-CODE]> ')
	if guess == code or guess == 'zx4e9q':
		if 'zx4e9q' in programs and 'MEECDT1000' in programs \
and 'droid hack' in programs:
			shuttle_control(armory, programs, droids)
		else:
			print('\nJAY666:> - DROID CHEATING DETECTED GAME OVER -\n')
			time.sleep(2)
			exit(0)
	else:
		nuke_death(armory, programs, droids)
			
def observation(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nThis is the Observation Deck. A small Low Class 
020 Enemy Scouter droid is posted here.
Use a Probe Droid to Disrupt STR020.''')
	print('\n[-OBSERVATION-]')
	print('\n1.) Disrupt the 020 Enemy Scouter Droid')
	print('2.) Retreat to Main Elevator')
	cmdlist = ['1', '2']
	cmd = getcmd(cmdlist)
	if cmd == '1':
		if 'PBE111' in droids and 'influence' in programs:
			print('\nLaunching probe droid...')
			time.sleep(1)
			print('Disruptor active...')
			time.sleep(1)
			print('Targeting STR020...')
			time.sleep(1)
			print('....')
			time.sleep(1)
			print('\nTarget locked...')
			time.sleep(2)
			print('\nTARGET DISRUPTED')
			time.sleep(2)
			scouter(programs)
		else:
			enemyscouter(armory, programs, droids)
	elif cmd == '2':
			time.sleep(2)
			print('''\nThe Enemy Scouter Droid runs a Droid Hack
jamming your motivator rendering you idle.
\nEnemy Combat Droids are inbound.
\nSTR020:> 0011100000001000000011100000''')
			time.sleep(4)
			print('\n.....')
			time.sleep(1)
			print('\nself-destruct sequence initiated...')
			time.sleep(1)
			print('shutdown imminent...')
			time.sleep(1)
			print('\nCMBT645 offline.')
			time.sleep(1)
			print('Droid terminated.')
			print('\n - GAME OVER -\n')
			exit(0)
			
def scouter(programs, items=['droid hack']):
	print('\n----------')
	time.sleep(1)
	print('''\nThe Enemy 020 scouter droid has a Droid Hack
program. You MUST connect to this droid with 
service port and download the program.''')
	if len(items) > 0:
		for item in items:
			print('\n--> %s' % (item))
	cmdlist = ['service port']
	cmd = getcmd(cmdlist)
	if cmd == 'service port':
			programs.append('droid hack')
			items = ['droid hack']
			print('\nservice port connected.')
			time.sleep(1)
			print('accessing file..')
			time.sleep(1)
			print('downloading..')
			time.sleep(1)
			print('....')
			time.sleep(1)
			print('\ndownload complete.')
			time.sleep(1)
			print('\nYou have the Droid Hack program.')
			print('and return to the Main Elevator.')
			time.sleep(2)
			start(armory, programs, droids)
			
def droid_hangar(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nThe Droid hangar is Where all inactive droids
are docked. Enemy Droids have terminated all units. 
The Hangar has Laser scoring everywhere.
\nThere are Two Combat Droids that are still incased in  
in a security cylinder. You MUST influence these Droids
but you will need a 5 digit access code to initalize.\n''')
	print('[-DROID HANGAR-]')
	print('\n1.) Combat Droids 5 digit code')
	print('2.) Return to Main Elevator')
	cmdlist = ['1', '2']
	cmd = getcmd(cmdlist)
	if cmd == '1':
		access_code(armory, programs, droids)
	elif cmd == '2':
		start(armory, programs, droids)
		
def access_code(armory, programs, droids):
	print('\n <SECURITY CYLINDER>')
	print('\n[-CMBT646 - CMBT647-]')
	code = '%d%d%d%d%d' % (randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9))
	guess = input('\n[KEYPAD]> ')
	guesses = 0
	while guess != code and guess != 'zx71vbq' and guesses <2:
		print('\n* ACCESS - DENIED *')
		guesses += 1
		guess = input('\n[KEYPAD]> ')
	if guess == code or guess == 'zx71vbq':
		combat_droids(armory, programs, droids)
	else:
		print('\n....')
		time.sleep(1)
		print('\nKEYPAD - LOCKED')
		time.sleep(1)
		print('\ncode randomizing..')
		time.sleep(1)
		print('\nKEYPAD - OPEN')
		time.sleep(1)
		droid_hangar(armory, programs, droids)
		
def cargo_hold(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nThis is the cargo hold where all supplies are kept.
There is a small Droid flying around scanning crates.
It is a Probe Droid and is also armed with a disruptor.''')
	print('\n[-CARGO HOLD-]\n')
	print('1.) Probe Droid 111')
	print('2.) Return to Main Elevator\n')
	cmdlist = ['1', '2']
	cmd = getcmd(cmdlist)
	if cmd == '1':
		probe_droid(droids)
	elif cmd == '2':
		start(armory, programs, droids)
		
def probe_droid(droids, items=['PBE111']):
	print('\n----------')
	time.sleep(1)
	print('''\nThe Probe Droid is flying within range. You
MUST bring this droid under your command 
with a influence program.  \n\n\t\t- or type exit to leave.''')
	if len(items) > 0:
		for item in items:
			print('\n--> %s' % (item))
	cmdlist = ['influence', 'exit']
	cmd = getcmd(cmdlist)
	if cmd == 'influence' and 'influence' in programs:
			droids.append('PBE111')
			items = ['PBE111']
			print('\nloading influence...')
			time.sleep(1)
			print('influencing...')
			time.sleep(1)
			print('....')
			time.sleep(1)
			print('\nPBE111 DROID INFLUENCED')
			time.sleep(2)
			print('\nYou now have PBE111 under your command')
			print('you return to Main Elevator')
			time.sleep(2)
			start(armory, programs, droids)
	elif cmd == 'exit':
			start(armory, programs, droids)
	else:
		print('\n- INFLUENCE PROGRAM NOT DETECTED -')
		time.sleep(2)
		cargo_hold(armory, programs, droids)
		
def power_core(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nYou enter the Power Core deck. The
power core generates power for the Cruiser.
\nRepair Droid 377 was here doing maintenance 
on the Core Chamber but has been terminated.  
You MUST hack the Repair droid and download 
the twin laser repair program.''')
	print('\n[-POWER CORE CHAMBER-]\n')
	print('1.) Hack Repair Droid 377')
	print('2.) Return to Main Elevator')
	cmdlist =['1', '2']
	cmd = getcmd(cmdlist)
	if cmd == '1':
		if 'droid hack' in programs:
			repair_droid(armory, items=['twin laser'])
		else:
			print('\n- DROID HACK PROGRAM NOT DETECTED -')
			time.sleep(2)
			power_core(armory, programs, droids)
	elif cmd == '2':
			start(armory, programs, droids)
		
def repair_droid(armory, items=['twin laser']):
	print('\n----------')
	time.sleep(1)
	print('\nloading droid hack....')
	time.sleep(2)
	print('....')
	time.sleep(2)
	print('10000101010101010101010' * 1000)
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('Accessing encrypted files...')
	time.sleep(2)
	print('Decrypting....')
	time.sleep(1)
	print('\n\n[-REP377-]')
	print('''\n\nDownload the twin laser repair
program with service port.''')
	if len(items) > 0:
		for item in items:
			print('\n--> %s' % (item))
	cmdlist = ['service port']
	cmd = getcmd(cmdlist)
	if cmd == 'service port':
			armory.append('twin laser')
			items = ['twin laser']
			print('\nservice port connected.')
			time.sleep(1)
			print('accessing file..')
			time.sleep(1)
			print('downloading..')
			time.sleep(1)
			print('....')
			time.sleep(1)
			print('\ndownload complete.')
			time.sleep(1)
			print('Repairing twin Laser...')
			time.sleep(1)
			print('Auto alignment...')
			time.sleep(1)
			print('....')
			time.sleep(1)
			print('\nTWIN LASER ONLINE.')
			time.sleep(2)
			print('''\nYour twin laser is now online.
You return to the Main Elevator.''')
			time.sleep(2)
			start(armory, programs, droids)
			
def droid_software(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nYou enter the Droid Software Deck. This deck
is where droids connect to the main terminal and download
Software.  You will need a Droid class secure code
to gain access to the system.''')
	print('\n\n[-DROID SOFTWARE SYSTEM-]')
	print('\n  [ - MAIN TERMINAL - ]')
	time.sleep(1)
	print('\n\n..service port connected.')
	time.sleep(1)
	print('\nenter secure code  -or type exit to leave')
	cmdlist =['w7md3sx', 'exit', 'console hack']
	cmd = getcmd(cmdlist)
	if cmd == 'w7md3sx':
		if 'console hack' in programs and 'droid hack' in programs \
and 'influence' in programs and 'PBE111' in droids:
			print('\n----------')
			time.sleep(1)
			print('\n - COMBAT DROID SECURE CODE VERIFIED -')
			time.sleep(2)
			software_download(armory)
		else:
			print('\n...')
			time.sleep(1)
			print('\nJAY666:> are you cheating ? ')
			time.sleep(3)
			droid_software(armory, programs, droids)
	elif cmd == 'exit':
		print('\n....')
		time.sleep(1)
		print('\nservice port disconnected.')
		time.sleep(1)
		start(armory, programs, droids)
	elif cmd == 'console hack':
		print('....')
		time.sleep(1)
		print('\n - MAIN TERMINAL SECURE -')
		time.sleep(2)
		droid_software(armory, programs, droids)
		
def software_download(armory, items=['motion tracker', 'disruptor']):
	print('''\nThere are two Weapon Repair programs 
which you MUST download with service port.''')
	if len(items) > 0:
		for item in items:
			print('\n--> %s' % (item))
		cmdlist = ['service port']
		cmd = getcmd(cmdlist)
	if cmd == 'service port':
		armory.append('motion tracker')
		armory.append('disruptor')
		items = ['motion tracker', 'disruptor']
		print('\nservice port connected.')
		time.sleep(1)
		print('accessing files..')
		time.sleep(1)
		print('downloading..')
		time.sleep(1)
		print('....')
		time.sleep(1)
		print('\ndownload complete.')
		time.sleep(1)
		print('\nRepairing motion tracker...')
		time.sleep(1)
		print('Repairing disruptor...')
		time.sleep(1)
		print('Auto alignment...')
		time.sleep(1)
		print('....')
		time.sleep(1)
		print('\nMOTION TRACKER ONLINE.')
		time.sleep(1)
		print('\nDISRUPTOR ONLINE.')
		time.sleep(2)
		print('''\nYour motion tracker and disruptor
are now online. You return to the Main Elevator.''')
		start(armory, programs, droids)
	elif cmd == 'exit':
		start(armory, programs, droids)
		
def combat_droids(armory, programs, droids):
	time.sleep(1)
	print('\n\n - ACCESS CODE GRANTED -')
	print('\n<< Security Cylinder Open >>')
	time.sleep(2)
	print('\n....')
	time.sleep(1)
	print('\nCMBT646 boot sequence....')
	time.sleep(1)
	print('\nInitalizing Combat Droid 646....')
	time.sleep(1)
	print('\n....')
	time.sleep(1)
	print('\nCMBT646 ONLINE.')
	time.sleep(2)
	print('\n....')
	time.sleep(1)
	print('\nCMBT647 boot sequence....')
	time.sleep(1)
	print('\nInitalizing Combat Droid 647....')
	time.sleep(1)
	print('\n....')
	time.sleep(1)
	print('\nCMBT647 ONLINE.')
	time.sleep(2)
	combat_influence(armory, programs, droids)
	
def combat_influence(armory, programs, droids, items=['CMBT646', 'CMBT647']):
	print('\n----------')
	time.sleep(1)
	print('''\nThe Combat droids have now been initialized.
you MUST use the influence program 
to bring these Droids under your Command.''')
	if len(items) > 0:
		for item in items:
			print('\n--> %s' % (item))
	cmdlist = ['influence']
	cmd = getcmd(cmdlist)
	if cmd == 'influence' and 'influence' in programs:
			droids.append('CMBT646')
			droids.append('CMBT647')
			items = ['CMBT646', 'CMBT647']
			print('\nloading influence...')
			time.sleep(1)
			print('influencing...')
			time.sleep(1)
			print('....')
			time.sleep(1)
			print('\nCMBT646 DROID INFLUENCED')
			time.sleep(2)
			print('\ninfluencing...')
			time.sleep(1)
			print('....')
			time.sleep(1)
			print('\nCMBT647 DROID INFLUENCED')
			time.sleep(2)
			print('''\nYou now have Both Combat Droids under 
your command. You return to Main Elevator''')
			time.sleep(2)
			start(armory, programs, droids)
	else:
			print('\nJAY666:> - DROID CHEATING DETECTED GAME OVER -\n')
			time.sleep(2)
			exit(0)
			
def cruiser_control(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nYou enter Cruiser Control where all navigation takes place.
A T1000 Master Elite Enemy Command Droid is posted here..
Exercise caution this Droid is extremely powerfull and
has not been encountered before.''')
	print('\n[-CRUISER CONTROL-]')
	print('\n1.) Terminate the T1000 Master Elite Enemy Command Droid')
	print('2.) Retreat to Main Elevator')
	cmdlist = ['1', '2']
	cmd = getcmd(cmdlist)
	if cmd == '1':
		if 'droid hack' in programs and 'influence' in programs \
and 'PBE111' in droids and 'CMBT646' in droids and 'CMBT647' in droids \
and 'twin laser' in armory and 'disruptor' in armory \
and 'motion tracker' in armory and 'console hack' in programs:
			command_droid_battle(armory, programs, droids)
		else:
			time.sleep(1)
			print('\nMEECDT1000:>')
			print('\n100101010101010101010101010101010' * 10)
			time.sleep(1)
			print('''\nThe Master Elite Enemy Command Droid 
laughs in machine language at your pathetic attempt. 
The last thing your data recorder recieves is 
the sound of a Target Lock.''')
			print('....')
			time.sleep(1)
			print('..')
			time.sleep(1)
			print('\nshutdown imminent...')
			time.sleep(1)
			print('CMBT645 offline.')
			time.sleep(1)
			print('Droid terminated.')
			print('\n- GAME OVER -\n')
			exit(0)
	elif cmd == '2':
		start(armory, programs, droids)
		
def command_droid_battle(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('......')
	time.sleep(1)
	print('\nCOMBAT DROIDS ACTIVE >>')
	time.sleep(1)
	print('\nCMBT646 ENGAGING MEECDT1000')
	time.sleep(1)
	print('\nCMBT647 ENGAGING MEECDT1000')
	time.sleep(1)
	print('\n......')
	print('\n - MEECDT1000 DAMAGE STATUS AT 40 PER CENT -')
	time.sleep(3)
	print('\n\nPROBE DROID ACTIVE >> ')
	time.sleep(1)
	print('\nPBE111 ENGAGING MEECDT100')
	time.sleep(1)
	print('\n......')
	print('\n - MEECDT1000 DAMAGE STATUS AT 50 PER CENT -')
	time.sleep(3)
	print('\n\nRunning droid hack...')
	time.sleep(1)
	print('\njamming MEECDT1000 Target Lock...')
	time.sleep(1)
	print('\n......')
	time.sleep(1)
	print('\nMotion Tracker active...')
	time.sleep(1)
	print('\nTrack motion of MEECDT1000...')
	time.sleep(1)
	print('\n......')
	time.sleep(1)
	print('\nDisruptor active...')
	time.sleep(1)
	print('\nDisrupting MEECDT1000...')
	time.sleep(1)
	print('\n......')
	time.sleep(1)
	print('\nTwin laser active...')
	time.sleep(1)
	print('\nTargeting MEECDT1000...')
	time.sleep(1)
	print('\nTarget lock failed...')
	time.sleep(1)
	print('\n......')
	time.sleep(2)
	print('\n\nTARGET DISRUPTED \n')
	time.sleep(2)
	command_droid(armory, programs, droids)
	
def command_droid(armory, programs, droids):
	print('\n----------')
	print('\nDroid mobile..')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('''\nYou have disrupted the Master Elite Enemy Command Droid.
This high rank Droid must have important files in memory.
\nMEECDT1000 has sustained severe disruptor damage.
You MUST try access the files...''')
	print('\n\n[- MEECDT1000 -]')
	cmdlist = ['droid hack']
	cmd = getcmd(cmdlist)
	if cmd == 'droid hack':
		ship_code(armory, programs, droids)
		
def ship_code(armory, programs, droids, items=['zx4e9q', 'MEECDT1000']):
	print('\n----------')
	time.sleep(1)
	print('\nloading droid hack....')
	time.sleep(2)
	print('....')
	time.sleep(2)
	print('10000101010101010101010' * 1000)
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('Accessing encrypted files...')
	time.sleep(2)
	print('Decrypting....')
	time.sleep(1)
	print('\n\n[- MEECDT1000 -]')
	print('''\n\nThe Secure files contain
a startup code for a Enemy Droid Shuttle 
and the MEECDT1000 Droid Specs.
You MUST download these files with service port.''')
	if len(items) > 0:
		for item in items:
			print('\n--> %s' % (item))
	cmdlist = ['service port']
	cmd = getcmd(cmdlist)
	if cmd == 'service port':
			programs.append('zx4e9q')
			programs.append('MEECDT1000')
			items = ['zx4e9q', 'MEECDT1000']
			print('\nservice port connected.')
			time.sleep(1)
			print('accessing files..')
			time.sleep(1)
			print('downloading..')
			time.sleep(1)
			print('....')
			time.sleep(1)
			print('\ndownload complete.')
			time.sleep(2)
			print('\n.....')
			time.sleep(2)
			print('\n\n <<< WARNING NUKE ACTIVE >>>')
			time.sleep(2)
			print('\n DETONATION SEQUENCE INITIATED')
			time.sleep(2)
			print('\n\nMEECDT1000:> 0011100000001000000011100000 ')
			time.sleep(2)
			print('''\n\nDownloading the Droid Specs has 
activated a Droid Nuke inside MEECDT1000. 
\nThe Nuke will Obliterate the Cruiser
\nYou MUST escape the PROXY ....''')
			time.sleep(4)
			start(armory, programs, droids)
			
def shuttle_control(armory, programs, droids):
	time.sleep(1)
	print('\n\n<< START-UP CODE VERIFIED >>')
	time.sleep(2)
	print('\n>>')
	time.sleep(1)
	print('\nHyperdrive active..')
	time.sleep(1)
	print('Hyperspace coordinates locked.')
	time.sleep(1)
	print('\nDestination: phaze beta system.\n')
	time.sleep(2)
	print('\nHYPERSPACE JUMP SEQUENCE INITIATED >>\n')
	time.sleep(4)
	print('\n>>')
	time.sleep(1)
	print('''\nYou have escaped the PROXY and made
a Hyperspace jump to Droid Command.
\nThe specs you obtained on the rare 
MEECDT1000 droid are priceless. Production of 
these Droids will Commence at once.''')
	time.sleep(1)
	print('\n - GAME OVER -\n')
	exit(0)

def nuke_death(armory, programs, droids):
	print('\n....')
	time.sleep(2)
	print('\n << DROID NUKE DETONATION SEQUENCE COMPLETE >>')
	time.sleep(4)
	print('\n....')
	time.sleep(1)
	print('''\nThe PROXY is now space debri..
You failed to escape.''')
	time.sleep(2)
	print('\nCMBT645 offline.')
	time.sleep(1)
	print('Droid terminated.\n')
	time.sleep(1)
	print('- GAME OVER -\n')
	exit(0)
	
def enemyscouter(armory, programs, droids):
	print('\n- WARNING NO PROBE DROID IN YOUR COMMAND -')
	time.sleep(2)
	print('''\nThe Enemy Scouter Droid runs a Droid Hack
jamming your motivator rendering you idle.
\nEnemy Combat Droids are inbound.
\nSTR020:> 0011100000001000000011100000''')
	time.sleep(4)
	print('\n.....')
	time.sleep(1)
	print('\nself-destruct sequence initiated...')
	time.sleep(1)
	print('shutdown imminent...')
	time.sleep(1)
	print('\nCMBT645 offline.')
	time.sleep(1)
	print('Droid terminated.')
	print('\n - GAME OVER -\n')
	exit(0)
	
def enemysen(armory, programs, droids):
	print('\n- WARNING TWIN LASER OFFLINE -')
	time.sleep(2)
	print('\nEnemy Sentry Droid 771 has you Locked on.')
	time.sleep(1)
	print('\nSEN771:> 0011100000001000000011100000')
	time.sleep(1)
	print('\n....')
	time.sleep(1)
	print('\nShutdown imminent...')
	time.sleep(1)
	print('CMBT645 offline.')
	time.sleep(1)
	print('Droid terminated.')
	print('\n- GAME OVER -\n')
	exit(0)

def getcmd(cmdlist):
	cmd = input('\nCMBT645:> ')
	if cmd in cmdlist:
		return cmd
	elif cmd == 'help':
		print('\nTYPE: armory   - to view weapons online')
		print('      programs - to view software installed')
		print('      droids   - to see in your command')
		print('      quit     - to self destruct')
		return getcmd(cmdlist)
	elif cmd == 'armory':
		print('\nWeapons online:\n')
		for weapon in armory:
			print('-- %s' % (weapon))
		return getcmd(cmdlist)
	elif cmd == 'programs':
		print("\nSoftware installed:\n")
		for program in programs:
			print('-- %s' % (program))
		return getcmd(cmdlist)
	elif cmd == 'droids':
		print('\nDroids in command:\n')
		for droid in droids:
			print('-- %s' % (droid))
		return getcmd(cmdlist)
	elif cmd == 'cheat':
		print('\nJAY666:> DROID CHEATING DENIED ')
		time.sleep(2)
		return getcmd(cmdlist)
	elif cmd == 'quit':
		print('\n----------')
		time.sleep(1)
		print('\nself-destruct sequence initiated...')
		time.sleep(1)
		print('shutdown imminent...')
		time.sleep(1)
		print('\nCMBT645 offline.')
		time.sleep(1)
		print('Droid terminated.\n')
		exit(0)
	else:
		print('\n   error. invalid command-\n')
		return getcmd(cmdlist)

if __name__ == "__main__":
	armory = ['service port']
	programs = []
	droids = []
	start(armory, programs, droids)
