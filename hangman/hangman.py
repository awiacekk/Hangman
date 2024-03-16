import os
import random
from deep_translator import GoogleTranslator

class Game:
    def __init__(self) -> None:
        self.language = None
        self.players = None
        file = open('languages.txt','r')
        self.languages = []
        while True:
            content=file.readline()
            if not content:
                break
            self.languages.append(content.replace("\"","").replace(",\n",""))
        file.close()
        self.translator = lambda text: text if self.language == "english" else GoogleTranslator(source='english', target=self.language).translate(text)

    def _play_(self):
        while(True):
            language = input("Enter the full language name with a capital letter (you will not be able to change it until you start a new game): ")
            if language not in self.languages:
                print("There is no such language, please enter it's full name")
            else:
                self.language = language.lower()
                break
        info = self.translator("Enter number of players (1 or 2)")
        error = self.translator("Incorrent number of players")
        while(True):
            try:
                players = int(input(info+': '))
                if players in [1,2]:
                    self.players = players
                    break
                else:
                    print(error)
            except Exception as e:
                print(error)

        print(self.translator("The game begins. This may take a few seconds..."))


class Hangman(Game):
    def __init__(self) -> None:
        super().__init__()
        super()._play_()
        self.prepare_translations()
    
    def prepare_translations(self):
        self.enter_level = self.translator("Enter your level of difficulty")
        self.error_level = self.translator("Only levels mentioned above are available")
        self.enter_letter = self.translator("Enter a letter or the word")
        self.wrong_wrd = self.translator("Wrong word. Mistakes")
        self.letter_needed = self.translator("A letter is needed")
        self.no_letter = self.translator("There is no such letter in this word. Mistakes")
        self.congr_player_won = self.translator("Congratulations, player 2 won!")
        self.congr_you_won = self.translator("Congratulations, you won!")
        self.unf_player_died = self.translator("Unfortunately, player 2 died. The word was")
        self.unf_you_died = self.translator("Unfortunately, you died. The word was")
        self.wanna_play = self.translator("Do you want to play again?")
        self.enter_word = self.translator("Player 1 enters the word")
        self.wanna_change = self.translator("Do you want to change the number of players or a language?")
    
    def play_hangman(self):
        while(True):
            levels = ["beginner", "intermediate", "advanced"]
            while(True):
                difficulty = input(self.enter_level+' (beginner, intermediate, advanced): ')
                if difficulty not in levels:
                    print(self.error_level)
                else:
                    if difficulty == levels[0]:
                        mistakes = 8
                    elif difficulty == levels[1]:
                        mistakes = 5
                    elif difficulty == levels[2]:
                        mistakes = 3
                    break
            if self.players == 2:
                word = input(self.enter_word+": ")
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                word = self.translator(random.choice(list(open('words.txt'))))
            show = []
            for s in word:
                show.append('_ ')
            print(''.join(show))

            current_mistakes = 0

            while(not current_mistakes==mistakes):
                character = input(self.enter_letter+': ')
                while(not character.isalpha()):
                    character = input(self.letter_needed+': ')
                if len(character) > 1:
                    if character != word:
                        current_mistakes += 1
                        print(self.wrong_wrd+': '+str(current_mistakes)+' / '+str(mistakes))
                        continue
                    else:
                        if self.players == 2:
                            print(self.congr_player_won)
                        else:
                            print()
                        break
                flag = False
                for index, s in enumerate(word):
                    if s == character:
                        show[index] = s+' '
                        flag = True
                if not flag:
                    current_mistakes += 1
                    print(self.no_letter+': '+str(current_mistakes)+' / '+str(mistakes))

                print(''.join(show))
                if ''.join(show).replace(' ','') == word:
                    if self.players == 2:
                        print(self.congr_player_won)
                    else:
                        print(self.congr_you_won)
                    break
                elif current_mistakes==mistakes:
                    if self.players == 2:
                        print(self.unf_player_died+": "+word)
                    else:
                        print(self.unf_you_died+": "+word)
                        
            answer = input(self.wanna_play+" (Y/n): ")
            if answer == 'n':
                break
            else:
                answer = input(self.wanna_change+" (Y/n): ")
                if answer == 'Y':
                    super()._play_()
                    self.prepare_translations()


game = Hangman()
game.play_hangman()
