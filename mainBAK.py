#import RPi.GPIO as GPIO
import hashlib
import time
import getpass

localTime = time.asctime(time.localtime(time.time()))
timeout = time.time() + 10

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#####Green Light#####
#GPIO.setup(11, GPIO.OUT)
#GPIO.output(11, True)
#####Red Light#####
#GPIO.setup(13, GPIO.OUT)
#####Blue Light####
#GPIO.setup(15, GPIO.OUT)

######Reads the database file so it can be authenticated in the program
def readDB():
	DB = []
	f = open("hashDB.txt","r")
	while True:
		AUTH = f.readline()
		AUTH = AUTH.strip()
		AUTH = AUTH.split(":")[0]

		DB.append(AUTH)
		if len(AUTH) == 0:
			f.close()
			break
	DB = filter(None, DB)
	#print(DB)
	return DB

######Reads the admin database to lookfor any admin cards
def readADB():
	adminDB = []
	f = open("HashAdminDB.txt","r")
	while True:
		admin = f.readline()
		admin = admin.strip()
		admin = admin.split(":")[0]
		adminDB.append(admin)

		if len(admin) == 0:
			f.close()
			break
	adminDB = filter(None, adminDB)
	return adminDB

#readDB()
#####Allows for this function to be called when the LEDs wanted to be flashed
def flash(x):
		#GPIO.output(11, True)
		#GPIO.output(13, True)
		time.sleep(x)
		#GPIO.output(11, False)
		#GPIO.output(13, False)

######Main loop for the program
while True:
	#GPIO.output(11, True)
	#readDB()
	###Reads input from the card reader
	#rawCard = getpass.getpass("Swipe Card: ")
	rawCard = getpass.getpass("Swipe Card: ")
	formCard = rawCard[1:8]		###Formats the string to remove extra junk

	formCard = hashlib.md5(formCard.encode())
	formCard = formCard.hexdigest()

	if formCard in readDB():   ##Checks to see if the card is on the allowed DB
		print("Access")    ##Debug
##################################################
##Logs the Entry
		with open('log.txt','a') as log:
			log.write("%s:Access:%s\n" % (formCard, localTime))
			log.write("")
			log.close()
		#####Green LED lights up to show that the userhas been granted access
		#GPIO.output(11, False)
		#time.sleep(3)
		#GPIO.output(11, True)


	elif formCard in readADB(): ##Checks if the card is on the adminDB for admin mode
		while True:
			#Add timeout incase admin mode is left
			######Turns on the BLUE light to show that the reader is in admin mode
			#GPIO.output(15, True)
			print("#####Admin Mode#####")
			##Swipe card 3 times incase a bad swipe

			swipe1 = getpass.getpass("Swipe Card01: ")
			swipe1 = swipe1[1:8]

			swipe2 = getpass.getpass("Swipe Card02: ")
			swipe2 = swipe2[1:8]

			swipe3 = getpass.getpass("Swipe Card03: ")
			swipe3 = swipe3[1:8]

			if swipe1 == swipe2 == swipe3:
				print("Card read: ", swipe3)	#Debug
#################################################
													###If either of these conditions are met
				if swipe3 in readDB():				###The program leaves admin mode
					print("Card already on database")
					#GPIO.output(15, False)

				elif swipe3 in readADB():
					print("Card is on the admin database")
#################################################

				else:
					####Flash green and red LED to show the card was properly read
					flash(1)
					###Adds the card to the DB
					with open('hashDB.txt','a') as db:
						swipe3 = hashlib.md5(swipe3.encode())
						swipe3 = swipe3.hexdigest()

						db.write("%s:\n" % swipe3)
						#n = input("Input Name: ")
						#db.write("%s\n" % n)
						db.close()

					###Log saying the card was added
					with open('log.txt','a') as log:
						log.write("%s:added to the DB:%s\n" % (swipe3, localTime))
						log.close()

					##Turn off admin mode
					#GPIO.output(15, False)
				break
			else:
				continue

	else:
		print("Denied")

		with open('log.txt','a') as log:
			log.write("%s:Denied:%s\n" % (formCard, localTime))
			log.write("")
			log.close()

		#####Lights up a RED light to show the user has a bad swipe
		#GPIO.output(13, True)
		#time.sleep(1)
		#GPIO.output(13, False)
