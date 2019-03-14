import tkinter as tk

class Entry(tk.Text):
    def __init__(self,
                 window,
                 text="Search",
                 font=("Arial", 12),
                 inactive_foreground="grey",
                 active_foreground="black",
                 width=15,
                 height=1,
                 predictive_list=[]
    ):
        tk.Text.__init__(self)
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
        if self.get("1.0", "end-1c") == "":
            self.configure(font=self.font, foreground=self.inactive_foreground)
            self.insert("1.0", self.text)

    def focus_in(self):
        if self.get("1.0", "end-1c") == self.text:
            self.delete("1.0", "end-1c")
            self.configure(font=self.font, foreground=self.active_foreground)

    def input(self):
        self.reduce_tag()
        user_txt = self.get_user_text()
        pred_txt = self.get_predictive_text(user_txt)
        if not pred_txt:
            self.remove_predictive_text()
            return
        self.insert_txt(user_txt, pred_txt)

    def insert_txt(self, user_txt, pred_txt):
        self.delete("1.0", "end-1c")
        self.insert("1.0", user_txt + pred_txt)
        self.mark_set("insert", "1.{}".format(len(user_txt)))
        self.tag_add("predictive", "insert", "end-1c")

    def remove_predictive_text(self):
        self.tag_remove("predictive", "1.0", "end-1c")
        self.delete("insert", "end-1c")

    def reduce_tag(self):
        if self.tag_ranges("predictive"):
            self.tag_remove("predictive", self.tag_ranges("predictive")[0])

    def get_user_text(self):
        if self.tag_ranges("predictive"):
            end = "{}".format(self.tag_ranges("predictive")[0].string)
        else:
            end = "end"
        return self.get("1.0", end+"-1c")

    def get_predictive_text(self, txt):
        for item in self.predictive_list:
            if item.lower().startswith(txt.lower()):
                return item[len(txt):]
        return None

    def move_left(self):
        self.mark_set("insert", "insert")

    def autofill(self):
        print("auto")
        self.tag_remove("predictive", "1.0", "end-1c")
        self.tag_add("normal", "1.0", "end-1c")
        self.mark_set("insert", "end-1c")

    def delete_called(self):
        if self.tag_ranges("predictive") and self.tag_ranges("predictive")[0].string == "1.0":
            self.tag_remove("predictive", "1.0", "end-1c")
        self.input()
