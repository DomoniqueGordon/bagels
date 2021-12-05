import random

NUM_DIGITS = 3
MAX_GUESSES = 10


def get_text(path):
    with open(path) as f:
        return f.read()

def get_secret_num():
    numbers = list('0123456789')
    random.shuffle(numbers)
    secret_num = ""
    for i in range(NUM_DIGITS):
        secret_num += str(numbers[i])
    return secret_num

def get_clues(guess, secret_num):
    if guess == secret_num:
        return "You got it!"
    
    clues = []

    for i in range(len(guess)):
        if guess[i] == secret_num[i]:
            # A correct digit is in the correct place.
            clues.append("Fermi")
        elif guess[i] in secret_num:
            # A correct digit is in the incorrect place.
            clues.append("Pico")
    if len(clues) == 0:
        return "Bagels"
    else:
        # Sort the clues into alphabetical order so their original order
        # doesn't give information away
        clues.sort()
        return ' '.join(clues)

def bagels():
    intro = get_text("intro.txt")
    print(intro.format(NUM_DIGITS))

    while True:
        secret_num = get_secret_num()
        print("I have thought up a number.")
        print("You have {} guesses to get it".format(MAX_GUESSES))

        num_guesses = 1
        while num_guesses <= MAX_GUESSES:
            guess = ""
            while len(guess) != NUM_DIGITS or not guess.isdecimal():
                print("Guess #{}: ".format(num_guesses))
                guess = input("> ")

            clues = get_clues(guess, secret_num)
            print(clues)
            num_guesses += 1

            if guess == secret_num:
                break  
            if num_guesses > MAX_GUESSES:
                print("You ran out of guesses.")
                print("The answer was {}.".format(secret_num))

        print("Do you want to play again? (yes or no)")
        if not input("> ").lower().startswith("y"):
            break

    print("Thanks for playing!")



class Bagels:
    @property
    def title(self):
        return "Bagels!"

    @property
    def intro(self):
        intro = get_text("intro.txt")
        return intro.format(NUM_DIGITS)

    @property
    def new_game_message(self):
        return """
        I have thought up a number.
        You have {} guesses to get it right.""".format(MAX_GUESSES)

    def set_secret_num(self):
        numbers = list('0123456789')
        random.shuffle(numbers)
        secret_num = ""
        for i in range(NUM_DIGITS):
            secret_num += str(numbers[i])
        with open("secret_num.txt", "w") as f:
            f.write(secret_num)

    @property
    def secret_num(self):
        with open("secret_num.txt") as f:
            return f.read()

    def get_clues(self, guess):
        if guess == self.secret_num:
            return "You got it!"

        clues = []

        for i in range(len(guess)):
            if guess[i] == self.secret_num[i]:
                # A correct digit is in the correct place.
                clues.append("Fermi")
            elif guess[i] in self.secret_num:
                # A correct digit is in the incorrect place.
                clues.append("Pico")
        if len(clues) == 0:
            return "Bagels"
        else:
            # Sort the clues into alphabetical order so their original order
            # doesn't give information away
            clues.sort()
            return "Clue: " + ' '.join(clues)