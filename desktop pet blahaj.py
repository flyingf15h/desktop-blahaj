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
screen_width, screen_height = 1920, 1080  
lastDirection = "right" # Direction blahaj was facing
swimTime = 0 

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
idle_gifs = {
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

currIdle = idle_gifs["idle_right"]
frameIndex = 0  # Frame counter
frames = []

# Choose idle animation
def set_idle_animation():
    global currIdle
    idle_choice = random.randint(1, 6)
    if idle_choice == 1:
        currIdle = idle_gifs["idle_plant"]
    elif idle_choice == 2:
        currIdle = idle_gifs["idle_music"]
    elif idle_choice == 3:
        currIdle = idle_gifs["idle_candy"]
    elif idle_choice == 4:
        currIdle = idle_gifs["idle_fish"]
    else:
        if(lastDirection == "right"):
            currIdle = idle_gifs["idle_right"]
        elif(lastDirection == "left"):
            currIdle = idle_gifs["idle_left"]
    return currIdle 

# Updates the animation and position of the pet
def behavior():
    global state, x, y, lastSleep, sleepLength, currIdle, lastDirection, frameIndex, currIdle, frames, swimTime, animationLocked
    
    # currGifs based on the current state
    if state == 0:  # Idle
        frames = set_idle_animation()
        y =  min(max(y + random.choice([-1, 1]), 200), screen_height - 200)

    elif state == 1:  # Idle to sleep
        frames = to_sleep
        lastSleep = time.time()
        sleepLength = random.randint(20, 100) * 1000 
        window.after(sleepLength, wakeUp) 
        state = 2

    elif state == 2:  # Sleeping
        frames = sleeping

    elif state == 3:  # Waking up
        frames = to_awake

    elif state == 4:  # Swimming left
        if swimTime == 0:
                swimTime = time.time(); 
        lastDirection = "left"
        frames = swim_left
        x = max(x - 10, 100)
        y = min(max(y + random.choice([-6, 6]), 200), screen_height - 210) 
        # Go in other direction if out of bounds
        if y >= screen_height - 210:
            y -= 20
        elif y <= 100:
            y += 20
        if x <= 100:
            x += 20
            state = 5    
        if (time.time() - swimTime) <= 2:
            state = 4    
        
    elif state == 5:  # Swimming right
        if swimTime == 0:
                swimTime = time.time();
        lastDirection = "right"
        frames = swim_right
        x = min(x + 10, screen_width - 210) 
        y = min(max(y + random.choice([-6, 6]), 200), screen_height - 210) 
        if y >= screen_height - 210:
            y -= 20
        elif y <= 100:
            y += 20
        # Go in other direction if out of bounds
        if x >= screen_width - 210:
            x -= 20
            state = 4
        if (time.time() - swimTime) <= 2:
            state = 5
        
    # Cycle through frames and update window
    frameIndex = (frameIndex + 1) % len(frames)
    label.configure(image=frames[frameIndex])
    label.image = frames[frameIndex]

    window.geometry(f'210x118+{x}+{y}')
    window.after(80, behavior) 

# Behavior transitions
def event():
    global state, lastSleep, currIdle, swimTime
    eventNum = random.randint(1, 20)
    
    # idle animations
    if eventNum <= 15:
        if state == 0: 
            set_idle_animation()
        else:
            if(lastDirection == "right"):
                currIdle = idle_gifs["idle_right"]
            elif(lastDirection == "left"):
                currIdle = idle_gifs["idle_left"]
        state = 0

    # to sleep
    elif eventNum == 16 and (time.time() - lastSleep > 180) and state == 0: 
        state = 1

    # swim right 
    elif eventNum in [17, 18] and x <= (screen_width - 200): 
        swimTime = 0 
        state = 5

    # swim left 
    elif eventNum in [19, 20] and x >= 100: 
        swimTime = 0
        state = 4

    # wake up
    elif eventNum == 14:  
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
