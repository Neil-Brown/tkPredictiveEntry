# Author Neil Brown
# https://github.com/Neil-Brown/

import tkinter as tk

class Entry(tk.Text):
    """ Custom Entry widget that provides predictive text from a list of terms passed in as a kwarg"""
    def __init__(self,
                 window,
                 text="Search",
                 font=("Arial", 12),
                 inactive_foreground="grey",
                 active_foreground="black",
                 width=15,
                 height=1,
                 predictive_list=()
    ):
        tk.Text.__init__(self)
        """ Sets the keyword parameters as attributes and bind the relevant keys to metods."""
        self.master = window
        self.text = text
        self.font = font
        self.inactive_foreground = inactive_foreground
        self.active_foreground = active_foreground

        self.predictive_list = sorted(predictive_list)

        self.configure(font=self.font, width=width, height=height)
        self.configure(tabs=(1,))

        self.tag_configure("predictive", foreground=self.inactive_foreground)
        self.tag_configure("normal", foreground=self.active_foreground)

        self.bindtags(('Text', 'post-class-bindings', '.', 'all'))

        self.bind_class("post-class-bindings", "<FocusIn>", lambda event: self.focus_in())
        self.bind_class("post-class-bindings", "<FocusOut>", lambda event: self.focus_out())
        self.bind_class("post-class-bindings", "<KeyPress>", lambda event: self.input())
        self.bind_class("post-class-bindings", "<Right>", lambda event: self.autofill())
        self.bind_class("post-class-bindings", "<Left>", lambda event: self.move_left())
        self.bind_class("post-class-bindings", "<Delete>", lambda event: self.delete_called())
        self.bind_class("post-class-bindings", "<BackSpace>", lambda event: self.delete_called())

        self.focus_out()

    def focus_out(self):
        """ Put the default text into the entry if entry is equal and entry aws no focus"""
        if self.get("1.0", "end-1c") == "":
            self.configure(font=self.font, foreground=self.inactive_foreground)
            self.insert("1.0", self.text)

    def focus_in(self):
        """ Delete default text when entry gets focus"""
        if self.get("1.0", "end-1c") == self.text:
            self.delete("1.0", "end-1c")
            self.configure(font=self.font, foreground=self.active_foreground)

    def input(self):
        """ Called when a key is pressed. Calls relevent methods."""
        self.reduce_tag()
        user_txt = self.get_user_text()
        pred_txt = self.get_predictive_text(user_txt)
        if not pred_txt:
            self.remove_predictive_text()
            return
        self.insert_txt(user_txt, pred_txt)

    def insert_txt(self, user_txt, pred_txt):
        """ Delete entry contents and refill with user text but predictive text if available"""
        self.delete("1.0", "end-1c")
        self.insert("1.0", user_txt + pred_txt)
        self.mark_set("insert", "1.{}".format(len(user_txt)))
        self.tag_add("predictive", "insert", "end-1c")

    def remove_predictive_text(self):
        """ Clear entry of text and predictive tag"""
        self.tag_remove("predictive", "1.0", "end-1c")
        self.delete("insert", "end-1c")

    def reduce_tag(self):
        """ Remove the start of the predictive tag range"""
        if self.tag_ranges("predictive"):
            self.tag_remove("predictive", self.tag_ranges("predictive")[0])

    def get_user_text(self):
        """ Return range of user inputed text"""
        if self.tag_ranges("predictive"):
            end = "{}".format(self.tag_ranges("predictive")[0].string)
        else:
            end = "end"
        return self.get("1.0", end+"-1c")

    def get_predictive_text(self, txt):
        """ Return predicitve text if iser input matches list items"""
        for item in self.predictive_list:
            if item.lower().startswith(txt.lower()):
                return item[len(txt):]
        return None

    def move_left(self):
        """ Called when left cursor is pressed. Move one space left."""
        self.mark_set("insert", "insert")

    def autofill(self):
        """ Called on the right cursor being pressed.
        Fill entry with rest of predictive text in normal foreground color"""
        self.tag_remove("predictive", "1.0", "end-1c")
        self.tag_add("normal", "1.0", "end-1c")
        self.mark_set("insert", "end-1c")

    def delete_called(self):
        """ Called when backspace is pressed.
            Delete predictive text if cursor is at "1.0"""
        if self.tag_ranges("predictive") and self.tag_ranges("predictive")[0].string == "1.0":
            self.tag_remove("predictive", "1.0", "end-1c")
        self.input()
