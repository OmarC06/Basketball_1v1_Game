from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from random import *
import os

Image.MAX_IMAGE_PIXELS = None

root = Tk()
root.title("Basketball")
root.geometry("500x800")

def raise_frame(frame):
  frame.tkraise()
  if frame == b:
      root.geometry("500x800")

a = Frame(root)
b = Frame(root)
c = Frame(root)

for frame in (a, b, c):
  frame.grid(row=0, column=0, sticky='nsew')

gif = Label(c, image="")
gif.grid(row=0, column=0)

def gifSetup(foldername, filename):
    raise_frame(c)
    
    file = f"clips/{foldername}/{filename}"
    info = Image.open(file)
    height = ImageTk.PhotoImage(info).height()
    width = ImageTk.PhotoImage(info).width()
    root.geometry(f"{width}x{height}")

    frames = info.n_frames
    animationFrames = []
    for i in range(frames):
        frame = ImageTk.PhotoImage(info.copy())
        animationFrames.append(frame)
        info.seek(i)

    def animation(currentFrame):
        if currentFrame == frames:
            info.close()
            raise_frame(b)
        else:
            frame = animationFrames[currentFrame]
            gif.configure(image=frame)
            currentFrame += 1

            c.after(50, animation, currentFrame) 
    animation(0)
    

spots = [
  "Centercourt",
  "Deep Center",
  "Deep Right Wing",
  "Deep Left Wing",

  "Top 3",
  "Right Wing 3",
  "Left Wing 3",
  "Right Corner 3",
  "Left Corner 3",

  "Top Mid",
  "Right Wing Mid",
  "Left Wing Mid",
  "Right Corner Mid",
  "Left Corner Mid",

  "Top Paint",
  "Right Paint",
  "Left Paint",
  "Center Paint"
]

def startGame():
    if gamepointE.get() and gamepointE.get().isnumeric():
        raise_frame(b)
        jumpball()
    else: 
        messagebox.showerror("Notice", "Enter a valid Game Point.")
def rerollRatings(value):
    global user, cpu
    user = playerMaker(ratings = ratingsMaker("user", value))
    cpu = {
    "ratings" : playerMaker(ratings = ratingsMaker("cpu", value)),

    "tendencies" : playerMaker(tendencies = tendencyMaker())
        
}
  
    for item in ratingTree.get_children():
        ratingTree.delete(item)
    for item2 in ratingTree2.get_children():
        ratingTree2.delete(item2)
    for rating in user.keys():
        ratingTree.insert("", END, values=(user[rating], rating, cpu["ratings"][rating]))
        ratingTree2.insert("", END, values=(user[rating], rating, cpu["ratings"][rating]))

startBtn = Button(a, text="Start", command=startGame).pack()#grid(row=0, column=0)
difficultyE1 = StringVar(a, "Pro")
difficultyE2 = OptionMenu(a, difficultyE1, "G-League", "Pro", "Hall of Fame", command=rerollRatings)
difficultyE2.pack()
rerollBtn = Button(a, text="Reroll Ratings", command=lambda: rerollRatings(difficultyE1.get())).pack()#.grid(row=1, column=0)
gamepointL = Label(a, text="Game Point").pack()
gamepointE = Entry(a)
gamepointE.insert(0, "21")
gamepointE.pack()
ratingTree = ttk.Treeview(a, columns=("You", "Rating", "Opp"), show="headings")
ratingTree.pack(fill=BOTH, expand=1)#grid(row=2, column=0)
ratingTree.column("You", anchor=CENTER, width=50)
ratingTree.column("Rating", anchor=CENTER, width=100)
ratingTree.column("Opp", anchor=CENTER, width=50)
ratingTree.heading("You", text="You")
ratingTree.heading("Rating", text="Rating")
ratingTree.heading("Opp", text="Opp")
# need a tendency tree actually nvm

score = [0,0]

currentSpot = spots[0]

def jumpball(): # since this is 1v1 itll just be random and not take jumpball skills. coin flip
  choice = randint(0, 1)
  if choice == 0:
      response("user", "offense", "jumpball", spots[0])
      messagebox.showinfo("Notice", "You have started with possession of the ball.")
      actionL.config(text=f"It is your ball. What will you do? You are at {currentSpot.lower()}.")
  else:
      response("cpu", "offense", "jumpball", spots[0])
      messagebox.showinfo("Notice", "The opponent has started with possession of the ball.")

def ratingsMaker(who, difficulty):
    match difficulty:
        case "G-League":
            match who:
                case "user":
                    mins = [20,35,55,30,75,70,80,50,40]
                    maxes = [45,65,85,90,95,95,95,90,95]
                case "cpu":
                    mins = [1,5,15,1,35,20,40,10,1]
                    maxes = [5,35,45,50,55,60,60,40,50]
        case "Pro":
            match who:
                case "user":
                    mins = [1,15,35,1,55,50,70,20,10]
                    maxes = [25,45,65,70,75,90,90,60,80]
                case "cpu":
                    mins = [1,15,35,1,55,50,70,20,10]
                    maxes = [25,45,65,70,75,90,90,60,80]
        case "Hall of Fame":
            match who:
                case "user":
                    mins = [1,10,25,1,45,40,50,15,5]
                    maxes = [15,35,50,60,65,60,70,45,55]
                case "cpu":
                    mins = [10,30,35,25,65,70,80,45,35]
                    maxes = [35,55,65,80,85,90,90,80,90]
    # the maxes and mins change depending on difficulty. need to think of most efficient 
    # way to do it bc rn id have to make A LOT of variables to take into account the cpu
    # AND user min/max changes
    
    for ratingName in ["Deep", "3", "Mid", "Inside", "Movement", "Defense", "Craftiness"]:
        match ratingName:
            case "Deep":
                ratingsA = [randint(mins[0], maxes[0]) for x in range(4)]
            case "3":
                ratingsB = [randint(mins[1], maxes[1]) for x in range(5)]
            case "Mid":
                ratingsC = [randint(mins[2], maxes[2]) for x in range(5)]
            case "Inside":
                ratingsD = [randint(mins[4], maxes[4]) for x in range(4)]
                ratingsD2 = [randint(mins[3], maxes[3])]
                ratingsD.extend(ratingsD2)
            case "Movement": # dribble and drive
                ratingsE = [randint(mins[5], maxes[5]) for x in range(3)]
                ratingsE2 = [randint(mins[6], maxes[6]) for x in range(2)]
                ratingsE.extend(ratingsE2)
            case "Defense":
                ratingsF = [randint(mins[7], maxes[7]) for x in range(6)]
            case "Craftiness": # contested and draw fouls
                ratingsG = [randint(mins[8], maxes[8]) for x in range(2)]
                
    overallRatings = []
    overallRatings.extend(ratingsG)
    overallRatings.extend(ratingsA)
    overallRatings.extend(ratingsB)
    overallRatings.extend(ratingsC)
    overallRatings.extend(ratingsD)
    overallRatings.extend(ratingsE)
    overallRatings.extend(ratingsF)
    
    return overallRatings    
    
def playerMaker(ratings = None, tendencies = None):        
    if ratings:
        ratingsDecider = {
            "Contested" : 50, # higher = good
            "Draw Foul" : 50,

            "Centercourt" : 50,
            "Deep Center" : 50,
            "Deep Right Wing" : 50,
            "Deep Left Wing" : 50,

            "Top 3" : 50,
            "Right Wing 3" : 50,
            "Left Wing 3" : 50,
            "Right Corner 3" : 50,
            "Left Corner 3" : 50,

            "Top Mid" : 50,
            "Right Wing Mid" : 50,
            "Left Wing Mid" : 50,
            "Right Corner Mid" : 50,
            "Left Corner Mid" : 50,

            "Top Paint" : 50,
            "Right Paint" : 50,
            "Left Paint" : 50,
            "Center Paint" : 50,

            "Dunk" : 50, # maybe dunk adds a boost?
            # "Layup" : 50, # no idea what to do with these. should i js assume the players can always dunk?
            #####
            "Stepback" : 50,
            "Crossover" : 50,
            "Hesitation" : 50,
            "Ball Security" : 50,
            "Drive" : 50,

            #####
            "Contest" : 50,
            "Block" : 50,
            "Steal" : 50,
            "Perimeter D" : 50,
            "Interior D" : 50, # need to use
            "Foul" : 50, #higher = worse
        }

        for x in ratingsDecider.keys():
            ratingsDecider[x] = ratings[list(ratingsDecider.keys()).index(x)]
        
        return ratingsDecider
      
    if tendencies:
        tendencyDecider = {
            "Centercourt" : 50,
            "Deep Center" : 50,
            "Deep Right Wing" : 50,
            "Deep Left Wing" : 50,

            "Top 3" : 50,
            "Right Wing 3" : 50,
            "Left Wing 3" : 50,
            "Right Corner 3" : 50,
            "Left Corner 3" : 50,

            "Top Mid" : 50,
            "Right Wing Mid" : 50,
            "Left Wing Mid" : 50,
            "Right Corner Mid" : 50,
            "Left Corner Mid" : 50,

            "Top Paint" : 50,
            "Right Paint" : 50,
            "Left Paint" : 50,
            "Center Paint" : 50,
            
            "Dunk" : 50, # maybe dunk adds a boost?
            # "Layup" : 50, # no idea what to do with these. should i js assume the players can always dunk?

            #####
            "Stepback" : 50,
            "Crossover" : 50,
            "Hesitation" : 50,
            "Dribble" : 50, 
            "Move" : 50, 
            "Back-Out" : 50,
            "Drive" : 50, 
            
            #####
            "Contest" : 50,
            "Steal" : 50,
            "Position for Rebound" : 50, # no rating
            "Do Nothing" : 50, # no rating
        }
            
        for x in tendencyDecider.keys():
            tendencyDecider[x] = tendencies[list(tendencyDecider.keys()).index(x)]

        return tendencyDecider    
        
user = playerMaker(ratings = ratingsMaker("user", difficultyE1.get()))
cpu = {
    "ratings" : playerMaker(ratings = ratingsMaker("cpu", difficultyE1.get())),

    "tendencies" : 
        {
        "Centercourt" : 50,
        "Deep Center" : 50,
        "Deep Right Wing" : 50,
        "Deep Left Wing" : 50,

        "Top 3" : 50,
        "Right Wing 3" : 50,
        "Left Wing 3" : 50,
        "Right Corner 3" : 50,
        "Left Corner 3" : 50,

        "Top Mid" : 50,
        "Right Wing Mid" : 50,
        "Left Wing Mid" : 50,
        "Right Corner Mid" : 50,
        "Left Corner Mid" : 50,

        "Top Paint" : 50,
        "Right Paint" : 50,
        "Left Paint" : 50,
        "Center Paint" : 50,
        
        "Dunk" : 50, # maybe dunk adds a boost?
        # "Layup" : 50, # no idea what to do with these. should i js assume the players can always dunk?

        #####
        "Stepback" : 50,
        "Crossover" : 50,
        "Hesitation" : 50,
        "Dribble" : 50,   
        "Move" : 50,
        "Back-Out" : 50, 
        "Drive" : 50, 

        #####
        "Contest" : 50,
        "Steal" : 50,
        "Position for Rebound" : 50,
        "Do Nothing" : 50
    }
}

def tendencyMaker():
    tendency = []
    actualTendency = []

    for x in list(cpu["ratings"].keys()):
        if x in cpu["tendencies"].keys():
            if x == "Contest":
                contestT = randint(50, 90)
                tendency.append(contestT)
            else:
                tendency.append(cpu["ratings"][x])
        else:
            if x == "Ball Security":
                for y in range(3):
                    tendency.append(cpu["ratings"]["Ball Security"]//2)
            if x in ["Block", "Perimeter D", "Interior D", "Foul"]:
                continue
            
    tendency.append(100 - contestT) 
    tendency.append(100 - cpu["ratings"]["Steal"])        
    
    for y in tendency:
        min = y-10
        if min < 0:
            min = 1
        max = y+10
        if max > 99:
            max = 99
            
        actualTendency.append(randint(min, max))
    # for a,z in enumerate(tendency):
    #     print(list(cpu["tendencies"].keys())[a], z, actualTendency[a])
    return actualTendency

cpu["tendencies"] = playerMaker(tendencies = tendencyMaker())  

actionL = Label(b, text="") 
actionL.grid(row=0, column=0)
actionED = Entry(b)
actionED.grid(row=1, column=0)

def confirm():    
    global options, userTargetSpot, userDribbleMove 
    newAction = actionED.get()
    if newAction not in options:
        messagebox.showerror("Incorrect Action", "Enter a possible action.")
    else:
        if "Shoot" in options or "Layup" in options:
            if newAction == "Move" or newAction == "Back-Out":
                options = spots[1:14]
                if currentSpot in options:
                    options.remove(currentSpot)
                makeOptions(options)
            elif newAction == "Drive":
                options = spots[14:]
                makeOptions(options)
            elif newAction == "Dribble":
                options = ["Stepback", "Crossover", "Hesitation"]
                makeOptions(options)
            else:
                response("cpu", "defense", newAction, currentSpot)
        elif "Steal" in options or "Contest" in options:
            success(newAction, actionL.cget("text").split(' ')[-1])
        elif newAction in spots:
            if newAction in spots[:14]:
                userTargetSpot = newAction
                if currentSpot in spots[9:]:
                    newAction = "Back-Out"
                else:
                    newAction = "Move"
            elif newAction in spots[14:]:
                userTargetSpot = newAction
                newAction = "Drive"
            response("cpu", "defense", newAction, currentSpot)
        elif newAction == "Stepback" or newAction == "Crossover" or newAction == "Hesitation":
            userDribbleMove = newAction
            newAction = 'Dribble'
            response('cpu', "defense", newAction, currentSpot)
    actionED.delete(0, END)
confirmBtn = Button(b, text="Confirm", command=confirm).grid(row=2, column=0)

playByPlay = ttk.Treeview(b, columns=("You", "Score", "Opp"), show="headings")
playByPlay.grid(row=20, column=0)
playByPlay.column("You", anchor=CENTER, width=200)
playByPlay.column("Score", anchor=CENTER, width=98)
playByPlay.column("Opp", anchor=CENTER, width=200)
playByPlay.heading("You", text="You")
playByPlay.heading("Score", text="Score")
playByPlay.heading("Opp", text="Opp")

ratingTree2 = ttk.Treeview(b, columns=("You", "Rating", "Opp"), show="headings")
ratingTree2.grid(row=21, column=0)
ratingTree2.column("You", anchor=CENTER, width=50)
ratingTree2.column("Rating", anchor=CENTER, width=100)
ratingTree2.column("Opp", anchor=CENTER, width=50)
ratingTree2.heading("You", text="You")
ratingTree2.heading("Rating", text="Rating")
ratingTree2.heading("Opp", text="Opp")

for rating in user.keys():
    ratingTree.insert("", END, values=(user[rating], rating, cpu["ratings"][rating]))
    ratingTree2.insert("", END, values=(user[rating], rating, cpu["ratings"][rating]))

def replaceThis(choice):
    actionED.delete(0, END)
    actionED.insert(0, choice)
def fuckThis(choice):
    return lambda: replaceThis(choice)
def makeOptions(choices):
    finalRow = b.grid_size()[1]
    for row in range(3, finalRow + 1):
        for item in b.grid_slaves(row):
            if type(item) == Button:
                item.destroy()
    for row, choice in enumerate(choices, 3):
        Button(b, text=choice, command=fuckThis(choice), width=20).grid(row=row,column=0)
    finalRow = b.grid_size()[1]
def cpuTendency(realOptions):
    tendeciesUsed = []
    for thing in realOptions:
        if thing == "Shoot" or thing == "Layup" or thing == "Dunk":
            tendeciesUsed.append(cpu["tendencies"][currentSpot])
        else:      
            tendeciesUsed.append(cpu["tendencies"][thing])
    return choices(realOptions, weights=tendeciesUsed)[0]
def calculationsAndShit(*ratings):
    global userAnkleBroken, cpuAnkleBroken, userStealAttempt, cpuStealAttempt, userStealAttemptFail, cpuStealAttemptFail, userDunkAttempt, cpuDunkAttempt
    if len(ratings) == 2:
        if 20 <= ratings[0] - ratings[1] < 100:
            weight1, weight2 = 0.9, 0.1
        elif 0 <= ratings[0] - ratings[1] < 20:
            weight1, weight2 = 0.8, 0.2
        elif -20 <= ratings[0] - ratings[1] < 0:
            weight1, weight2 = 0.65, 0.35
        elif -100 <= ratings[0] - ratings[1] < -20:
            weight1, weight2 = 0.4, 0.6

        chance = (ratings[0] * weight1) - (ratings[1] * weight2)

    elif len(ratings) == 3:
        rating = (ratings[0] + ratings[1])/2
        if 20 <= rating - ratings[2] < 100:
            weight1, weight2 = 0.9, 0.1
        elif 0 <= rating - ratings[2] < 20:
            weight1, weight2 = 0.8, 0.2
        elif -20 <= rating - ratings[2] < 0:
            weight1, weight2 = 0.65, 0.35
        elif -100 <= rating - ratings[2] < -20:
            weight1, weight2 = 0.4, 0.6

        chance = (rating * weight1) - (ratings[2] * weight2)

    if userDunkAttempt:
        if user["Dunk"] in range(1, 20):
            change = -10
        elif user["Dunk"] in range(20, 40):
            change = -5
        elif user["Dunk"] in range(40, 50):
            change = 1
        elif user["Dunk"] in range(50, 60):
            change = 5
        elif user["Dunk"] in range(60, 70):
            change = 10
        chance += change

    if cpuDunkAttempt:
        if cpu["ratings"]["Dunk"] in range(1, 20):
            change = -10
        elif cpu["ratings"]["Dunk"] in range(20, 40):
            change = -5
        elif cpu["ratings"]["Dunk"] in range(40, 50):
            change = 1
        elif cpu["ratings"]["Dunk"] in range(50, 60):
            change = 5
        elif cpu["ratings"]["Dunk"] in range(60, 70):
            change = 10
        chance += change

    # if userStealAttempt or cpuStealAttempt:
    #   if userStealAttemptFail or cpuStealAttemptFail:
    #     chance +=10
    #     userStealAttempt, cpuStealAttempt = False, False
      
    if userAnkleBroken or cpuAnkleBroken:
        chance += 20
        userAnkleBroken, cpuAnkleBroken = False, False
    a = randint(0, 100)
    print(a, chance)
    if a < chance:
        return True
    else:
        return False
def offRebound(): 
    if choices([0, 1], weights=[60,40])[0] == 0:
      return True
    else:
      return False
def findGIF(action):
    pass
    # path = fr"C:\Users\dinos\Videos\Coding Stuff\bball game v4 1v1 edition\clips\{action}"
    # fileList = os.listdir(path)
    # chosen = choice(fileList)
    # gifSetup(action, chosen)

userDunkAttempt = False
cpuDunkAttempt = False
userStealAttemptFail = False
cpuStealAttemptFail = False
userStealAttempt = False
cpuStealAttempt = False
userAnkleBroken = False
cpuAnkleBroken = False
userDribbleMove = ''
cpuDribbleMove = ''    
def success(userAction, cpuAction):
    print(cpuAction)
    global userTargetSpot, userDribbleMove, cpuDribbleMove, currentSpot, userAnkleBroken, cpuAnkleBroken, userStealAttempt, cpuStealAttempt, userStealAttemptFail, cpuStealAttemptFail, userDunkAttempt, cpuDunkAttempt
    if userAction == "Shoot" or userAction == "Layup" or userAction == "Dunk":
        if userAction == "Dunk":
                userDunkAttempt == True
        if cpuAction == "Contest":
            if calculationsAndShit(user[currentSpot], user["Contested"], cpu["ratings"]['Contest']):
                if currentSpot in spots[:9]:    
                    score[0] += 3
                    if currentSpot in spots[:4]:
                        findGIF("Deep3s")
                    else:
                        findGIF("Contested 3s")
                else:
                    score[0] += 2
                    match userAction:
                        case "Shoot":
                            findGIF("Mid Range")
                        case "Layup":
                            findGIF("Layups")
                        case "Dunk":
                            findGIF("Poster Dunks")
                messagebox.showinfo("Notice", f"You scored. You - {score[0]}  :  {score[1]} - Opp")
                playByPlay.insert('', END, values=(f"Scored from {currentSpot}", f"{score[0]} - {score[1]}", ""))
                gameEnd()
                currentSpot = spots[4]
                response("cpu", "offense", "wtv", currentSpot)
            else:  
              if randint(0, 100) < cpu["ratings"]["Block"]:
                userBlocked = True
                # findGIF("Blocks") do i want to show clips for cpu???
                messagebox.showinfo("Notice", "You got blocked.")
                playByPlay.insert('', END, values=(f"Missed from {currentSpot}", f"{score[0]} - {score[1]}", "Blocked"))  
              else:
                userBlocked = False
                messagebox.showinfo("Notice", "You missed.")
                playByPlay.insert('', END, values=(f"Missed from {currentSpot}", f"{score[0]} - {score[1]}", ""))
              if offRebound():
                  messagebox.showinfo("Notice", "You got the rebound.")
                  playByPlay.insert('', END, values=("Offensive Rebound", f"{score[0]} - {score[1]}", ""))
                  if not userBlocked:
                    currentSpot = spots[randint(14,17)] # might make it anywhere on the court tbh cuz long rebounds.
                  response("user", "offense", "wtv", currentSpot)
              else:
                  messagebox.showinfo("Notice", "Your opponent got the rebound.")
                  playByPlay.insert('', END, values=("", f"{score[0]} - {score[1]}", "Defensive Rebound"))
                  if not userBlocked:
                    currentSpot = spots[4]
                  response("cpu", "offense", "wtv", currentSpot)
        elif cpuAction == "Position for Rebound":
            if randint(0, 100) < user[currentSpot]:
                if currentSpot in spots[:9]:    
                    score[0] += 3
                    if currentSpot in spots[:4]:
                        findGIF("Deep3s")
                    else:
                        findGIF("3s")
                else:
                    score[0] += 2
                    match userAction:
                        case "Shoot":
                            findGIF("Mid Range")
                        case "Layup":
                            findGIF("Layups")
                        case "Dunk":
                            findGIF("Dunks")    
                messagebox.showinfo("Notice", f"You scored. You - {score[0]}  :  {score[1]} - Opp")
                playByPlay.insert('', END, values=(f"Scored from {currentSpot}", f"{score[0]} - {score[1]}", ""))
                gameEnd()
                currentSpot = spots[4]
                response("cpu", "offense", "wtv", currentSpot)
            else:
              # i MIGHT make it so this still only gives a 90 10 chance of a defensive rebound. idk might be a lil unfair.
              messagebox.showinfo("Notice", "You missed.")
              playByPlay.insert('', END, values=(f"Missed from {currentSpot}", f"{score[0]} - {score[1]}", ""))
              playByPlay.insert('', END, values=("", f"{score[0]} - {score[1]}", "Defensive Rebound"))
              currentSpot = spots[4]
              response("cpu", "offense", "wtv", currentSpot)
    elif userAction == "Dribble":
        if cpuAction == "Steal":
            cpuStealAttempt = True
            if calculationsAndShit(user["Ball Security"], cpu["ratings"]["Steal"]):
                if calculationsAndShit(user[userDribbleMove], cpu["ratings"]["Perimeter D"]):
                    cpuAnkleBroken = True
                    findGIF(userDribbleMove)
                    messagebox.showinfo("Notice", "You broke his ankles.")
                    cpuStealAttemptFail = True
                else:
                    cpuAnkleBroken = False
                    messagebox.showinfo("Notice", "Your crossover had no effect.")
                response("user", "offense", "wtv", currentSpot)
            else:
              messagebox.showinfo("Notice", "You got stripped.")
              playByPlay.insert('', END, values=("Turnover", f"{score[0]} - {score[1]}", "Steal"))
              response("cpu","offense","wtv",currentSpot)
        elif cpuAction == "Do Nothing":
            if calculationsAndShit(user[userDribbleMove], cpu["ratings"]["Perimeter D"]): 
                cpuAnkleBroken = True
                findGIF(userDribbleMove)
                messagebox.showinfo("Notice", "You broke his ankles.")
            else:
                cpuAnkleBroken = False
                messagebox.showinfo("Notice", "Your crossover had no effect.")
            response("user", "offense", "wtv", currentSpot)
    elif userAction == "Move" or userAction == "Back-Out" or userAction == "Drive":
        if cpuAction == "Steal":
            cpuStealAttempt = True
            if calculationsAndShit(user["Ball Security"], cpu["ratings"]["Steal"]):
                currentSpot = userTargetSpot
                actionL.config(text=f"You are now at {currentSpot}. What next?")
                response("user", "offense", "moved", currentSpot)
                cpuStealAttemptFail = True
            else:
              messagebox.showinfo("Notice", "You got stripped.")
              playByPlay.insert('', END, values=("Turnover", f"{score[0]} - {score[1]}", "Steal"))
              response("cpu","offense","wtv",currentSpot)
        elif cpuAction == "Do Nothing":
            if userAction != "Drive":
                currentSpot = userTargetSpot
                actionL.config(text=f"You are now at {currentSpot}. What next?")
                response("user", "offense", "moved", currentSpot)
            else:
                if calculationsAndShit(user["Drive"], cpu["ratings"]["Interior D"]):
                    currentSpot = userTargetSpot
                    actionL.config(text=f"You are drove to {currentSpot}. What next?")
                    response("user", "offense", "moved", currentSpot)
                else:
                    actionL.config(text=f"You are still at {currentSpot}. What now?")
                    messagebox.showinfo("Notice", "Your drive was shut off.")
                    response("user", "offense", "moved", currentSpot)

    if cpuAction == "Shoot" or cpuAction == "Layup" or cpuAction == "Dunk":
        if cpuAction == "Dunk":
                cpuDunkAttempt == True
        if userAction == "Contest":
            if calculationsAndShit(cpu["ratings"][currentSpot], cpu["ratings"]["Contested"], user['Contest']):
                if currentSpot in spots[:9]:    
                    score[1] += 3
                else:
                    score[1] += 2
                messagebox.showinfo("Notice", f"They scored. You - {score[0]}  :  {score[1]} - Opp")
                playByPlay.insert('', END, values=("", f"{score[0]} - {score[1]}", f"Scored from {currentSpot}"))
                gameEnd()
                currentSpot = spots[4]
                response("user", "offense", "wtv", currentSpot)
            else:
              if randint(0, 100) < user["Block"]:
                cpuBlocked = True
                findGIF("Blocks")
                messagebox.showinfo("Notice", "You blocked him.")
                playByPlay.insert('', END, values=("Blocked", f"{score[0]} - {score[1]}", f"Missed from {currentSpot}"))  
              else:
                cpuBlocked = False  
                messagebox.showinfo("Notice", "They missed.")
                playByPlay.insert('', END, values=("", f"{score[0]} - {score[1]}", f"Missed from {currentSpot}"))
              if offRebound():
                  messagebox.showinfo("Notice", "Your opponent got the rebound.")
                  playByPlay.insert('', END, values=("", f"{score[0]} - {score[1]}", "Offensive Rebound"))
                  if not cpuBlocked:    
                    currentSpot = spots[randint(14,17)] # might make it anywhere on the court tbh cuz long rebounds.
                  response("cpu", "offense", "wtv", currentSpot)
              else:
                  messagebox.showinfo("Notice", "You got the rebound.")
                  playByPlay.insert('', END, values=("Defensive Rebound", f"{score[0]} - {score[1]}", ""))
                  if not cpuBlocked:
                    currentSpot = spots[4]
                  response("user", "offense", "wtv", currentSpot)
        elif userAction == "Position for Rebound":
            if randint(0, 100) < cpu['ratings'][currentSpot]:
                if currentSpot in spots[:9]:    
                    score[1] += 3
                else:
                    score[1] += 2
                messagebox.showinfo("Notice", f"They scored. You - {score[0]}  :  {score[1]} - Opp")
                playByPlay.insert('', END, values=("", f"{score[0]} - {score[1]}", f"Scored from {currentSpot}"))
                gameEnd()
            else:
              messagebox.showinfo("Notice", "They missed.")
              playByPlay.insert('', END, values=("", f"{score[0]} - {score[1]}", f"Missed from {currentSpot}"))
            currentSpot = spots[4]
            response("user", "offense", "wtv", currentSpot)
    elif cpuAction == "Dribble":
        if userAction == "Steal":
            userStealAttempt = True
            if calculationsAndShit(cpu["ratings"]["Ball Security"], user["Steal"]):
                if calculationsAndShit(cpu["ratings"][cpuDribbleMove], user["Perimeter D"]): 
                    userAnkleBroken = True
                    messagebox.showinfo("Notice", "You got dropped, instead.")
                    userStealAttemptFail = True
                else:
                    userAnkleBroken = False
                    messagebox.showinfo("Notice", "You couldn't steal it, but you stayed on your feet.")
                response("cpu", "offense", "wtv", currentSpot)
            else:
                findGIF("Steals")
                messagebox.showinfo("Notice", "You stole the ball.")
                playByPlay.insert('', END, values=("Steal", f"{score[0]} - {score[1]}", "Turnover"))
                response("user","offense","wtv",currentSpot)
        elif userAction == "Do Nothing":
            if calculationsAndShit(cpu["ratings"][cpuDribbleMove], user["Perimeter D"]): 
                userAnkleBroken = True
                messagebox.showinfo("Notice", "You got dropped.")
            else:
                userAnkleBroken = False
                messagebox.showinfo("Notice", "You stayed on your feet.")
            response("cpu", "offense", "wtv", currentSpot)
    elif cpuAction == "Move" or cpuAction == "Back-Out" or cpuAction == "Drive":
        if userAction == "Steal":
            userStealAttempt = True
            if calculationsAndShit(cpu["ratings"]["Ball Security"], user["Steal"]):
                currentSpot = cpuTargetSpot
                response("cpu", "offense", "moved", currentSpot)
                userStealAttemptFail = True
            else:
                findGIF("Steals")
                messagebox.showinfo("Notice", "You stole the ball.")
                playByPlay.insert('', END, values=("Steal", f"{score[0]} - {score[1]}", "Turnover"))
                response("user","offense","wtv",currentSpot)
        elif userAction == "Do Nothing":
            if cpuAction != "Drive":
                currentSpot = cpuTargetSpot
                response("cpu", "offense", "Do Nothing", currentSpot)
            else:
                if calculationsAndShit(cpu["ratings"]["Drive"], user["Interior D"]):
                    currentSpot = cpuTargetSpot
                    response("cpu", "offense", "Do Nothing", currentSpot)
                else:
                    messagebox.showinfo("Notice", "You managed to cut off his drive.")
                    response("cpu", "offense", "Do Nothing", currentSpot)    

options = []
userTargetSpot = ''
cpuTargetSpot = ''
def response(who, possessionType, priorAction, location):
    global options, userTargetSpot, cpuTargetSpot, userDribbleMove, cpuDribbleMove
    if who == "user":
        if possessionType == "offense":
            if priorAction != "jumpball":
                actionL.config(text=f"You are at {currentSpot}. What's your move?")

            if location in spots[0:9]:
                options = ["Shoot", "Dribble", "Move", "Drive"]
            elif location in spots[9:14]:
                options = ["Shoot", "Dribble", "Back-Out", "Drive"]
            elif location in spots[14:]:
                options = ["Layup", "Dunk", "Back-Out"]
        elif possessionType == "defense":
            if priorAction == "Shoot" or priorAction == "Layup" or priorAction == "Dunk":
                options = ["Contest", "Position for Rebound"]
            elif priorAction == "Dribble" or priorAction == "Move" or priorAction == "Back-Out" or priorAction == "Drive":
                options = ["Steal", "Do Nothing"]
        makeOptions(options)
    elif who == "cpu":
        if possessionType == "offense":
            if location in spots[0:9]:
                cpuOptions = ["Shoot", "Dribble", "Move", "Drive"]
            elif location in spots[9:14]:
                cpuOptions = ["Shoot", "Dribble", "Back-Out", "Drive"]
            elif location in spots[14:]:
                cpuOptions = ["Layup", "Dunk", "Back-Out"]
        elif possessionType == "defense":
            if priorAction == "Shoot" or priorAction == "Layup" or priorAction == "Dunk":
                cpuOptions = ["Contest", "Position for Rebound"]
            elif priorAction == "Dribble" or priorAction == "Move" or priorAction == "Back-Out" or priorAction == "Drive":
                cpuOptions = ["Steal", "Do Nothing"]

        decision = cpuTendency(cpuOptions)
        if decision == "Move" or decision == "Back-Out":
            cpuOptions = spots[1:14]
            if currentSpot in cpuOptions:
                cpuOptions.remove(currentSpot)
            cpuTargetSpot = choice(cpuOptions) #might make it based on tendency to shoot there
        elif decision == "Drive":
            cpuOptions = spots[14:]
            cpuTargetSpot = choice(cpuOptions)
        elif decision == "Dribble":
            cpuOptions = ["Stepback", "Crossover", "Hesitation"]
            cpuDribbleMove = cpuTendency(cpuOptions)

        if possessionType == "offense":
            actionL.config(text=f'At {location}, opponent uses: {decision}')
            response("user", "defense", decision, currentSpot)
        elif possessionType == "defense":
            success(priorAction, decision)
def gameEnd():
    if score[0] >= int(gamepointE.get()):
        if score[0] - score[1] > 1:
            messagebox.showinfo("Notice", f"You won with a score of {score[0]} to {score[1]} on {difficultyE1.get()} difficulty!")
            playByPlay.insert('', END, values=("You won", f"{score[0]} - {score[1]}", ""))
            actionED.config(state="disabled")
    elif score[1] >= int(gamepointE.get()):
        if score[1] - score[0] > 1:
            messagebox.showinfo("Notice", f"You lost with a score of {score[1]} to {score[0]} on {difficultyE1.get()} difficulty.") 
            playByPlay.insert('', END, values=("", f"{score[0]} - {score[1]}", "They won"))
            actionED.config(state="disabled")
    
raise_frame(a)
root.mainloop()
