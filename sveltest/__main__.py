#!/usr/bin/env python
#-*- coding:utf-8 -*-

# authors:guanfl
# 2022/9/23

"""

                   _  _              _
                  | || |            | |
  ___ __   __ ___ | || |_  ___  ___ | |_
 / __|\ \ / // _ \| || __|/ _ \/ __|| __|
 \__ \ \ V /|  __/| || |_|  __/\__ \| |_
 |___/  \_/  \___||_| \__|\___||___/ \__|


"""
from .runner import main

main()


from io import StringIO
import string, sys

stdout = sys.stdout

sys.stdout = file = StringIO()

print ("""
According to Gbaya folktales, trickery and guile
are the best ways to defeat the python, king of
snakes, which was hatched from a dragon at the
world's start. -- National Geographic, May 1997
""")

sys.stdout = stdout

print (file.getvalue())


print(55)
