import speech_recognition as sr
from cmu_graphics import *
from PIL import Image

words = open("bad-words.txt").read().splitlines()
PROFANITY_SET = set(words)

# Initialize the recognizer
r = sr.Recognizer()

def is_profane(text):
    for word in text.split(' '):
        for profane_word in PROFANITY_SET:
            if word.lower() == profane_word:
                return True
    return False

def onAppStart(app):
    app.logo = Image.open("mellontalk.jpeg")
    app.imageWidth,app.imageHeight = app.logo.width,app.logo.height
    app.logo = CMUImage(app.logo)

    app.width = 800
    app.height = 800
    app.is_paused = False
    app.speaker = 1
    app.timepassed = 0
    app.text = ""
    app.usernames = ['chrissy', 'swandy']
    app.notUnderstood = False
    # app.prevMessages = []
    app.prevMessages = [] # if length greater than 16, .pop(0)
    app.welcome = True
    app.textboxes = [TextBox(0,app), TextBox(1,app)]

class TextBox:
    def __init__(self,user, app):
        self.left = user * app.width/2 + app.width/18
        self.top = app.height * 11/12 + 15
        self.width =  app.width/2 - app.width/9
        self.height = app.height /12 - 30

    
def redrawAll(app):
    ###################################
    # Welcome Screen
    if app.welcome:
        newWidth, newHeight = (app.imageWidth*3/4,app.imageHeight*3/4)
        drawRect(0,0,app.width,app.height,fill = 'lightyellow')
        drawImage(app.logo, app.width/2 - newWidth/2,100, width = newWidth, height = newHeight)
        drawLabel('MellonTalk is designed to bridge gaps and foster understanding among diverse communities.',app.width/2, 50, size = 18, font = 'Didot')
        drawLabel('This platform leverages advanced communication technologies',app.width/2, 500, size = 18, font = 'Didot')
        drawLabel('to create a safe, inclusive environment',app.width/2, 530, size = 18, font = 'Didot')
        drawLabel('where individuals from different backgrounds can share, learn, and grow together.',app.width/2, 560, size = 18, font = 'Didot')
        drawLabel('If you receive a message with profanity, press space to see it.',app.width/2, 630, size = 18, font = 'Didot',fill = rgb(252,71,51))
        drawLabel("The person won't be able to send another message.",app.width/2, 660, size = 18, font = 'Didot',fill = rgb(252,71,51))
        
        drawLabel('Press Enter to Continue',app.width/2,app.height - 80, size = 50,font = 'Didot' )
    ###################################
    else:
        reddishPink = rgb(252,71,51)
        for i in range(2):
            if i == 0:
                color = 'pink'
            else:
                color = 'lavenderblush'
        
            drawRect(app.width/2*i,0,app.width/2,app.height,fill = color)
            drawRect(app.width/2*i,0,app.width/2,app.height/12,fill = 'white')
            drawLabel(f'{app.usernames[i]}',app.width/2 * i + app.width/12, app.height/24, size = 30, font = 'Noteworthy')
            drawRect(app.width/2*i, app.height* 11/12,app.width/2,app.height/12,fill = 'white')
            textBox = app.textboxes[i]
            drawRect(textBox.left,textBox.top, textBox.width,textBox.height ,fill = 'white')
            drawLabel('Speaking', i * app.width/2 + app.width/4 , app.height * 11/12 + 30, size = 20, fill = 'crimson', font = 'Noteworthy')
            
            for j in range(len(app.prevMessages)):
                user, message = app.prevMessages[j]
                startY = 80
            
                if user != i:
                    # left
                    drawRect(app.width/2 * i + 10, startY + 41 * j, len(message)*15, 30,fill = reddishPink)
                    drawLabel(f'{app.usernames[i]}',app.width/2 * i + 12, startY + 41 * j - 7, size = 10, align = 'left',fill = 'black', font = 'Noteworthy')
                    drawLabel(message.capitalize(), app.width/2 * i + 20 , startY + 41 * j + 15, size = 20, align = 'left',fill = 'white', font = 'Courier New')
                else:
                    # right
                    drawRect(app.width/2 * i + app.width/2 - 10 - len(message)*15, startY + 40 * j, len(message)*15, 30,fill = 'white')
                    drawLabel(message.capitalize(), app.width/2 * i + app.width/2 - 20, startY + 40 * j + 15, size = 20, align = 'right', fill = reddishPink, font = 'Courier New')
                if j == len(app.prevMessages) - 1 and app.is_paused:
                    temp = (user + 1) % 2
                    drawRect(app.width/2 * temp + 10, startY + 41 * j, len('This message contains profanity!')*9, 30,fill = 'hotpink')
                    drawLabel('This message contains profanity!', app.width/2 * temp + 20 , startY + 41 * j + 15, size = 20, align = 'left',fill = 'white', font = 'Cochin')
        if app.notUnderstood:
            drawRect((app.speaker - 1) * app.width/2 +app.width/4,app.height/2,app.width/2 - 70, app.width/12 , align = 'center', fill = 'tomato',border = 'black')
            drawLabel(f'Could not understand your audio!',(app.speaker - 1) * app.width/2 +app.width/4,app.height/2 - 10, size = 20, font = 'Cochin',bold = True)
            drawLabel(f'Press esc to continue.',(app.speaker - 1) * app.width/2 +app.width/4,app.height/2 + 10, size = 20, font = 'Cochin',bold = True)

    

        drawLine(app.width/2,0,app.width/2,app.height,lineWidth = 1)
        drawLine(0,app.height/12,app.width,app.height/12,lineWidth = 1)
        drawLine(0,app.height*11/12,app.width,app.height*11/12,lineWidth = 1)

def onMousePress(app, mouseX, mouseY):
    for i in range(2):
        textBox = app.textboxes[i]
        anotherTextBox = app.textboxes[(i+1)%2]
        if (textBox.left <= mouseX <= textBox.left + textBox.width) and (textBox.top <= mouseY <= textBox.top + textBox.height) and not app.is_paused:
            app.speaker = i + 1 
            listen_and_recognize(app)
        
 
def onKeyPress(app, key):
    if key == 'enter' and app.welcome:
        app.welcome = False
    if key == 'space' and app.is_paused:
        app.timepassed = -50
        app.speaker = 1
        app.is_paused = False
        app.text = ""
    if key == 'escape' and app.notUnderstood:
        app.notUnderstood = False
 
def listen_and_recognize(app):
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            app.text = r.recognize_google(audio)
            
            app.prevMessages.append((app.speaker - 1, app.text))
            if len(app.prevMessages) > 16:
                app.prevMessages = app.prevMessages[1:]
            if is_profane(app.text):
                app.is_paused = True
                return
            app.speaker = 3 - app.speaker
            return
        except sr.UnknownValueError:
            print('No understand')
            app.notUnderstood = True
    
            return 
 
def main():
    runApp()
 
main()
 