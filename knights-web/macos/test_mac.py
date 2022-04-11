import os
path="/Users/simonelopez/Documents/chromedriver/chromedriver"



import string
import random

number_of_strings = 5
length_of_string = 8
print(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))

