from tkinter import *
from tkinter import messagebox
from datetime import datetime
from datetime import date
from tkinter import filedialog
import tkinter.font as tkFont
import requests
import random

window = Tk()
window.title("Lightshot Link Generator")
window.geometry("230x300")
window.resizable(False, False)

ans = "prnt.sc/"
path = "LightshotImages/"
chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
amount = 0
lossesAmount = 0
generationLimiterValue = BooleanVar()
generationLimiterValue.set(True)

def ChooseDirectory(**path):
    path = filedialog.askdirectory() #requesting the downnloading directory
    print(path)
    return path

def Generate(**ans):
    #generateProgress.start()
    generateResults.configure(state = "normal") #cleaning the text field
    generateResults.delete(1.0, END)
    generateResults.configure(state = "disabled")
    if(generationLimiterValue.get() == 1 and int(generateAmount.get()) > 1500): #checking if higher than limit
        generateResults.configure(state = "normal")
        generateResults.insert(1.0, "Out of the limit!")
        generateResults.configure(state = "disabled")
    else:
        lossesAmount = 0
        logFile = open('log.txt', 'a') #opening the log file
        logFile.write("\n[" + str(date.today()) + "]\n" + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second) + "\n") #writing date
        logFile.write("Generated " + generateAmount.get() + " links\n") #num of generated links
        for i in range(int(generateAmount.get())):
            ans = "prnt.sc/"
            for j in range(6):
                ans = ans + random.choice(chars) #generating a link
            generateResults.configure(state = "normal") #adding to the text field
            generateResults.insert(1.0, ans + '\n')
            generateResults.configure(state = "disabled")
            image_in = requests.get("https://" + ans, headers = {'User-Agent': 'Chrome'}) #reading the html
            image_in_str = str(image_in.text)
            image_in_index = str(image_in_str).find('<img class="no-click screenshot-image" src="') + 44 #index from which searching the image link
            image_in_pre = ""
            while image_in_str[image_in_index] != '"': #finding the image link
                image_in_pre = image_in_pre + image_in_str[image_in_index]
                image_in_index += 1
            try: #trying to get the image url
                image_out_pre = requests.get(image_in_pre, headers = {'User-Agent': 'Chrome'})
                image_out = open(path + "image" + str(i) + ".png", "wb") #downloading the image
                image_out.write(image_out_pre.content)
                image_out.close()
            except:
                lossesAmount += 1
                messagebox.showerror(title = "Error occured", message = "An error occured during downloading an image")
        logFile.write("Losses: " + str(float(lossesAmount) / float(generateAmount.get()) * 100) + "%\n")
        logFile.close()
        messagebox.showinfo(title = "Complete", message = "Generation and downoloading complete")

generateFont = tkFont.Font(family = "Arial", size = 10, weight = "bold")

generateButton = Button(window, width = 11, height = 2, text = "Generate", font = generateFont, command = lambda:Generate())
generateDirectoryButton = Button(window, width = 11, height = 2, text = "Save to...", font = generateFont, command = lambda:ChooseDirectory())
generateAmount = Spinbox(window, from_=0, to = 1000, width = 15, textvariable = amount)
generateResults = Text(window, width = 16, height = 10, border = 4, state = "disabled")
generateLimiter = Checkbutton(window, text = "Limiter", var = generationLimiterValue, font = generateFont,)
generateResultsScrollbar = Scrollbar(window, orient = "vertical", command = generateResults.yview)

generateAmount.grid(column = 1, row = 1)
generateButton.grid(column = 2, row = 1)
generateResults.grid(column = 1, row = 3)
generateLimiter.grid(column = 1, row = 2)
generateDirectoryButton.grid(column = 2, row = 2)

window.mainloop()