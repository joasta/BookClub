import pandas as pd
import re
from random import randint
from Intern import Intern



if __name__ is '__main__':
    name = input("Who are you?\n")
    #name="jj"
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
            #parse_input("rate (Book) <4.5>", name)
            #parse_input("getu j", name)
            #parse_input("getg fiction", name)
            #parse_input("info Book5", name)
            #parse_input("rec (Book7) {Anna} [poem] http://www.wp.pl wonderful book", name)
            #rec >t Book >a May Parker >g poetry >r 4.5
