from Intern import Intern
import os

os.chdir(os.path.dirname(__file__))

if __name__ is '__main__':
    """
    Pass user's name and request to an Intern object.
    """

    name = input("Who are you?\n")
    bot = Intern(name)
    proceed = True
    while proceed:
        instream = input("What do you want to do? rec/rate/info/getu/getg\n")
        if instream == "q":
            proceed = False
        elif instream == "":
            pass
        else:
            bot.parse_text(instream)
            #i.e.: rec >t Book >a May Parker >g poetry >r 4.5
