import string
import random
import time

maxGuesses = 6

word = ""
guess = ""

wordLen = 0
wordTopic = ""

hits = list()       ## List containing all the correct guesses
misses = list()     ## List containing all the incorrect guesses

## List containing all the remaining letters
remainingLetters = list(string.ascii_uppercase)

## Dictionary, with the "Topics" being the "Keys",
## and the words belonging to that specific topic being stored
## in a list tied to the corresponding "Key"/"Topic"
wordPool = {"Fruits":\
            ["AVOCADO", "ORANGE", "BANANA", "PAPAYA", "WATERMELON"],
            "Sports":\
            ["BASKETBALL", "VOLLEYBALL", "FOOTBALL", "BADMINTON", "NETBALL"],
            "Occupations":\
            ["FIREFIGHTER", "POLICEMAN", "DOCTOR", "ACCOUNTANT", "BANKER"],
            "Zoo Animals":\
            ["ELEPHANT", "GIRAFFE", "KANGAROO", "RABBIT", "SQUIRREL"],
            "Birds":\
            ["VULTURE", "FLAMINGO", "TURKEY", "KINGFISHER", "HUMMINGBIRD"],
            "Insects":\
            ["GRASSHOPPER", "BUTTERFLY", "MOSQUITO", "FIREFLY", "DRAGONFLY"],
            "Countries":\
            ["AFGHANISTAN", "SLOVAKIA", "ECUADOR", "GUATEMALA", "VENEZUELA"]}

## Function to deal with the initial set-up of game
## Displays list of topics, ensures User picks a valid number that represents
## one of the topics, randomly selects one word corresponding to that topic
## Sets "word"(Answer) to the randomly chosen word
## Sets current "guess" by replacing every letter of "word" with an underscore
def init():
    print ("Welcome!! Have fun playing Hangman.. :)")

    ## Shows the list of topics as a sorted list
    topics = sorted(list(wordPool.keys()))
    numOfTopics = len(topics)
    choice = -1

    while choice == -1:
        print ("\nPlease choose from the following list of topics..")
        for index in range(0, numOfTopics):
            print (index+1, ": ", topics[index], sep='')
        prompt = "\nPlease enter a number between 1 and " + \
                 str(numOfTopics) + " to choose a topic: "
        try:
            choice = int(input(prompt)) - 1
        except ValueError:
            print ("Please enter a valid number!")
        else:
            if choice < 0 or choice >= numOfTopics:
                choice = -1
                print ("Invalid choice! Try again...")

    global wordTopic
    wordTopic = topics[choice]
    
    print ("\nYou have chosen the topic \"" + wordTopic + "\"!")
    print ("Reminder: 6 wrong guesses and you lose!")
    print ("\nMay the odds be ever in your favor..")

    global word, wordLen, guess
    word = random.choice(wordPool[wordTopic])
    wordLen = len(word)
    guess = "_"*len(word)

## Function will display the different states of
## the Hangman figure based on the number of misses
def displayHangman():
    ## "Private" function __drawHangman
    def __drawHangman(headWithArms = "", body = "", legs = ""):
        print ("\n\t" + "|"*10 + "\n\t||" + "|".center(12) + \
               "\n\t||" + headWithArms.center(12) + \
               "\n\t||" + body.center(12) + \
               "\n\t||" + legs.center(12) + \
               "\n\t||\n" + "".ljust(6) + "|"*16 + "\n")

    ## No switch statement in Python, therefore using
    ## if-elif-else here to draw different states of the hangman
    numOfMisses = len(misses)
    if   (numOfMisses == 0):
        __drawHangman()                     ## Gallows only
    elif (numOfMisses == 1):
        __drawHangman("O")                  ## Head only
    elif (numOfMisses == 2):
        __drawHangman("O", "|")             ## Head and body
    elif (numOfMisses == 3):
        __drawHangman("_O ", "|")           ## Head, body and right arm
    elif (numOfMisses == 4):
        __drawHangman("_O_", "|")           ## Head, body and both arms
    elif (numOfMisses == 5):
        __drawHangman("_O_", "|", "/  ")    ## Head, body, arms and right leg
    else:
        __drawHangman("_O_", "|", "/ \\")   ## Complete Hangman

## Main display function to update the screen
## Used to display the hangman figure, current guess,
## as well as the "Hits", "Misses" & remaining letters
def display():
    displayHangman()
    print ("\nWord: ", " ".join(list(guess)),\
           "\t[Word Length: ", wordLen, "]",\
           "[Topic: ", wordTopic, "]", sep = '')
    print ("\nHits:".ljust(8), ",".join(hits))
    print ("Misses:".ljust(7), ",".join(misses))
    print ("Remaining letters:", ",".join(remainingLetters))

## Prompts user to input his/her next guess
## Ensures that it is one of the remaining letters
## Adds it to "hits" if guessed letter is part of the word,
## Else adds it to "misses", update number of misses,
## Removes the guessed letter from the list of remaining letters
def getNextGuess():
    prompt = "\nPlease choose your next letter: "
    try:
        ## Converts input to uppercase, i.e. 'a' & 'A' are
        ## both valid inputs for the letter 'A'
        char = input(prompt).upper()
    except ValueError:
        print ("Please enter a valid letter!")
    else:
        if char not in remainingLetters:
            print ("Please enter a valid letter!")
        else:
            if char in word:
                print ("Great choice! :)")
                hits.append(char)
                ## Updates the guess, by replacing the corresponding
                ## underscores with the correct letter using string slicing
                for index in range(0, len(word)):
                    if word[index] == char:
                        global guess
                        guess = guess[0:index] + char + guess[index+1:]
            else:
                misses.append(char)
                print ("Bad choice.. " +\
                       ("try again!" if len(misses) < maxGuesses else ":(") )
            
            remainingLetters.remove(char)

## Checks if game is over, i.e. to see if the current guess is the word itself
def gameOver():
    return word == guess

## End of game, shows if the user has won or lost
## Reveals the answer in the event that user has lost
def showResults():
    display()

    results = "\n\n" + ("Congratulations!! You have won! :)" if gameOver()\
                else "You have lost.. The answer is \"" + word + "\"..") +\
                "\n" + "- "*8 + "[GAME OVER]" + " -"*8

    ## Prints out the string one character at a time, i.e. typewriter effect
    for letter in results:
        print (letter, end='')
        time.sleep(0.045)

## Main game loop
init()
while not gameOver() and len(misses) < maxGuesses:
    display()
    getNextGuess()
showResults()
