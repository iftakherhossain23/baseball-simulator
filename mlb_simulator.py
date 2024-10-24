# Program     : MLB - Python Edition
# Name        : Iftakher Hossain
# Date        : Feb 21, 2022
# Description : This program simulates a baseball game through using the 2021
#               batting statistics of 9 MLB players in a separate file to
#               determine if they reach a base or not through 5 innings.

#Set up the program's various modules

#Display the state of affairs, including the batter, their statistics, and the outcomes of the previous play
def display(inning,outs,runs,batting,on_base_percent_bat,second_base_bat,third_base_bat,home_run_bat,on_deck,
            previous_player,previous_result,first_base_player,second_base_player,third_base_player):
    print("------------------------------------------------------------")
    print("Innings:",inning)
    print("Outs:",outs)
    print("Score:",runs)
    print("Batter:",batting)
    print("OBP:",on_base_percent_bat)
    print("Doubles:",second_base_bat,"- Triples:",third_base_bat,"- Home Runs:",home_run_bat)
    print("On Deck:",on_deck)
    print("Previous:",previous_player,previous_result)
    print("1B:",first_base_player)
    print("2B:",second_base_player)
    print("3B:",third_base_player)

#Use the statistics from the file to determine the probability of each outcome    
def hit(second,third,home,ab,obp):
    import random

    second = int(second)
    third = int(third)
    home = int(home)
    ab = int(ab)
    obp = float(obp)
    
    hit_chance = random.randrange(1,1001)
    second_chance = 1000 * (round((second / ab),3))
    third_chance = 1000 * (round((third / ab),3))
    hr_chance = 1000 * (round((home / ab),3))

    #Compare the statistics with the random number to determine the outcome of the pitch (i.e. how many bases were advanced)
    if (hit_chance <= obp*1000):
        base_chance = random.randrange(1,1001)
        if (base_chance <= second_chance):
            base_advance = 2
        elif (base_chance <= second_chance + third_chance):
            base_advance = 3
        elif (base_chance <= second_chance + third_chance + hr_chance):
            base_advance = 4
        else:
            base_advance = 1
    else:
        base_advance = 0

    #Return the outcome to the main function
    return base_advance

def previous(base_progress,previous_result):
    #Determine the outcome of the previous pitch to display
    if (base_progress == 0):
       previous_result =  "- Out"
    elif (base_progress == 1):
       previous_result =  "- Single"
    elif (base_progress == 2):
       previous_result =  "- Double"
    elif (base_progress == 3):
       previous_result =  "- Triple"
    elif (base_progress == 4):
       previous_result =  "- Home Run"

    return previous_result

def result(score):
    #Create a randomly generated score for the opposing team
    import random
    opposing_score = random.randrange(11)
    output_message = ""
    
    #Determine the result of the match depending on the scores
    if (score > opposing_score):
        output_message = "You win! " + str(score) + "-" + str(opposing_score)
    elif (score < opposing_score):
        output_message = "You lose! " + str(score) + "-" + str(opposing_score)

    return output_message

def main():
    #Set up the lists that will collect from the player statistics file
    players = []
    second_base = []
    third_base = []
    home_run = []
    at_bat = []
    on_base_percent = []

    #Set up the variables that will be used during the game 
    inning = 1
    runs = 0
    outs = 0
    batter_ctr = 0
    first_base_player = ""
    second_base_player = ""
    third_base_player = ""
    base_progress = ""
    previous_player = ""
    previous_result = ""
    final_out_complete = False

    #Read from the statistics file
    stats_file = "player_statistics.txt"
    stats = open(stats_file,"r")
    
    stats_read = stats.readline()
    
    while (stats_read != ""):
        #Continually collect the statistics and add them to separate lists
        stats_read = stats_read.split()
        players.append(stats_read[0])
        second_base.append(stats_read[1])
        third_base.append(stats_read[2])
        home_run.append(stats_read[3])
        at_bat.append(stats_read[4])
        on_base_percent.append(stats_read[5])
        stats_read = stats.readline()

    #Start the gameplay of 5 innings
    while (inning <= 5):

        #Resetting certain variables each inning
        first_base_player = ""
        second_base_player = ""
        third_base_player = ""

        #Simulate the current inning until 3 outs are reached
        while (outs < 3):

           #Obtain the previous pitch's outcome
           previous_result = previous(base_progress,previous_result)

           #Determine the current batter
           batting = players[batter_ctr]

           #Display the on deck batter; if the end of the list is reached, the first batter is on deck
           if (batter_ctr <= 7):
               on_deck = players[batter_ctr+1]
           elif (batter_ctr == 8):
               on_deck = players[0]

           #Display the previous batter; if this is the start of the list then show the batter at the end of the list
           #assuming this will only likely be needed outside the first inning
           if (batter_ctr >= 1):
               previous_player = players[batter_ctr-1]
           elif (batter_ctr == 0 and inning != 1):
               previous_player = players[8]

           #Receive input to "throw a pitch"
           pitch = input("Press Enter for the next pitch..")

           #Display the state of affairs, including the batter, their statistics, and the outcomes of the previous play
           if (pitch == ""):
               if (final_out_complete):
                   outs = 3
               display(inning,outs,runs,batting,on_base_percent[batter_ctr],second_base[batter_ctr],third_base[batter_ctr],home_run[batter_ctr],
                       on_deck,previous_player,previous_result,first_base_player,second_base_player,third_base_player)
               
               #Proceed to the next batter in the list
               if (batter_ctr != 8):
                   batter_ctr += 1
               elif (batter_ctr == 8):
                   batter_ctr = 0
                   
           #Use the hit function to determine the outcome of the batter each pitch
           base_progress = hit(second_base[batter_ctr],third_base[batter_ctr],home_run[batter_ctr],at_bat[batter_ctr],on_base_percent[batter_ctr])

           #Create the aftermath of the outcome, adjusting any men on the other bases accordingly
           if (base_progress == 0):
               #Ensure the final inning reaches 3 outs and does not get skipped in the loop
               if (not final_out_complete and outs == 2 and inning == 5):
                   outs = 2
                   final_out_complete = True
               else:
                   outs += 1
           elif (base_progress == 1):
               if (third_base_player != ""):
                   runs += 1
               third_base_player = second_base_player
               second_base_player = first_base_player
               first_base_player = batting
           elif (base_progress == 2):
               if (third_base_player != ""):
                   runs += 1
               third_base_player = first_base_player
               if (second_base_player != ""):
                   runs += 1
               second_base_player = batting
               first_base_player = ""
           elif (base_progress == 3):
               if (third_base_player != ""):
                   runs += 1
               third_base_player = batting
               if (second_base_player != ""):
                   runs += 1
               second_base_player = ""
               if (first_base_player != ""):
                   runs += 1
               first_base_player = ""
           elif (base_progress == 4):
               if (third_base_player != ""):
                   runs += 1
               third_base_player = ""
               if (second_base_player != ""):
                   runs += 1
               second_base_player = ""
               if (first_base_player != ""):
                   runs += 1
               first_base_player = ""
               runs += 1
            
               
        #Resetting certain variables each inning
        inning += 1
        outs = 0
        
    #Determine and display the result upon completion of the simulation
    print(result(runs))

#Running the program with the main function
main()
