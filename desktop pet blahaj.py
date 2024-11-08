from ctypes import windll
import random
import tkinter as tk
import time
from PIL import Image, ImageTk

print("blohai :3")

x = random.randint(200, 1300)
y = random.randint(100, 500)  
state = 1
gifPath = 'C:\\Users\\bramb\\OneDrive\\Documents\\VSCode\\desktop pet blahaj\\gifs\\'
lastSleep = 0 
sleepLength = 0  
screenWidth, screenHeight = 1920, 1080  
lastDirection = "right" # Direction blahaj was facing
swimTime = 0 
animationLocked = False

# Window config
window = tk.Tk()
window.config(highlightbackground='black')
window.wm_attributes('-transparentcolor', 'black')
window.title("Desktop Pet")
window.geometry("210x118")  
# Set window icon (doesn't do anything rn because overridedirect is on)
icon = tk.PhotoImage(file = gifPath + 'petIcon.png')
window.iconphoto(True, icon)
# No toolbar on top of blahaj window but keep window on top
window.overrideredirect(True)
window.attributes('-topmost', True) 

# Control backslash to close program
def close_program(event=None):
    print("Closing program")
    window.destroy()
window.bind("<Control-q>", close_program)

label = tk.Label(window, bd=0, bg='black')
label.pack()

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
    global currIdle, lastDirection
    num = random.randint(1, 16)
    if num == 11:
        lastDirection = "right"
        currIdle = idles["idle_plant"]
    elif num == 12:
        lastDirection = "right"
        currIdle = idles["idle_music"]
    elif num == 13:
        lastDirection = "right"
        currIdle = idles["idle_candy"]
    elif num == 14:
        lastDirection = "right"
        currIdle = idles["idle_fish"]
    else:
        if(lastDirection == "right"):
            currIdle = idles["idle_right"]
        elif(lastDirection == "left"):
            currIdle = idles["idle_left"]
    return currIdle 

# Updates the animation and position of the pet
def behavior():
    global state, x, y, lastSleep, sleepLength, currIdle, lastDirection, frameIndex, currIdle, frames, swimTime, animationLocked
    
    if not animationLocked: 
        # currGifs based on the current state
        if state == 0:  # Idle
            frames = setIdleAnim()

        elif state == 1:  # Idle to sleep
            frames = to_sleep
            lastSleep = time.time()
            sleepLength = random.randint(20, 100) * 1000 
            window.after(sleepLength, wakeUp) 
            state = 2

        elif state == 2:  # Sleeping
            frames = sleeping
            state = 2

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
        y =  min(max(y + random.choice([-1, 1]), 200), screenHeight - 200)

    elif frames == swim_left:
        x = max(x - 10, 200)
        y = min(max(y + random.choice([-6, 6]), 200), screenHeight - 210) 
        if (time.time() - swimTime) <= 2:
            state = 4
    
    elif frames == swim_right:
        x = min(x + 10, screenWidth - 210) 
        y = min(max(y + random.choice([-6, 6]), 200), screenHeight - 300) 
        if (time.time() - swimTime) <= 2:
            state = 5
    
    # Go in other direction if out of bounds
    if y >= screenHeight - 210:
        y -= 10
    elif y <= 100:
        y += 10

    # Play frames 
    frameIndex = (frameIndex + 1) % len(frames)
    label.configure(image=frames[frameIndex])
    label.image = frames[frameIndex]

    # Unlock after last frame
    if frameIndex == len(frames) - 1:
        animationLocked = False
    
    window.geometry(f'210x118+{x}+{y}')
    window.after(80, behavior) 

# Behavior transitions
def event():
    global state, lastSleep, currIdle, swimTime, lastDirection, animationLocked
    eventNum = random.randint(1, 20) 

    # to sleep
    if eventNum in [12, 13] and (time.time() - lastSleep > 10) and state == 0: 
        swimTime = 0
        state = 1

    # swim right 
    elif (eventNum in [14, 15, 16] and x <= (screenWidth - 210)) or x >= 150: 
        if swimTime == 0:
            swimTime = time.time()
        lastDirection = "right" 
        state = 5

    # swim left 
    elif (eventNum in [17, 18, 19] and x >= 200) or x >= (screenWidth - 300): 
        if swimTime == 0:
            swimTime = time.time()
        lastDirection = "left"
        state = 4

    # idle animations
    if eventNum <= 11:
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
