import random
import string

from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.app import App


charset = {x:0 for x in list(string.ascii_uppercase)}

numletters = 5
#you need to define variable before using, doesnt metter what the num (5) is, it changes later anyway

class MainScreen(Screen):

    def ResetGame(self, inputform):
        inputform.clear_widgets()
        print(numtries, word)
        pass



    def StartGame(self, inputform, numberofletters):
    # inputform is the area where user inputs letters - Input Screen

        global dictionary
        global words
        global word
        global currenttry
        global numletters
        global numtries

        numletters = numberofletters
        currenttry = 1
        numtries = numletters + 1

        with open("guessable_words2", "r") as f:
            dictionary = f.read().splitlines()
        with open("hidden_words2", "r") as f:
            words = f.read().splitlines()
        word = random.choice(words)
        while len(word) != numberofletters:
            word = random.choice(words)
        word = word.upper()

        #for test purposes
        print(word)

        inputform.buildinputform(numberofletters+1)

        inputform.children[numberofletters].disabled = False
        inputform.children[numberofletters].children[numberofletters-1].focus = True

    #def restart(self, inputform):
        #inputform.children[6 - currenttry].disabled = True
        #for i in range(6):
            #for x in range(5):
                #inputform.children[i].children[x].text = ''
                #inputform.children[i].children[x].background_color = (1, 1, 1, 1)


class MainLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_up=self.keyboard_up)

    def keyboard_up(self, key, keycode, modifier):
        if self.children[1].children[1].check_line_full():
            if keycode == 13:
                self.children[1].children[1].check(self.children[1].children[0])


class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    pass

class MyLetterInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s=''
        if self.text:
            self.text = ''
        if substring.isalpha():    #checks if string is made up of letters
            s = substring.upper()
        if self.focus_next != StopIteration:
            nextwidget = self.get_focus_next()
            nextwidget.focus = True
        return super().insert_text(s, from_undo=False)

    def do_backspace(self, from_undo = False, mode='bkspc'):
        if len(self.text) > 0:
            self.text = ''
        elif self.focus_previous != StopIteration:
            previousblock = self.get_focus_previous()
            previousblock.focus = True
            if previousblock.text:
                previousblock.text = ''


class MyWordleApp(App):
    pass

class MyLineInput(BoxLayout):
    # using size_hint_y values in kivy file
    boxheight = (14 - 4) / (numletters + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



        for i in range(numletters):
            newletter = MyLetterInput()
            if i == (numletters - 1):
                newletter.focus_next = StopIteration
            elif i == 0:
                newletter.focus_previous = StopIteration
            self.add_widget(newletter)


class InputScreen(BoxLayout):
    messageproperty = StringProperty("Good Luck!")


    def buildinputform(self, numberoflines):
        for i in range(numberoflines):
            newline = MyLineInput()
            self.add_widget(newline)
            if i != 0:
                newline.disabled = True

    def check(self, letterlist):
        global currenttry
        word_guessed = False
        word_complete = True
        attempt = ''
        for i in range(1,numtries):
            attempt += "".join(self.children[numtries - currenttry].children[numletters - i].text)
        if len(attempt) < numletters:
            word_complete = False
        if not word_guessed and currenttry == numtries:
            self.messageproperty = 'Sorry you lost :( The word was ' + word
        if word_complete and not word_guessed and attempt.lower() in dictionary:
            if attempt == word:
                word_guessed = True
                self.messageproperty = 'YOU GUESSED IT!!'
                for i in range(0, numletters):
                    self.children[numtries - currenttry].children[(numletters - 1) - i].background_color = (0.4, 0.57, 0.5, 1)
            else:
                for i in range(0, numletters):
                    charset[attempt[i]] = 1
                    if attempt[i] == word[i]:
                        charset[attempt[i]] = 3
                        self.children[numtries - currenttry].children[(numletters - 1) - i].background_color = (0.09, 0.7, 0.56, 1)
                    else:
                        letterinword = False
                        for i2 in range(numletters):
                            if (word[i2] == attempt[i]) and (i2 != i) and (attempt[i2] != word[i2]):
                                self.children[numtries - currenttry].children[(numletters - 1) - i].background_color = ((1, 0.85, 0.34, 1))
                                charset[attempt[i]] = 2

                letterlist.updatecolor()
                self.children[numtries - currenttry].disabled = True
                currenttry += 1
                self.children[numtries - currenttry].disabled = False
                self.children[numtries - currenttry].children[numletters - 1].focus = True
        else:
            self.messageproperty = "Invalid Input! Try Again!"


    def check_line_full(self):
        attempt = ''
        for i in range(1, numtries):
            attempt += "".join(self.children[numtries - currenttry].children[numletters - i].text)
        if len(attempt) < numletters:
            return False
        else:
            return True



class RemainingLetters(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clear_widgets()
        for letter in charset.keys():
            nextletter = Label(text=letter, color=(33/255, 37/255, 41/255, 1), size_hint=(0.20, 0.20), font_size=40, font_name='BebasNeue-Regular')
            self.add_widget(nextletter)
    def updatecolor(self):
        for i in self.children:
            match charset[i.text]:
                case 0:
                    with i.canvas.before:
                        Color(0.8, 0.8, 0.85, 1)
                        Rectangle(size=(i.width, i.height), pos=i.pos)
                case 1:
                    with i.canvas.before:
                        Color(0.9, 0.4, 0.36, 1)
                        Rectangle(size=(i.width, i.height), pos=i.pos)

                case 2:
                    with i.canvas.before:
                        Color(0.95, 0.87, 0.6, 1)
                        Rectangle(size=(i.width, i.height), pos=i.pos)

                case 3:
                    with i.canvas.before:
                        Color(0.4, 0.57, 0.5, 1)
                        Rectangle(size=(i.width, i.height), pos=i.pos)

    def reset(self):
        global charset
        charset = {x: 0 for x in list(string.ascii_uppercase)}
        self.updatecolor()

if __name__ == "__main__":
    MyWordleApp().run()