import random

CLEAR = '\033[0;255m'
COL_VALUE = bytearray(b'\x01\x04\x02\x03\x05')
def colors(i): return '\033[' + str(COL_VALUE[i]) + ';255m'

##CLEAR = '\033[00m'
##COL_VALUE = bytearray(b'[\"\\]#')
##def colors(i):
##    return '\033[' + str(COL_VALUE[i]) + 'm'

CARDS_PER_PLAYER = 32

def card_format(card):
    num = card & 15
    special = num - 9
    formats = ("[ " + str(num) + "]", "[+2]", "[SK]", "[RE]", "[+4]", "[WI]")
    return colors(card >> 4) + formats[max(special, 0)] + CLEAR

def random_card(force_color = False):
    r = random.random()
    if r < 0.80:
        number = 0
        if r > 0.0421: number = random.randint(1, 9)
        color = random.randint(0, 3)
        return (color << 4) | number
    special = 10 + random.randint(0, 4)
    if force_color or special < 13: return special | (random.randint(0, 3) << 4)
    else: return special | (4 << 4)

def ask_color():
    while True:
        print("\n\n" + CLEAR + ("Pick a color:") + "\n\n" + ("1: " + colors(0) + "RED " + CLEAR + "2: " + colors(1) + "BLUE" + CLEAR) + "\n" +
              ("3: " + colors(2) + "GREEN " + CLEAR + "4: " + colors(3) + "YELLOW" + CLEAR) + "\n\n\n\n")
        num = input("Enter color: ")
        if not num.isdigit():
            input("Invalid choice.")
            continue
        num = int(num)
        if num < 1 or num > 4:
            input("Invalid choice.")
            continue
        return num - 1

hands = bytearray(CARDS_PER_PLAYER*4)
card_counts = bytearray(4)
order = None
players = ['','','','']
wins = []
rounds = bytearray(1)
        
# Register players and give out cards
count = ""
while not count.isdigit() or not (int(count) > 1 and int(count) <= 4): count = input("Enter player count (max 4):\n")
count = int(count)
order = list(range(count))
for i in range(count - 1, 0, -1):
    j = random.randint(0, i)
    order[i], order[j] = order[j], order[i]
for i in range(count):
    name = ""
    while len(name) <= 0 or len(name) > 7: name = input("Enter player " + str(i + 1) + "'s name (max 7):\n")
    # Setup player
    players[i] = name
    card_counts[i] = 7
    for j in range(7): hands[i * CARDS_PER_PLAYER + j] = random_card()
    
# Reset game state
debt = bytearray(2)
last_played = random_card(True)
skip = False
# Game loop
while True:
    if len(order) < 2:
        wins.append(order[0])
        break
    l = 0
    while 0 <= l < len(order):
        i = order[l]
        l += 1
        p_col = colors(i)
        # Print player turn, as well as next player
        if not skip:
            print("\n" + p_col + players[i] + "'s turn, next: " + players[order[l % len(order)]] + "\n")
        else:
            print("\n" + p_col + players[i] + ", your turn was")
            print(p_col + "skipped by " + players[order[(l - 2) % len(order)]] + CLEAR)
        print("\n\n\n\n\n")
        # Handle skipping turns
        if not skip: input(p_col + "Press ENTER to play.\n")
        else:
            input(p_col + "Press ENTER to end turn.\n")
            skip = False
            continue
        # Ask player to perform an action
        drawn, played, draw_debt, placed_card = False, False, False, False
        choice, status_msg = "", ""
        rounds[0] += 1
        
        while True:
            # Collect debt if needed BEFORE rendering card screen
            if draw_debt:
                for j in range(debt[0]):
                    hands[i * CARDS_PER_PLAYER + card_counts[i]] = random_card()
                    card_counts[i] += 1
                debt[0] = 0
                draw_debt = False
            if played and placed_card:
                last_special = (last_played & 15) - 9
                if last_special == 1:
                    debt[0] += 2
                    debt[1] = 1
                elif last_special == 4:
                    debt[0] += 4
                    debt[1] = 4
                
            print("\n" + p_col + "Current card: " + card_format(last_played) + p_col + ", Debt: " + str(debt[0]) + "\n" + CLEAR)
            line_count = (card_counts[i] + 3) // 4

            for j in range(line_count):
                line = ""
                for k in range(min(4, card_counts[i] - j * 4)):
                    card_index = k + j * 4
                    line += "{:02}:{} ".format(card_index + 1, card_format(hands[CARDS_PER_PLAYER * i + card_index]) + CLEAR)
                print(line)
            if (7 - line_count) > 0:
                print("\n" * (6 - line_count))

            if status_msg:
                input(p_col + status_msg)
                status_msg = ""
                if played == True: break
                continue

            if drawn: choice = input(p_col + "Card (- is skip): ")
            else: choice = input(p_col + "Card (- is draw): ")

            if choice == "-":
                if drawn:
                    played = True
                    status_msg = "Skipping..."
                    continue
                else:
                    draw_debt = True
                    drawn = True
                    hands[i * CARDS_PER_PLAYER + card_counts[i]] = random_card()
                    card_counts[i] += 1
                    status_msg = "Drawing..."
                    continue
            if not choice.isdigit():
                status_msg = "Invalid input!"
                continue
            choice = int(choice)
            if choice < 1 or choice > card_counts[i]:
                status_msg = "Invalid card index!"
                continue
            
            play_index = i * CARDS_PER_PLAYER + choice - 1
            card = hands[play_index]
            special = (card & 15) - 9
            # Card with wild color
            if special > 3:
                wild_color = ask_color()
                card = (card & 15) | (wild_color << 4)
                played = True
            # Regular colored card check
            elif (card & 15) == (last_played & 15) or (card >> 4) == (last_played >> 4):
                played = True
            if played:
                placed_card = True
                draw_debt = debt[0] > 0
                if draw_debt and (special == 1 or special == 4): draw_debt = debt[1] != special                        
                last_played = card
                card_counts[i] -= 1       
                for j in range(play_index, i * CARDS_PER_PLAYER + card_counts[i]):
                    hands[j] = hands[j + 1]
                # Skip and reverse cards
                if special == 2 or (special == 3 and len(order) == 2): skip = True
                elif special == 3 and len(order) > 2:
                    order.reverse()
                    l = len(order) - 1 - l

                if card_counts[i] > 0: status_msg = "Played card..."
                else:
                    wins.append(i)
                    del order[l-1]
                    status_msg = "You're out!"
            else: status_msg = "Can't play that."
# Print results
p_col = colors(wins[-1])
print("\n",p_col + "Game Over!","\n\n",p_col + "-- Results --","\n",p_col + "Rounds: " + str(rounds[0]),"\n",p_col + "-- Winners --")
for i in range(count): print(p_col + str(i) + ":", players[wins.pop(0)])
input("\n" * (5 - count) + p_col + "Press ENTER to end game." + CLEAR)
