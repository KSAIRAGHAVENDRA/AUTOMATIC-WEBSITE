#currently supports only checkout-forms
import re
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--text", required=True,help="path to the input image")
args = vars(ap.parse_args())

def getNumber(number):
    NumberSwitch = { 
        "one":1, 
        "two":2,
        "three":3, 
        "four":4, 
        "five":5,
        "six":6, 
        "seven":7, 
        "eight":8, 
        "nine":9, 
        "ten":10,
    }
    return NumberSwitch.get(number,0)

def getElements(speechtext):
	texts = []
	buttons = []
	#parse for textfields
	for m in re.finditer("(one|two|three|four|five)\s*(textfield(s|)|textinput(s|))\s*for\s*\w*\s*", speechtext):
	    foundtext = m.group(0).strip()
	    matchobj = re.search(r"\w+", foundtext) #Get the word at the beginning of the string. Whatever that word is.
	    count = getNumber(matchobj.group(0))
	    plaintext = re.search(r"(\w+)$", foundtext).group(0) # Get the word at the end of the string. Whatever that word is.
	    texts.append([count,plaintext])
	    # print(m.group(0),texts)

	#parse for buttons
	for m in re.finditer("(one|two|three|four|five)\s*\w*\s*(button(s|))\s*", speechtext):
	    foundtext = m.group(0).strip()
	    matchobj = re.search(r"\w+", foundtext) #Get the word at the beginning of the string. Whatever that word is.
	    count = getNumber(matchobj.group(0))
	    remainingstr = foundtext[matchobj.end():]
	    plaintext = re.search(r"\w+", remainingstr).group(0) # Get the middle word. Whatever that word is.
	    buttons.append([count,plaintext])
	    # print(m.group(0),buttons)

	return [texts,buttons]

def elementstohtml(speechtext, texts, buttons):
    code = "<!DOCTYPE html>"+'\n'+"<html>"+'\n'
    #add page title
    code = code + "<head>"+'\n'+"<title>"+texts[0][1].capitalize()+"</title>"+'\n'+"</head>"+'\n'
    #add body tag
    code = code + "<body>"+'\n'
    #add div
    code = code + "<div class=\"container\">" + '\n' + "<br>" + '\n'

    code = code + "<H4><b>"+speechtext+"</H4>" + '\n' + "<br> <br>" + '\n'
    #add elements from top-to-bottom
    for tf in texts:
        code = code + "<label><b>"+tf[1].capitalize()+"</b></label>" + '\n'
        code = code + "<br>" + '\n'
        for i in range(tf[0]):
            code = code + "<input type=\"text\" class=\"textfield\" required>" + '\n'
            code = code + "<br><br>" + '\n'

    for btn in buttons:
        for i in range(btn[0]):
            code = code + "<button type=\"submit\">"+btn[1].capitalize()+"</button>"+'\n'
        code = code + "<br>" + '\n'

    #close div
    code = code + "<br>" + '\n' + "</div>" + '\n'
    
    #add css styling
    style = "<style>" + '\n'
    style = style + ".container {background-color: #f2f2f2;padding: 5px 20px 15px 20px;border: 1px solid lightgrey;border-radius: 3px;}"+'\n'
    style = style + "button:hover {background-color: #45a049;}"+'\n'
    style = style + "label"+"{margin-left:"+str(500)+"px;font-size: 30px;}" + '\n'
    style = style + "input[type=text]"+"{margin-left:"+str(500)+"px;padding: 17px;border: 1px solid #ccc;border-radius: 3px;width: 30%;}" + '\n'
    style = style + "button{background-color: #4CAF50;color: white;padding: 12px;margin: 10px 0;width: 25%;"
    style = style + "margin-left:"+str(550)+"px;border: none;border-radius: 3px;cursor: pointer;font-size: 20px;}" + '\n'
    style = style + "</style>"+'\n'
    code = code + style

    #close body tag
    code = code + "</body>"+'\n'
    #close html tag
    code = code + "</html>"+'\n'

    return code

def save_as_html(code):
    file1 = open("generated_pagefromspeech"+".htm","w")
    file1.write(code)
    file1.close()

if __name__ == "__main__":
    speechtext = args["text"] 
    #"Hey azure I need a website Login Page with one textfield for username one textfield for password and one submit button"
    #"Hey azure I need a website Payment Page with one textfield for CardHolderName one textfield for CardNumber one textfield for ExpiryDate and one Pay button"
    #Hey azure I need a website Payment Page with one textfield for Name one textfield for ContactNumber three textfields for Address and one submit button
    #Hey azure I need a website Login Page with one textfield for username one textfield for password one back button and one submit button
    returnlist = getElements(speechtext)
    texts,buttons = returnlist[0], returnlist[1]
    print(texts,buttons)
    code = elementstohtml(speechtext,texts,buttons)
    save_as_html(code)
