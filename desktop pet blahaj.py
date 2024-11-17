from ctypes import windll
import random
import tkinter as tk
import time
import math
from PIL import Image, ImageTk
from collections import deque

print("blohai :3")

x = random.randint(200, 1300)
y = random.randint(100, 500)  
state = 1
gifPath = 'C:\\Users\\bramb\\OneDrive\\Documents\\VSCode\\desktop pet blahaj\\gifs\\'
lastSleep = 0 
sleepLength = 0  
screenWidth, screenHeight = 1520, 800  # Hard coded since the regular screen doesn't work 
lastDirection = "right" # Direction blahaj was facing
swimTime = 0 
animationLocked = False
idlePhase = 0
lastIdle = "idle"
dragX = dragY = 0
isDragging = False 
eventNum = 1
eventQueue = deque() 
hoverStartTime = None 
lastPetTime = 0 

# Window config
window = tk.Tk()
window.title("Desktop Pet")
window.geometry(f"{screenWidth}x{screenHeight}+0+0")
window.overrideredirect(True)  
window.attributes('-topmost', True) 
window.config(bg='black')
window.wm_attributes('-transparentcolor', 'black') 

# Pet container in window
label = tk.Label(window, bd=0, bg='black')
label.place(x=x, y=y)

# Control backslash to close program
def close_program(event=None):
    print("Closing program")
    window.destroy()
window.bind("<Control-q>", close_program)

# Pet interactions
def dragStart(event):
    global dragX, dragY, isDragging
    dragX = event.x
    dragY = event.y
    isDragging = True

def drag(event):
    global x, y
    newX = label.winfo_x() + (event.x - dragX)
    newY = label.winfo_y() + (event.y - dragY)
    x = newX
    y = newY
    label.place(x=x, y=y)

def dragEnd(event):
    global isDragging
    isDragging = False 

def hoverStart(event):
    global hoverStartTime
    hoverStartTime = time.time()

def hoverEnd(event):
    global hoverStartTime
    hoverStartTime = None

def hover():
    global hoverStartTime, lastPetTime, animationLocked, frames, state
    if hoverStartTime and (state in [0, 4, 5]  ) and (time.time() - hoverStartTime) >= 2 and (time.time() - lastPetTime) >= 20:
        lastPetTime = time.time()
        animationLocked = True
        state = 6
        hoverStartTime = None  
    window.after(100, hover)

label.bind("<Enter>", hoverStart)
label.bind("<Leave>", hoverEnd)
label.bind("<Button-1>", dragStart)   
label.bind("<B1-Motion>", drag)  
label.bind("<ButtonRelease-1>", dragEnd)

# Load gifs
def loadGif(file_path):
    imagePil = Image.open(file_path)
    frames = []
    try:
        while True:
            frame = ImageTk.PhotoImage(imagePil.copy().convert("RGBA"))
            frames.append(frame)
            imagePil.seek(len(frames))  # Move to the next frame
    except EOFError:
        pass 
    except (FileNotFoundError, IOError):
        print(f"Error! Couldn't load {file_path}")
        return []
    return frames

# Load animations as lists of frames
idles = {
    "idle_right": loadGif(gifPath + 'idle.gif'),
    "idle_left": loadGif(gifPath + 'idleLeft.gif'), 
    "idle_plant": loadGif(gifPath + 'idle_plant.gif'),
    "idle_music": loadGif(gifPath + 'idle_music.gif'),
    "idle_candy": loadGif(gifPath + 'idle_candy.gif'),
    "idle_fish": loadGif(gifPath + 'idle_fish.gif')
}

to_sleep = loadGif(gifPath + 'to_sleep.gif')
sleeping = loadGif(gifPath + 'sleeping.gif')
to_awake = loadGif(gifPath + 'to_awake.gif')
swim_right = loadGif(gifPath + 'swim_right.gif')
swim_left = loadGif(gifPath + 'swim_left.gif')
happy = loadGif(gifPath + 'happy.gif')

currIdle = idles["idle_right"]
frameIndex = 0  # Frame counter
frames = []

# Choose idle animation
def setIdleAnim():
    global currIdle, lastDirection, lastIdle

    thoughts = {
        11: ("idle_plant", idles["idle_plant"]),
        12: ("idle_music", idles["idle_music"]),
        13: ("idle_candy", idles["idle_candy"]),
        14: ("idle_fish", idles["idle_fish"])
    }

    num = random.randint(1, 16)

    if (num in [12, 14]) and lastIdle != thoughts[num][0]:
        lastIdle, currIdle = thoughts[num]
        lastDirection = "right"  

    elif (num in [11, 13]) and lastIdle != thoughts[num][0]:
        lastIdle, currIdle = thoughts[num]
        lastDirection = "left"

    else:
        currIdle = idles[f"idle_{lastDirection}"]

    return currIdle

# Updates the animation and pet position
def behavior():
    global state, x, y, eventQueue, lastSleep, sleepLength, currIdle, lastDirection, frameIndex, currIdle, frames, swimTime, animationLocked, idlePhase, isDragging
    
    if not animationLocked: 
        if state == 0:  # Idle
            frames = setIdleAnim()

        elif state == 1:  # Idle to sleep
            frames = to_sleep
            lastSleep = time.time()
            sleepLength = random.randint(10, 60) * 1000 
            state = 2

        elif state == 2:  # Sleeping
            frames = sleeping
            if (time.time() - lastSleep) >= sleepLength / 1000:  
                state = 3
            else: state = 2

        elif state == 3:  # Waking up
            frames = to_awake
            eventQueue.append(1)

        elif state == 4:  # Swimming left
            lastDirection = "left"
            frames = swim_left    
        
        elif state == 5:  # Swimming right
            lastDirection = "right"
            frames = swim_right
        
        elif state == 6: # Happy
            lastDirection = "right"
            frames = happy 
        
        animationLocked = True

        if state == 6 and frameIndex == len(frames) - 1:
            animationLocked = False 
            state = 0    
    
    # Have movement during idle and swimming animations
    if state == 0:
        if y <= 10:
            y += 2
        elif y >= (screenHeight - 118):
            y -= 2
        else:
            y += math.sin(idlePhase) * 4
            idlePhase += 1  

    elif frames == swim_left:
        x = max(x - 10, 10)
        y = min(max(y + random.choice([-6, 6]), 10), screenHeight - 110) 
        if (time.time() - swimTime) <= 2:
            state = 4
    
    elif frames == swim_right:
        x = min(x + 10, screenWidth - 220) 
        y = min(max(y + random.choice([-6, 6]), 10), screenHeight - 110) 
        if (time.time() - swimTime) <= 2:
            state = 5

    x = max(0, min(x, screenWidth - 220))
    y = max(0, min(y, screenHeight - 110))

    if not isDragging:
        label.place(x=x, y=int(y))

    # Play frames 
    frameIndex = (frameIndex + 1) % len(frames)
    label.configure(image=frames[frameIndex])
    label.image = frames[frameIndex]

    # Unlock after last frame
    if frameIndex == len(frames) - 1:
        animationLocked = False
    
    window.after(100, behavior) 

# Queue for changes in behavior 
def queueEvent(): 
    global state, lastSleep, currIdle, swimTime, lastDirection, animationLocked, eventNum

    if animationLocked:
        window.after(800, queueEvent)
        return

    if eventQueue:
        nextEvent = eventQueue.popleft()
        event(nextEvent)
    else:
        eventNum = random.randint(1, 20)
        eventQueue.append(eventNum)

    window.after(500, queueEvent)

# Behavior transitions
def event(queued):
    global state, lastSleep, currIdle, swimTime, lastDirection, animationLocked, eventNum

    eventNum = queued 
    # to sleep
    if eventNum in [12, 13] and (time.time() - lastSleep > 10) and state == 0: 
        swimTime = 0
        state = 1

    # swim left 
    elif (eventNum in [10, 17, 18, 19, 20] and x >= 200) or x >= (screenWidth - 350): 
        if swimTime == 0:
            swimTime = time.time()
        lastDirection = "left"
        state = 4
        
    # swim right 
    elif (eventNum in [11, 14, 15, 16] and x <= (screenWidth - 210)) or x >= 150: 
        if swimTime == 0:
            swimTime = time.time()
        lastDirection = "right" 
        state = 5
    
    # idle animations
    if eventNum <= 9:
        swimTime = 0
        if state == 0: 
            setIdleAnim()
        else:
            if(lastDirection == "right"):
                currIdle = idles["idle_right"]
            elif(lastDirection == "left"):
                currIdle = idles["idle_left"]
        state = 0

# Return to idle after sleeping
def wakeUp():
    global state
    state = 0    

# Start the main animation and event loops
window.after(100, behavior)
window.after(100, hover)  
window.after(500, queueEvent)
window.mainloop()
