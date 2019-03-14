from unittest import TestCase

from entry import Entry


class TestEntry(TestCase):
    def setUp(self):
        self.l = ["q23", "abcd", "adef", "zfv"]
        self.entry = Entry(window=None, predictive_list=self.l)

    def test_list_sorted(self):
        self.assertEqual(self.entry.predictive_list, sorted(self.l))

    def test_focus_in_text(self):
        self.entry.event_generate("<FocusIn>")
        self.assertEqual(self.entry.get("1.0", "end-1c"), "")

    def test_focus_in_foreground(self):
        self.entry.event_generate("<FocusIn>")
        self.assertEqual(self.entry.cget("foreground"), self.entry.active_foreground)

    def test_focus_out_text(self):
        self.entry.event_generate("<FocusOut>")
        self.assertEqual(self.entry.get("1.0", "end-1c"), "Search")

    def test_focus_out_foreground(self):
        self.entry.event_generate("<FocusOut>")
        self.assertEqual(self.entry.cget("foreground"), self.entry.inactive_foreground)


class TestUserEntry(TestCase):
    def setUp(self):
        self.l = ["q23", "abcd", "adef", "zfv"]
        self.entry = Entry(window=None, predictive_list=self.l)
        self.entry.delete("1.0", "end-1c")
        self.entry.event_generate("<FocusIn>")

    def test_get_user_text(self):
        self.entry.insert("insert", "a")
        self.assertEqual("a", self.entry.get_user_text())

    def test_get_user_text_multiple_chars(self):
        self.entry.insert("insert", "a")
        self.entry.insert("insert", "b")
        self.assertEqual("ab", self.entry.get_user_text())

    def test_get_predictive_text(self):
        self.assertEqual("bcd", self.entry.get_predictive_text("a"))

    def test_get_predicitve_text_multiple(self):
        self.assertEqual("d", self.entry.get_predictive_text("abc"))

    def test_get_predictive_text_no_match(self):
        self.assertEqual(None, self.entry.get_predictive_text("p"))


class TestDelete(TestCase):
    def setUp(self):
        self.l = ["q23", "abcd", "adef", "zfv"]
        self.entry = Entry(window=None, predictive_list=self.l)
        self.entry.event_generate("<FocusIn>")
        for char in "abc":
            self.entry.insert("insert", char)
            self.entry.input()
        self.entry.delete("1.0", "end-1c")

    def test_no_text_when_all_deleted(self):
        self.assertEqual(self.entry.get("1.0", "end-1c"), "")

    def test_no_tag_when_all_deleted(self):
        self.assertEqual(self.entry.tag_ranges("predictive"), ())


class TestAutoFill(TestCase):
    def setUp(self):
        self.l = ["q23", "abcd", "adef", "zfv"]
        self.entry = Entry(window=None, predictive_list=self.l)
        self.entry.event_generate("<FocusIn>")
        self.entry.insert("insert", "a")
        self.entry.input()
        self.entry.autofill()

    def test_autofill_text(self):
        self.assertEqual(self.entry.get("1.0", "end-1c"), "abcd")

    def test_autofill_predictive_tag_removed(self):
        self.assertEqual(self.entry.tag_ranges("predictive"), ())

    def test_autofill_normal_tag_added(self):
        self.assertEqual(self.entry.tag_ranges("normal")[0].string, "1.0")
        self.assertEqual(self.entry.tag_ranges("normal")[1].string, "1.4")

    def test_autofill_cursor_at_end(self):
        self.assertEqual(self.entry.index("insert"), "1.4")
