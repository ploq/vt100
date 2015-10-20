import sys, re, time

import escape


class Terminal:
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.term = [["" for k in range(width)] for n in range(height)]
        self.curr = [0,0]

    def add_width(self, rel_width):
        for n in range(rel_width):
            for i in self.term:
                self.width += 1
                i.append("")

    def move_cur_abs(self, x, y):
        print("Move", x ,y)
        if self.width > x and self.height > y:
            self.curr[0] = x
            self.curr[1] = y

        if self.height < y:
            for n in range(y - self.height):
                self.height += 1
                self.term.append(["" for k in range(self.width)])

        if self.width < x:
            self.add_width(x+self.width)

    def move_cur_rel(self, x=None, y=None):
        """x,y is how many steps to move"""
        if x and self.width > self.curr[0] + x > 0:
            self.curr[0] = self.curr[0] + x
        elif x and self.curr[0] + x > self.width:
            self.width += 1
            self.term[self.curr[1]].append("")
            self.curr[0] = self.curr[0] + x

        if y and self.height < self.curr[1] + y:
            self.curr[1] = self.curr[1] + y

        elif y and (self.height > self.curr[1] + y) and self.curr[1] + y > 0:
            self.term.append(["" for k in range(self.width)])
            self.height += 1
            self.curr[1] = self.curr[1] + y
            self.curr[0] = 0

    def add(self, char):
        if self.curr[0] + 1 > self.width:
            self.curr[1] += 1

        self.term[self.curr[1]][self.curr[0]] = {"char": char, "color": "white"}
        if self.curr[0] + 1 < self.width:
            self.curr[0] += 1

    def print_term(self):
        for y in self.term:
            for x in y:
                if x != "":
                    sys.stdout.write(x["char"])
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")


class Parser:
    def __init__(self, term):
        self.term = term

    def parse_seq(self, seq):
        a = re.match("(\d+);(\d+)H", seq)
        if a:
            self.term.move_cur_abs(int(a.group(2)), int(a.group(1)))

    def parse(self, line=None):
        collected = ""
        state = "escape"
        for char in line:
            if char == escape.ESC:
                state = "escape"
                continue
            if char.isdigit() and state == "escape":
                collected += char
            elif char == ";":
                collected += char
            elif char.isalpha() and state == "escape":
                esc = collected + char
                self.parse_seq(esc)
                collected = ""
                state = "not"
            elif state != "escape":
                self.term.add(char)

term = Terminal(20,10)
parser = Parser(term)

with open("test.log") as fd:
    for line in fd:
        parser.parse(line)

term.print_term()

