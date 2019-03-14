# tkPredictiveEntry
A tkinter Entry widget that provides predictive text assistance.

## Requirements
* Windows, Mac or Linux
* Python 2.7 or 3.x with tkinter

## Installation
Place entry.py into your project directory:
`from entry import Entry`

## Documentation
     my_entry = Entry(window=window)
     my_entry.pack()

Places the Entry into the parent provided. 
Any of the three geometry managers: "pack", "grid", or "place" can be used.

Optional keyword arguments:
* font = 
  * Takes a tuple of family name and font size
  * Defaults to ("Arial", 12)
* text = 
   * The text to display when the entry is empty and has no focus
   * Defaults to "Search"
* inactive_foreground =
   * The font color to use for predictive text
   * Defaults to grey
* active_foreground = 
   * Font color for user input
   * Defaults to "back"
* width = 
   * The width of the Entry widget
   * Defaults to 15
* predictive_list = 
   * A list string terms from which the predictive text is to be supplied
     

## Example
    import tkinter as tk
    
    from entry import Entry
    
    
    class Main(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
            self.configure(width=WIDTH, height=HEIGHT)
            center(self, self.winfo_screenwidth(), self.winfo_screenheight())
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
