from psychopy import visual, event, data, gui, core
# import module for creating data frame and saving log file
import pandas as pd
# import module to create new directory 
import os
# import csv to read csv-file with questions
import csv
#import random for shuffling stimuli list
import random
#import core for wait time

# define dialogue box (important that this happens before you define window)
box = gui.Dlg(title = "")
box.addField("ID: ") 
box.addField("Alder: ")
box.addField("Køn: ", choices=["Andet", "Kvinde", "Mand"])
box.addField("Eksperimentbetingelse: ", choices=["0","1"])
box.addField("Frame: ", choices=["A","B"])
box.addField("Ville i dag stemme: ", choices=["Socialdemokratiet","Venstre", "Moderaterne", "Socialistisk Folkeparti", "Danmarksdemokraterne", "Liberal Alliance", "Det Konservative Folkeparti", "Enhedslisten", "Radikale Venstre", "Alternativet", "Nye Borgerlige", "Dansk Folkeparti"])
box.show()

#Intro text control
introtext_control = '''Du vil om et kort øjeblik blive præsenteret med et citat og en påstand.\n\n
Din opgave er at vurdere sandsynligheden for, at påstanden er sand eller usand på en skala fra 100% rigtig til 100% forkert. 
Det vil sige, at 50% svarer til, at du vurderer, at påstanden har lige stor sandsynlig for at være sand, som usand.\n\n 
Du vælger dit svar ved at rykke den røde markør på skalaen og afgiver svaret ved at trykke på mellemrums-tasten.\n\n 
Du vil først blive præsenteret med 3 øvespørgsmål for at blive bekendt med formatet.\n\n 
Tryk på mellemrums-tasten for at starte.
'''

#intro text experiment
introtext_experiment = '''Dette er et spil, der handler om at optjene flest mulige point. Du starter med 100 point.\n\n 
Du vil om et kort øjeblik blive præsenteret med et citat og en påstand.\n\n 
Din opgave er at vurdere sandsynligheden for, at påstanden er sand eller usand på en skala fra 100% rigtig til 100% forkert. 
Du vinder point ved at svare "forkert" til usande påstande og "rigtigt" til sande påstande. 
Hvis dit svar er korrekt, vinder du det dobbelte af de point du har satset. 
Hvis du derimod ikke svarer korrekt, mister du dine satsede point. 
Du kan også vælge ikke at satse noget, hvis du synes, der lige stor sandsynlighed for at påstanden er sandt som usandt.\n\n 
Din indsats bliver beregnet, som den optimale indsats, ud fra den sandsynlighed du har vurderet.\n\n 
Du vælger dit svar, ved at rykke den røde markør på skalaen og afgiver svaret ved at trykke på mellemrums-tasten.\n\n 
Du vil først blive præsenteret med 3 øvespørgsmål for at blive bekendt med formatet.\n\n 
Tryk på mellemrums-tasten for at starte.
'''

#debrief message
debrief = '''Forsøget er nu slut. Udsagne du har set kommer ikke fra politikerene. Disse er fundet på for at påvirke forsøgsdeltagernes vurderinger. I virkeligheden er hensigten med dette forsøg, at undersøge om man kan forbedre folks dømmekraft ved at fremstille spørgsmålene i et spil. Tak for at du deltog i forsøget!
'''

#training round text
after_training = ''' Træningsspørgsmålene er nu ovre. De næste spørgsmål tæller med i eksperimentet. Gå videre ved at trykke på mellemrumstasten'''

# define window
win = visual.Window(units='height', fullscr = True, color = [-0.6314, -0.3804, -0.3804])

##Functions
#define evaluation function. 0 = no response, 1 = correct, -1 incorrect
def evaluate_response(rating, tf):
    
    #if answer is 0
    if rating == 50:
        return 0
    
    #if answer is correct
    if (tf == "t" and rating > 50) or (tf == "f" and rating < 50):
        return 1
    
    #if incorrect
    else:
        return -1

#defining kellybet. Takes bankroll, probability of winning and returns optimal wager size
def kellybet(bankroll, probability_of_winning):
    
    wager = 0
    
    if probability_of_winning is not None:
        #prob of winnning
        p = float(probability_of_winning) / 100
    
        #proportion of the bet gained in a win
        b = 1.0
    
        #what fraction to bet
        f = p - ((1 - p) / b)
    
        wager = bankroll * f
    
    return wager

#function for showing message for a certain time
def msg_wait(text, wait_time):
    message = visual.TextStim(win, text = text, height = 0.05)
    message.draw()
    win.flip()
    core.wait(wait_time)
    

#function for showing message until spacebar
def msg_spacebar(text):
    message = visual.TextStim(win, text = text, alignText = "left", height = 0.025)
    message.draw()
    win.flip()
    event.waitKeys(keyList=["space"])

#give feedback function
def give_feedback(evaluation):
    
    if evaluation == -1:
        msg_wait("Dit svar var forkert", 1.1)
    elif evaluation == 1:
        msg_wait("Dit svar var korrekt", 1.1)
    else: 
        msg_wait("Dit svar var neutralt", 1.5)

if box.OK: # To retrieve data from popup window
    ID = box.data[0]
    Age = box.data[1]
    Gender = box.data[2]
    condition = box.data[3]
    Frame = box.data[4]
    Vote = box.data[5]
elif box.Cancel: # To cancel the experiment if popup is closed
    core.quit()

#date
date = data.getDateStr()

## define logfile 
# prepare pandas data frame for recorded data
columns = ['time_stamp','id', "question_text", "question_num", 'accuracy', "points", "rating", "vote"]
logfile = pd.DataFrame(columns=columns)

# make sure that there is a logfile directory and otherwise make one
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")

# define logfile name
logfile_name = "logfiles/logfile_{}_{}.csv".format(ID, date)

##Defining elements
# define points stimuli
points_stim = visual.TextStim(win, pos=(-0.5 , 0.45), color = [1.0000, 0.2941, -1.0000])
points_stim.size = 0.07

# define points to 100
points = 100.0

# define betting
betsize = visual.TextStim(win, pos=(0, -0.15))
betsize.size = 0.05

# define question
question = visual.TextStim(win, pos=(0, 0.0))
question.size = 0.04


#define frame
frame_text = visual.TextStim(win, pos=(0, 0.3))
frame_text.size = 0.05

# define question counter
ordinal_num = 0

# define slider
scale = visual.Slider(win,
             ticks=(0,25,50,75,100),
             labels=['100% forkert', '75% forkert', '50%  (Neutral)', '75% rigtigt', '100% rigtigt'],
             startValue=50,
             granularity=1,
             color='white',
             pos = (0,-0.25),
             labelHeight = .03)

#choose file path that corresponds with chosen framing
if Frame == "A":
    file = open("stimuli/Questions_A.txt")
else:
    file = open("stimuli/Questions_B.txt")

#read chosen csv file to dict object
questions = csv.DictReader(file, delimiter=';')

#turn dictReader object into list
questions = list(questions)


#shuffle list
#random.shuffle(questions)

#read in training questions
file = open("stimuli/questions_training.txt")
training_questions = list(csv.DictReader(file, delimiter=';'))

#insert training questions after real questions
questions.extend(training_questions)

#reverse order of questions to bring training questions to the front
questions.reverse()

#show intro-text for correct condition
if condition == "0":
    msg_spacebar(introtext_control)
else:
    msg_spacebar(introtext_experiment)


#Iterate through all key-value pairs
for dct in questions:
    
    #when training questions are done reset points
    if ordinal_num == len(training_questions):
        msg_spacebar(after_training)
        points = 100
    
    #Reset scale
    scale.reset()
    
    #Set rating to middlepoint
    rating = 50
    
    #frame
    frame_text.text = dct["Frame"]
    
    #get question
    question.text = "Er det følgende udsagn  rigtigt? \n \n" + dct["Question"]
    
    #get current points
    points_stim.text = "Point: " + str(points)
    
    # update scale and betsize until key press:
    while not event.getKeys(keyList = ["space"]):
        
        #Only override rating with the scale rating if a rating on slider has been selected
        if scale.getRating() is not None:
            rating = scale.getRating()
        
        # display on screen for experiment
        if condition == "1":
            if rating < 50:
                betsize.text = "Du satser " + str(abs(round(kellybet(points, rating)))) + " på forkert"
                
            elif rating > 50:
                betsize.text = "Du satser " + str(abs(round(kellybet(points, rating)))) + " på rigtigt"
                
            else:
                betsize.text = "Du satser " + str(abs(round(kellybet(points, rating))))
                
                
                
            points_stim.draw()
        
        # else display control condition
        else:
            #display correct expression for false and true
            # for leaning false
            if rating < 50:
                betsize.text = str(100 - rating) +"% forkert"
            # for leaning true
            elif rating > 50:
                betsize.text = str(rating) +"% rigtigt"
            # for neutral
            else: 
                betsize.text = "50% rigtigt 50% forkert (Neutral)"            
                
                
        
        # always display
        betsize.draw()
        scale.draw()
        question.draw()
        frame_text.draw()
        win.flip()
    
    #evaluate response
    evaluation = evaluate_response(rating, dct["t_or_f"])
    
    #calculate new points
    points = round(points + evaluation * abs(kellybet(points, rating)))
    
    #keep track of order of stimuli
    ordinal_num = ordinal_num + 1
    
    #keep track of question num
    question_num = dct["num"]
    
    #append logfile
    logfile = logfile.append({
        'time_stamp': date,
        'id': ID,
        "question_text": dct["Question"],
        "ordinal_num": ordinal_num,
        'accuracy': evaluation,
        "question_num": question_num,
        "rating" : rating,
        "condition": condition,
        "frame": Frame,
        "points": points,
        "vote": Vote}, ignore_index = True)
    
    #give feedback
    give_feedback(evaluation)

#show final points
if condition == "1":
    msg_wait("Endeligt antal point: " + str(points), 2)
    

#show debrief
msg_spacebar(debrief)

# save data to directory
logfile.to_csv(logfile_name)








