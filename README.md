[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5a74125791a8439ea04f93a8aaa3c883)](https://app.codacy.com/app/neilbrownemail/tkPredictiveEntry?utm_source=github.com&utm_medium=referral&utm_content=Neil-Brown/tkPredictiveEntry&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/Neil-Brown/tkGradientButton.svg?branch=master)](https://travis-ci.org/Neil-Brown/tkGradientButton)[![Coverage Status](https://coveralls.io/repos/github/Neil-Brown/tkPredictiveEntry/badge.svg?branch=master)](https://coveralls.io/github/Neil-Brown/tkPredictiveEntry?branch=master)[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# tkPredictiveEntry
A tkinter Entry widget that provides predictive text assistance.

## Requirements
-   Windows, Mac or Linux
-   Python 2.7 or 3.x with tkinter

## Installation
Place entry.py into your project directory:
`from entry import Entry`

## Documentation
     my_entry = Entry(window=window)
     my_entry.pack()

Places the Entry into the parent provided. 
Any of the three geometry managers: "pack", "grid", or "place" can be used.

Optional keyword arguments:
-   font
    -   Takes a tuple of family name and font size
    -   Defaults to ("Arial", 12)
    
-   text
    -   The text to display when the entry is empty and has no focus
    -   Defaults to "Search"
    
-   inactive_foreground
    -   The font color to use for predictive text
    -   Defaults to grey
    
-   active_foreground = 
    -   Font color for user input
    -   Defaults to "back"
    
-   width = 
    -   The width of the Entry widget
    -   Defaults to 15
    
-   predictive_list = 
    -   A list string terms from which the predictive text is to be supplied
     

## Example
     import tkinter as tk

     from entry import Entry


     class Main(tk.Tk):
         def __init__(self):
             tk.Tk.__init__(self)
             self.entry = Entry(window=self,
                                  inactive_foreground="grey",
                                  active_foreground="black",
                                  font=("Arial", 20),
                                  text="Display message",
                                  predictive_list = [
                                                     "Michael Jackson",
                                                     "George Michael",
                                                     "Tom Cruise",
                                  ]

             )
             self.entry.pack(fill=None, expand=False)

     if __name__ == '__main__':
         main = Main()
         main.mainloop()
