from ctypes import windll
import random
import tkinter as tk
import time
import math
from PIL import Image, ImageTk

print("blohai :3")

x = random.randint(200, 1300)
y = random.randint(100, 500)  
state = 1
gifPath = 'C:\\Users\\bramb\\OneDrive\\Documents\\VSCode\\desktop pet blahaj\\gifs\\'
lastSleep = 0 
sleepLength = 0  
screenWidth, screenHeight = 1520, 800  
lastDirection = "right" # Direction blahaj was facing
swimTime = 0 
animationLocked = False
idlePhase = 0
lastIdle = "idle"
dragX = dragY = 0
isDragging = False 

# Window config
window = tk.Tk()
window.title("Desktop Pet")
window.geometry(f"{screenWidth}x{screenHeight}+0+0")
window.overrideredirect(True)  # No toolbar
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

# Drag pet with mouse
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

label.bind("<Button-1>", dragStart)   
label.bind("<B1-Motion>", drag)  
label.bind("<ButtonRelease-1>", dragEnd)


# Load and gifs
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

currIdle = idles["idle_right"]
frameIndex = 0  # Frame counter
frames = []


# Choose idle animation
def setIdleAnim():
    global currIdle, lastDirection, lastIdle
    num = random.randint(1, 16)
    if num == 11 and lastIdle != "idle_plant":
        lastDirection = "right"
        lastIdle = "idle_plant"
        currIdle = idles["idle_plant"]
    elif num == 12 and lastIdle != "idle_music":
        lastDirection = "right"
        lastIdle = "idle_music"
        currIdle = idles["idle_music"]
    elif num == 13 and lastIdle != "idle_candy":
        lastDirection = "right"
        lastIdle = "idle_candy"
        currIdle = idles["idle_candy"]
    elif num == 14 and lastIdle != "idle_fish":
        lastDirection = "right"
        lastIdle = "idle_fish"
        currIdle = idles["idle_fish"]

    else:
        if(lastDirection == "right"):
            currIdle = idles["idle_right"]
        elif(lastDirection == "left"):
            currIdle = idles["idle_left"]
    return currIdle 

# Updates the animation and position of the pet
def behavior():
    global state, x, y, lastSleep, sleepLength, currIdle, lastDirection, frameIndex, currIdle, frames, swimTime, animationLocked, idlePhase, isDragging
    
    if not animationLocked: 
        # currGifs based on the current state
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

        elif state == 4:  # Swimming left
            lastDirection = "left"
            frames = swim_left    
        
        elif state == 5:  # Swimming right
            lastDirection = "right"
            frames = swim_right
        
        animationLocked = True
    
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
    
    window.after(80, behavior) 

# Behavior transitions
def event():
    global state, lastSleep, currIdle, swimTime, lastDirection, animationLocked
    eventNum = random.randint(1, 20) 

    # to sleep
    if eventNum in [12, 13] and (time.time() - lastSleep > 10) and state == 0: 
        swimTime = 0
        state = 1

    # swim left 
    elif (eventNum in [9, 10, 17, 18, 19] and x >= 200) or x >= (screenWidth - 350): 
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
    if eventNum <= 8:
        swimTime = 0
        if state == 0: 
            setIdleAnim()
        else:
            if(lastDirection == "right"):
                currIdle = idles["idle_right"]
            elif(lastDirection == "left"):
                currIdle = idles["idle_left"]
        state = 0
        
    # wake up
    elif eventNum == 20 and state == 2:  
        swimTime = 0
        state = 3
    
    window.after(500, event)  

# Return to idle after sleeping
def wakeUp():
    global state
    state = 0    

# Start the main animation and event loops
window.after(80, behavior)
window.after(500, event)
window.mainloop()
