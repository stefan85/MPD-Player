from mpd import MPDClient
from time import sleep
import RPi.GPIO as GPIO
import sys

def FolderToPlaylist(foldername):
	client.clear()
	for filename in client.lsinfo(foldername):
		print "Adding: " + filename["file"]
		client.add(filename["file"])
	print(client.playlist())

def StartPlaying():
	client.play() # play the playlist
	print "play"
	#print client.status()
 
def Next():

	if (int(client.status()['song']) < int((client.status()['playlistlength']))-1): #check if there is a next song
		print "Next song"
		client.next()
	else:
		print "Fail: No next song"

def Previous():

	if (int(client.status()['song']) > 0): #check if there is a next song
		print "Previous song"
		client.previous()
	else:
		print "Fiil: No previous song"	

def PlayButtonFunction(channel):
	print "Play button is pressed"

def NextButtonFunction(channel):
	print "Next button is pressed"
	Next()

def PreviousButtonFunction(channel):
	print "Previous button is pressed"
	Previous()
	
def SetupGPIO():
	GPIO.setmode(GPIO.BCM)
	#GPIO.setup(23, GPIO.OUT)
	GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)	#Play button
	GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)	#Play button
	GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)	#Play button
	
	GPIO.add_event_detect(18, GPIO.FALLING, callback=PlayButtonFunction, bouncetime=300)
	GPIO.add_event_detect(23, GPIO.FALLING, callback=NextButtonFunction, bouncetime=300)
	GPIO.add_event_detect(24, GPIO.FALLING, callback=PreviousButtonFunction, bouncetime=300)


	
client = MPDClient() # instantiate the client object
client.connect(host="localhost", port=6600) # connect to the mpd daemon
client.clear()
client.update() # update the mpd database with the files in our books folder





def main(argv):
	SetupGPIO()
	
	#GPIO.output(23, True)
	FolderToPlaylist("21")
	StartPlaying()

	sleep(60)
	#GPIO.output(23, False)
	
	client.stop()
	
	while(True):
		print"test"
		sleep(5)
	pass

if __name__ == "__main__":
    main(sys.argv)