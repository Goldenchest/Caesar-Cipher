# CIPHER TYPING GAME
import string
import random
import time
from Tkinter import *

fileName = "words.txt"

class Cipher(object):
	# load words from text file
	punct = string.punctuation # string of punctuation symbols
	digits = '0123456789' # string of digits
	def __init__(self):
		file = open(fileName, 'r') # open text file of words
		wordList = file.read().split() # create a list of every word
		file.close() # close file
		self.wordList = wordList # make wordList a class variable
		
	# test if a word is valid or not
	def isWord(self, word):
		word = word.lower() # words in text file are lowercase
		word = word.strip(" z!@#$%^&*()-_+={}[]|\\:;'<>?,./\"") # remove extraneous characters from word
		return (word in self.wordList) # return True if word is in wordList, False otherwise
	def getRandomWord(self):
		word = random.choice(self.wordList)
		while len(word)<4:
			word = random.choice(self.wordList)
		return word
	
class Caesar(Cipher):
	def __init__(self):
		super(Caesar,self).__init__() # initialize Cipher class (load words)		
	# map shifted letters to corresponding letters in alphabet
	def buildCoder(self, shift):
		lower = 'abcdefghijklmnopqrstuvwxyz'*2 # multiplied by 2 so shift may loop back to beginning of alphabet
		upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'*2 # uppercase alphabet
		dictionary = {}
		for i in range(len(upper) - shift): # for each index in the uppercase alphabet, minus shift value
			dictionary[upper[i]] = upper[i+shift] # map shifted letters to their corresponding letters
		for i in range(len(lower) - shift): # for each index in the lowercase alphabet, minus shift value
			dictionary[lower[i]] = lower[i+shift]
		return dictionary
	# shift every letter of a string: takes in a string and a dictionary of mapped letters
	def applyCoder(self, string, mappedLetters):
		newString = ''
		for letter in string: # for each letter in inputted string:
			# if the letter is valid:
			if letter not in Cipher.punct and letter not in Cipher.digits and letter != ' ':
				newString += mappedLetters[letter] # add shifted letter to newString
			elif letter in Cipher.punct or letter in Cipher.digits: # if letter is a punctuation or a number:
				newString += letter # add the punctuation and number to the string
		return newString # return the processed string
	# apply the encryption for an inputted shift value
	def applyShift(self, string, shift):
		return self.applyCoder(string, self.buildCoder(shift))
	# find the best shift to decipher a Caeser cipher
	def findBestShift(self, string):
		#punct = string.punctuation # string of punctuation symbols
		counter = 0 # count the number of valid words found
		shift = 0 # start with a shift of zero and increment
		numWords = 0 # variable to temporarily store the current counter value before changing counter
		text = string.split(' ') # text is a list of inputted words
		for key in range(26): # for each key less than 26:
			counter = 0 # reset counter
			for word in text: # for each word in text:
				word = self.applyShift(word,key) # apply  shift with current key
				filteredWord = '' # string to hold filtered text
				for letter in word: # for each letter in the word:
					if letter not in Cipher.punct: # if letter is not a punctuation:
						filteredWord += letter # add letter to newWord
				if self.isWord(filteredWord): # if word is valid:
					counter += 1 # increment the counter
			if (counter > numWords): # if more words were found than for previous shift value:
				numWords = counter # set numWords as current counter value
				shift = key # optimal shift is now current key value
		return shift # return the shift value that found the most words
	# decode a message
	def decode(self, message):
		shift = self.findBestShift(message) # find the best shift for the message
		return self.applyShift(message,shift) # apply the shift and return the decoded message

#####################################################################################################
# Tkinter code
class Buttons(object):
	textFieldActive = False
	def __init__(self, left_x, top_y, label, color, width=150, height=35):
		self.left_x = left_x
		self.top_y = top_y
		self.width = width
		self.height = height
		self.color = color
		self.label = label
		self.displayButton()
	def displayButton(self):
		canvas.create_rectangle(self.left_x, self.top_y, self.left_x+self.width, self.top_y+self.height, fill=self.color)
		canvas.create_text(self.left_x+self.width/2, self.top_y+self.height/2, text=self.label, fill="black", font="calibri")
	def inButton(self, x, y):
		return x > (self.left_x) and x < (self.left_x+self.width) and\
			   y > (self.top_y) and y < (self.top_y+self.height)
	def getX(self):
		return self.left_x
	def getY(self):
		return self.top_y
	def getWidth(self):
		return self.width
	def getHeight(self):
		return self.height
class TextField(Buttons):
	def __init__(self, left_x, top_y, label="", color = "white", width=700, height = 50):
		super(TextField,self).__init__(left_x, top_y, label, color, width, height)
	def activateButton(self):
		canvas.currentTextField = self
		Buttons.textFieldActive = True
		self.color = "white"
		self.displayButton()
	def correctAnswer(self):
		self.color = "green2"
		self.displayButton()
class MainMenuButton(Buttons):
	def __init__(self, left_x=10, top_y=10, label="Main Menu", color="cyan"):
		super(MainMenuButton,self).__init__(left_x, top_y, label, color)
	def activateButton(self):
		canvas.gameState = "menu"
		drawGame()

class StartGameButton(Buttons):
	def __init__(self, left_x=150, top_y=450, label="Start Game", color="green"):
		super(StartGameButton,self).__init__(left_x, top_y, label, color)
	def activateButton(self):
		canvas.gameState = "game"
		drawGame()
class HelpButton(Buttons):
	def __init__(self, left_x=600, top_y=450, label="How To Play", color="grey"):
		super(HelpButton,self).__init__(left_x, top_y, label, color)
	def activateButton(self):
		canvas.gameState = "help"
		drawGame()
class CipherButton(Buttons):
	def __init__(self, left_x=325, top_y=450, label="Bonus Feature: Cipher Translator", color="red"):
		super(CipherButton,self).__init__(left_x, top_y, label, color, width=250)
	def activateButton(self):
		canvas.gameState = "cipher"
		drawGame()
class TranslateButton(Buttons):
	def __init__(self, left_x=500-75, top_y=160, label="Translate", color = "green"):
		super(TranslateButton,self).__init__(left_x, top_y, label, color)
	def activateButton(self):
		canvas.cipherState = "translate"
		self.printButtonStatus()
	def printButtonStatus(self):
		#print "printing"
		canvas.create_text(canvas.width/2, 400, text="Mode: Translating", fill="blue", font="calibri 20")
		#drawGame()
class EncryptButton(Buttons):
	def __init__(self, left_x=500-75, top_y=210, label="Encrypt...", color = "orange"):
		super(EncryptButton,self).__init__(left_x, top_y, label, color)
	def activateButton(self):
		canvas.cipherState = "encrypt"
		self.printButtonStatus()
	def printButtonStatus(self):
		canvas.create_text(canvas.width/2, 400, text="Mode: Encrypting", fill="blue", font="calibri 20")
class KeyButton(Buttons):
	def __init__(self, left_x, top_y, label, color = "grey", width=30, height=30):
		super(KeyButton,self).__init__(left_x, top_y, label, color = "grey", width=30, height=30)
		self.isActive = False
	def activateButton(self):
		canvas.key = int(self.label)
		self.color = "green"
		self.displayButton()
		self.isActive = True
	def deactivateButton(self):
		self.color = "grey"
		self.displayButton()
		self.isActive = False
	def isActive(self):
		return self.isActive
def printText(message, x, y):
	drawGame()
	canvas.create_text(x, y, text=message, fill="black", font="calibri 28")
def typeInTextField(textField, text):
	try:
		printText(canvas.text, textField.getX()+textField.getWidth()/2, textField.getY()+textField.getHeight()/2)
	except:
		pass
def inputText(event):
	if canvas.gameState in ['game', 'cipher']:
		canvas.text += event.char
		typeInTextField(canvas.currentTextField, canvas.text)
def callBackSpace(event):
	canvas.text = canvas.text[:-1]
	typeInTextField(canvas.currentTextField, canvas.text)
def printSpace(event):
	canvas.text += ' '
	typeInTextField(canvas.currentTextField, canvas.text)
def nullFunction(event):
	pass
def checkButtons(buttonsList, x, y):
	for button in buttonsList:
		if button.inButton(x,y):
			if button == canvas.mainMenuButton:
				getNextWord()
				canvas.typingEnabled = True
				canvas.currentLevel = 1
			if button == canvas.startGameButton:
				canvas.secondsCounter = 0
				canvas.startTime = time.clock()
				canvas.typingEnabled = False
			if button == canvas.cipherButton:
				canvas.cipherState = "encrypt"
				canvas.keyButtons[0].activateButton()
			if button in canvas.keyButtons:
				for keyButton in canvas.keyButtons:
					if keyButton != button:
						keyButton.deactivateButton()
			button.activateButton()
def checkTextFields(textFieldList, x, y):
	canvas.typingEnabled = True
	for textField in textFieldList:
		if textField.inButton(x,y):
			textField.activateButton()
			canvas.typingEnabled = True
		if not textField.inButton(x,y):
			textField.activateButton()
			canvas.text = ''
def clickButton(event):
	canvas.text = ''
	if canvas.gameState == "menu":
		checkButtons(canvas.menuButtons, event.x, event.y)
	elif canvas.gameState == "game":
		checkTextFields(canvas.gameTextFields, event.x, event.y)
		checkButtons(canvas.gameButtons, event.x, event.y)
	elif canvas.gameState == "help":
		checkButtons(canvas.helpButtons, event.x, event.y)
	elif canvas.gameState == "cipher":
		checkTextFields(canvas.cipherTextFields, event.x, event.y)
		checkButtons(canvas.cipherButtons, event.x, event.y)
		checkButtons(canvas.keyButtons, event.x, event.y)
	elif canvas.gameState == "score":
		checkButtons(canvas.scoreButtons, event.x, event.y)
	drawGame()

def initButtons():
	canvas.mainMenuButton = MainMenuButton()
	canvas.startGameButton = StartGameButton()
	canvas.helpButton = HelpButton()
	canvas.cipherButton = CipherButton()
	canvas.translateButton = TranslateButton()
	canvas.encryptButton = EncryptButton()
	leftPad = 120
	#canvas.key1=KeyButton(leftPad,100,'1');canvas.key2=KeyButton(leftPad+30,100,'2');canvas.key3=KeyButton(leftPad+30*2,100,'3')
	canvas.keyButtons = {}
	for key in range(26):
		canvas.keyButtons[key] = KeyButton(leftPad+30*key,300,str(key))
	canvas.menuButtons = [canvas.helpButton, canvas.startGameButton, canvas.cipherButton]
	canvas.gameButtons = [canvas.mainMenuButton]
	canvas.helpButtons = [canvas.mainMenuButton]
	canvas.cipherButtons = [canvas.mainMenuButton, canvas.translateButton, canvas.encryptButton,]
	canvas.keyButtons = canvas.keyButtons.values()
	canvas.scoreButtons = [canvas.mainMenuButton]
def initTextFields():
	canvas.gameTextFields = []
	canvas.gameInput = TextField(canvas.width/2-350,canvas.height/2+150)
	canvas.cipherInput = TextField(canvas.width/2-350,canvas.height/2+150)
	canvas.gameTextFields = [canvas.gameInput]
	canvas.cipherTextFields = [canvas.cipherInput]
def run():
	global cipherObject
	cipherObject = Caesar()
	global root
	root = Tk()
	global canvas
	canvas = Canvas(root, width=1000, height=600)
	canvas.width = 1000
	canvas.height = 600
	canvas.pack()
	canvas.text = ''
	canvas.typingEnabled = False
	canvas.currentTextField = None
	canvas.background = "bisque"
	canvas.gameState = "menu"
	canvas.startTime = time.clock()
	canvas.gameWon = False
	canvas.scorePrinted = False
	canvas.currentLevel = 1
	canvas.maxLevel = 5
	canvas.rawWord = ''
	canvas.encryptedWord = ''
	canvas.key = None
	canvas.shift = None
	canvas.levelPassed = False
	initButtons()
	initTextFields()
	drawMainMenu()
	root.bind("<Button-1>", clickButton)
	root.bind("<KeyPress-BackSpace>", callBackSpace)
	root.bind("<Return>",clickButton)
	#root.bind("<space>",printSpace)
	timerFired()
	root.mainloop()

def timerFired():
	delay = 10
	canvas.after(delay, timerFired)
	if canvas.typingEnabled == True:
		root.bind("<Key>", inputText)
	elif canvas.typingEnabled == False:
		root.bind("<Key>", nullFunction)
	if canvas.gameWon and not canvas.scorePrinted:
		canvas.scorePrinted = True
		canvas.gameState = "score"
		drawGame()
	if canvas.gameState == "game":
		if time.clock()-canvas.startTime > 1.0:
			canvas.startTime = time.clock()
			canvas.secondsCounter += 1
def displayButtons(buttonsList):
	for button in buttonsList:
		button.displayButton()
def displayTextFields(textFieldsList):
	for textField in textFieldsList:
		textField.displayButton()
def drawGame():
	if canvas.gameState == "menu":
		drawMainMenu()
	elif canvas.gameState == "score":
		drawScore()
	elif canvas.gameState == "game":
		drawCipherGame()
	elif canvas.gameState == "help":
		drawHelp()
	elif canvas.gameState == "cipher":
		drawCipherCreator()
def drawBackground():
	canvas.delete(ALL)
	canvas.create_rectangle(0, 0, canvas.width, canvas.height, fill=canvas.background)
def drawMainMenu():
	canvas.delete(ALL)
	drawBackground()
	canvas.create_text(canvas.width/2, canvas.height/2, text="CAESAR CIPHER DECRYPTION CHALLENGE", fill="black", font="calibri 18")
	displayButtons(canvas.menuButtons)
def drawCipherGame():
	canvas.delete(ALL)
	drawBackground()
	displayButtons(canvas.gameButtons)
	displayTextFields(canvas.gameTextFields)
	canvas.create_text(canvas.width/2,canvas.height/2+210, text="Click on the box above to enter decrypted message. Press enter when done",\
					   fill="black", font="calibri 10")
	canvas.create_text(100, 100, text="LEVEL " + str(canvas.currentLevel) + "/" + str(canvas.maxLevel), fill="black", font="calibri 18")
	drawEncryptedWord()
	if canvas.text == canvas.rawWord:
		canvas.gameInput.correctAnswer()
		canvas.currentLevel += 1
		if canvas.currentLevel == canvas.maxLevel:
			canvas.gameWon = True
		else:
			getNextWord()
			canvas.delete(ALL)
			canvas.text = ''
			drawGame()
def getEncryptedWord():
	shift = random.randrange(22,25)
	canvas.key = 26-shift
	canvas.rawWord = cipherObject.getRandomWord()
	while len(canvas.rawWord) < 3 or len(canvas.rawWord) > 5:
		canvas.rawWord = cipherObject.getRandomWord()
	return cipherObject.applyShift(canvas.rawWord,shift)
def getNextWord():
	canvas.encryptedWord = getEncryptedWord()
def drawEncryptedWord():
	if len(canvas.encryptedWord) == 0:
		getNextWord()
	canvas.create_text(canvas.width/2, 150, text=canvas.encryptedWord, fill="black", font="calibri 30")
	canvas.create_text(canvas.width/2, 100, text="key: " + str(canvas.key), fill="black", font="calibri 18")
def drawHelp():
	canvas.delete(ALL)
	instructionsTitle = "Welcome to the Caesar Cipher Decryption Challenge!"
	instructions = "This game puts your cipher decription skills to the test.\nThe goal of the game is to"\
					+ " decrypt ten Caesar Cipher encrypted phrases (of random words) as quickly as possible.\nAs soon as you"\
					+ " solve a cipher, simply click on the text box, type the word in, and press enter.\n"\
					+ "The box will turn green if your guess was correct."
	howCaesarWorks = "How do Caesar Ciphers work?"
	caesarInstructions = 'In Caesar Ciphers, each letter of a message is "shifted" by a certain value.\n'\
						  + 'Encrypting the letter "a" with a shift value of 2 would shift the "a" two places to the right,\n'\
						  + 'so it would become a "c". Shifting the word "hello" with a value of 4 would yield "lipps".\n'\
						  + 'A key is a value tells you how to decypher a Cipher: a key of 3 would tell you that you need\n to '\
						  + 'shift every letter forward three positions. For example, "mouse" with a shift \nof 1 would yield "npvtf".'
	drawBackground()
	canvas.create_text(canvas.width/2, 100, text = instructionsTitle, fill="black", font="calibri 18")
	canvas.create_text(canvas.width/2, 175, text = instructions, fill="black", font="calibri")
	canvas.create_text(canvas.width/2, 250, text = howCaesarWorks, fill="black", font="calibri 18")
	canvas.create_text(canvas.width/2, 350, text = caesarInstructions, fill="black", font="calibri")
	displayButtons(canvas.helpButtons)
	
def drawScore():
	canvas.delete(ALL)
	drawBackground()
	canvas.create_text(500,300,text="You took " + str(canvas.secondsCounter) + " seconds to decipher 5 words.",fill="black",font="calibri 15")
	displayButtons(canvas.scoreButtons)
def printTranslation():
	if canvas.cipherState == "translate":
		if canvas.text != '':
			canvas.shift = cipherObject.findBestShift(canvas.text)
			canvas.create_text(canvas.width/2,550, text=str(cipherObject.applyShift(canvas.text,canvas.shift)) + ", key = "\
								+ str(26-canvas.shift) + ", shift = " + str(canvas.shift), fill="black", font="calibri 18")
def drawCipherCreator():
	canvas.delete(ALL)
	drawBackground()
	canvas.create_text(canvas.width/2, 50, text="CIPHER CREATOR", fill="black", font="calibri 18")
	canvas.create_text(canvas.width/2, 80, text="Translate a Casear Cipher or create one yourself!", fill="black", font="calibri 13")
	canvas.create_text(canvas.width/2,canvas.height/2+210, text="Click on the box above to type.",\
					   fill="black", font="calibri 10")
	canvas.create_text(canvas.width/2,140, text="MODE:",\
					   fill="black", font="calibri 18")
	canvas.create_text(canvas.width/2,280, text="Key:", fill="black", font="calibri 18")
	displayButtons(canvas.cipherButtons)
	displayButtons(canvas.keyButtons)
	displayTextFields(canvas.cipherTextFields)
	if canvas.cipherState == "encrypt":
		canvas.encryptButton.printButtonStatus()
		canvas.create_text(canvas.width/2,550, text=cipherObject.applyShift(canvas.text,canvas.key), fill="black", font="calibri 18")
	if canvas.cipherState == "translate":
		canvas.translateButton.printButtonStatus()
	printTranslation()
run()
