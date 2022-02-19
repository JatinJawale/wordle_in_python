import requests
import random
from bs4 import BeautifulSoup as bs
import enchant

from clrprint import *

def print_instructions():
    """Prints instructions for the player"""
    print("\n*****Welcome to Wordle in Python!*****")
    print("Here you have 5 turns to guess a five-letter word.")
    print("If your guess contains letters in correct place, they'll show up as green.")
    print("If your guess contains letters in incorrect place, they'll show up as orange/yellow.")
    print("Each incorrect letter will be red/grey.")
    print("For example, if the target word is 'GREAT', and your first guess is 'GRAPE', the output will be: ")
    compare("GRAPE", "GREAT")
    print("**************Let's Play**************\n")

def get_words():    
    """
        Uses BeautifulSoup to scrape the webpage to get all the 5-letter words.

        Parameters:
            soup - a BeautifulSoup Object

        Returns:
            words - a list of all 5-letter words
    """
    url = "https://www.thefreedictionary.com/5-letter-words.htm" # URL to scrape for words
    page = requests.get(url)

    soup = bs(page.content, "html.parser") # Creating BeautifulSoup object
    results = soup.find_all("li") # Finding the appropriate tags on the page
    
    words = []
    for word in results:
        w = word.get_text('li').upper()
        if len(w) == 5 and w not in words:
            words.append(w)

    return words

def is_valid_guess(guess):
    """
        Validates the guess. The input guess should be 5 characters long and should be a valid english word.
        Here, I am using 'enchant' to check for valid english words.

        Paramter:
            guess - the word to be validated

        Returns:
            boolean - whether the word is valid or not
    """
          
    if len(guess) == 5 and d.check(guess):
        return True
    
    return False


def compare(guess, target):
    """
        Compares the guess and the target, and prints the output accordingly

        Parameters:
            guess - player's input
            target - the word to be guessed.

        Returns:
            solved - a boolean which indicates wheter the player was successful in guessing the target word.
    """
    solved = False

    guess_list = [g for g in guess]

    for g in guess_list:
        if guess_list.count(g) > 1:
            guess_list.remove(g)
    
    if guess == target:
        for j in range(len(guess)):
            clrprint(guess[j] + " ", end='', clr = 'green')
        print("\n\nThat's right! You guessed '{}' correctly!".format(guess))
        solved = True
    else:
        for j in range(len(guess)):
            if guess[j] in target and guess[j] in guess_list:
                if guess[j] == target[j]:
                    clrprint(guess[j] + " ", end='', clr = 'green')
                    
                else:
                    clrprint(guess[j] + " ", end = '', clr = 'yellow')
                guess_list.remove(guess[j])
            else:
                clrprint(guess[j] + " ", end = '', clr = 'red')
        print()
        
    return solved

def play():
    """
        Starts the game for the player
    """
    target = random.choice(words_list)
    
    inst = input("\nDo you want the instructions? (Y for YES, any other key for NO):\n").lower()
    if inst == 'y':
        print_instructions()

    print("\nWord has been decided! Go on and start guessing!")
        
    for i in range(5):
        
        guess = input("\nGuess {}: ".format(i + 1)).upper()

        while not is_valid_guess(guess):
            print("{} is not a valid word!".format(guess))
            guess = input("\nGuess {}: ".format(i + 1)).upper()
            if is_valid_guess(guess):
                break

        solved = compare(guess, target)
        if solved:
            break
                        
    if not solved:
        print("\nSorry. The word was ",end = '')
        clrprint(target, end = '', clr = 'green')
        print(". Try again!")

    again = input("\nPlay again? (Y for YES, any other key for NO):\n").lower()
    if again == 'y':
        play()
    else:
        print("\nThank you for playing!")




d = enchant.Dict('en_US') # Initiating the english disctionary

words_list = get_words()

play()


