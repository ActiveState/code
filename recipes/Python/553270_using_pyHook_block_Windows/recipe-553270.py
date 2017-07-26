import pyHook
import pygame

# create a keyboard hook
def OnKeyboardEvent(event):
	print 'MessageName:',event.MessageName
	print 'Message:',event.Message
	print 'Time:',event.Time
	print 'Window:',event.Window
	print 'WindowName:',event.WindowName
	print 'Ascii:', event.Ascii, chr(event.Ascii)
	print 'Key:', event.Key
	print 'KeyID:', event.KeyID
	print 'ScanCode:', event.ScanCode
	print 'Extended:', event.Extended
	print 'Injected:', event.Injected
	print 'Alt', event.Alt
	print 'Transition', event.Transition
	print '---'
	if event.Key.lower() in ['lwin', 'tab', 'lmenu']:
		return False	# block these keys
	else:
		# return True to pass the event to other handlers
		return True

# create a hook manager
hm = pyHook.HookManager()
# watch for all keyboard events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()

# initialize pygame and start the game loop
pygame.init()

while(1):
	pygame.event.pump()
