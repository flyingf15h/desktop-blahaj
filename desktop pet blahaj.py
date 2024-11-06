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

# Updates the animation and position of the pet
def behavior():
    global state, x, y, lastSleep, sleepLength, currIdle, lastDirection, frameIndex, currIdle, frames
    
    # currGifs based on the current state
    if state == 0:  # Idle
        frames = currIdle

    elif state == 1:  # Idle to sleep
        frames = to_sleep
        lastSleep = time.time()
        sleepLength = random.randint(20, 100) * 1000  # 20-100 seconds in ms
        state = 2
        window.after(sleepLength, wakeUp)  # Schedule wake-up

    elif state == 2:  # Sleeping
        frames = sleeping
        state = 2

    elif state == 3:  # Waking up
        frames = to_awake

    elif state == 4:  # Swimming left
        lastDirection = "left"
        frames = swim_left
        x = max(x - 10, 100)
        y = min(max(y + random.choice([-10, 10]), 200), screen_height - 200) 
        # Go in other direction if out of bounds
        if y >= screen_height - 200:
            y -= 20
        elif y <= 200:
            y += 20
        if x <= 200:
            x += 20
            state = 5        
        
    elif state == 5:  # Swimming right
        lastDirection = "right"
        frames = swim_right
        x = min(x + 10, screen_width - 100) 
        y = min(max(y + random.choice([-10, 10]), 200), screen_height - 200) 
        if y >= screen_height - 200:
            y -= 20
        elif y <= 200:
            y += 20
        # Go in other direction if out of bounds
        if x >= screen_width - 200:
            x -= 20
            state = 4
        
    # Cycle through frames and update window
    if frames:
        frameIndex = (frameIndex + 1) % len(frames)
        label.configure(image=frames[frameIndex])
        label.image = frames[frameIndex]

    window.geometry(f'210x118+{x}+{y}')
    window.after(100, behavior) 

# Behavior transitions
def event():
    global state, lastSleep, currIdle
    eventNum = random.randint(1, 14)
    currentTime = time.time()

    # idle animations
    if eventNum <= 8: 
        if state == 0:
            idle_choice = random.randint(1, 16)
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
        else:
            if(lastDirection == "right"):
                currIdle = idle_gifs["idle_right"]
            elif(lastDirection == "left"):
                currIdle = idle_gifs["idle_left"]
        state = 0

    # to sleep
    elif eventNum == 9 and (currentTime - lastSleep > 180) and state == 0: 
        state = 1

    # swim right 
    elif eventNum in [10, 11]:  
        state = 5

    # swim left 
    elif eventNum in [12, 13]: 
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
window.after(100, behavior)
window.after(500, event)
window.mainloop()
