# UNO rules
plus = True
starting_hand = 7
num_of_wildcard = 4
repetition = 1
suites = ['b','g','r','y',]
num_of_suites = len(suites)
cards = ['0','1','1','2','2','3','3','4','4','5','5','6','6','7','7','8','8','9','9','p','p','r','r','s','s','w','W']
numbers = list(dict.fromkeys(cards))
num_of_norm = (len(numbers)-2)*num_of_suites*repetition


# Crazy Eights rules
# plus = False
# starting_hand = 5
# num_of_wildcard = 4
# repetition = 1
# suites = ['b','g','r','y',]
# num_of_suites = len(suites)
# cards = ['2','3','4','5','6','7','9','0','J','Q','K','A','w','W']
# numbers = list(dict.fromkeys(cards))
# num_of_norm = (len(numbers)-2)*num_of_suites*repetition

debug = False

