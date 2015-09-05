from objects import *
from scoring import *

def StartNew(n):
	Game(n).new_game()

def StartFromFile():
	if os.path.isfile("saved.p"):
		f = open("saved.p", "rb")
		g = pickle.load(f)
		g.play_game()
		f.close
	else:
		print("\n\nERROR: No Game File Found")

def ViewHiScores():
	print("\n\n")
	if os.path.isfile("scores.p"):
			f = open("scores.p", "rb")
			scorekeeper = pickle.load(f)
			scorekeeper.disp_scores()
			f.close
	else:
		print("ERROR: No Score File Found")
	print("\n\n")
	pause()

def pause():
	input("Press any key to continue: ")

if __name__ == "__main__":
	while 1:
		f = open("info.txt", "r")
		print(f.read())
		f.close
		command = input("N S V X: ")
		if command.lower() not in "nsvx":
			print("INVALID COMMAND PLEASE TRY AGAIN")
			pause()
		else:
			if command.lower() == "n": 
				n = input("What size board?  ")
				if n in '1023456789':
					StartNew(int(n))
				else: print("Invalid number entered, please try again")
			elif command.lower() == "s":
				StartFromFile()
			elif command.lower() == "v":
				ViewHiScores()
			else:
				break