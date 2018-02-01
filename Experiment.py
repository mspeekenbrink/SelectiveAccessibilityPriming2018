#!/usr/bin/env python
import random, csv
from psychopy import visual, event, core, data, gui, misc
import numpy as np
import Instructions, AnchorTask, CIDTask, SpanTask, ImageReelTask, ImageQuestionTask
  
# some variables
interTaskTime = 3
interTaskTime2 = 6

debug = False
set_fullscr = True
resolution = (1600,900)
#resolution = (800,450)

responses = ['yes','no']
taskAnchors = [['15'],['2','25'],['5','85']]
folderNames = [[''],['winter','summer'],['']]
comparativeQuestions = ['Is Big Ben taller or shorter than 15 meters high?',
                        u'Is the annual average temperature in the UK higher or lower than [anchor]\u00B0?',
                        'Is the average weight of a dog greater or less than [anchor] kilograms?']
                        
comparativeOptions = [['taller','shorter'],
                   ['higher','lower'],
                   ['greater','less']]
                   
absoluteQuestions = ['How tall is Big Ben?',
                     'What is the annual average temperature in the UK?',
                     'What is the average weight of a dog?']
units = [' metres',
         u'\u00B0C',
         ' kilograms']
         
# Admin
expInfo = {'date':data.getDateStr(),'ID':1,'gender':['male','female','other'],'age':17,'native language':['','English','other']}

#present a dialogue to change params
ok = False
while(not ok):
    expInfo = {'date':data.getDateStr(),'ID':1,'gender':['male','female','other'],'age':17,'native language':['','English','other']}
    dlg = gui.DlgFromDict(expInfo, title='Experiment', fixed=['date'],order=['date','ID','gender','age'])
    if dlg.OK:
        misc.toFile('lastParams.pickle', expInfo)#save params to file for next time
        if expInfo['native language'] != "":
            ok = True
        else:
            dlg.OK = False
    else:
        core.quit()#the user hit cancel so exit


# setup data file
fileName = 'Data/' + 'Subject' + str(expInfo['ID']) + '_' + expInfo['date'] + '.csv'

# Read in counterbalancing etc.
# Adapted from http://stackoverflow.com/questions/14091387/creating-a-dictionary-from-a-csv-file
reader = csv.DictReader(open('Files/ExpStructure.csv'))
result = []
for row in reader:
    if row['id'] == str(expInfo['ID']):
        result = row

if result['whichExpt.First'] == '1':
    taskOrder = [1,2,3]
else:
    taskOrder = [1,2,3]

anchors = [taskAnchors[0],taskAnchors[1][int(result['E1anchor']) - 1],taskAnchors[2][int(result['E2anchor']) - 1]]
#imageFolders = [folderNames[0],folderNames[1],folderNames[2][int(result['E1anchor']) - 1]]
imageFolders = [folderNames[0],folderNames[1][int(result['E1anchor']) - 1],folderNames[2]]
print imageFolders

for i in [1,2]:
    comparativeQuestions[i] = comparativeQuestions[i].replace('[anchor]',anchors[i])
#if result['wordKey'] == "P":
#    responses = [responses[1],responses[0]]

dataFile = open(fileName, 'w') #a simple text file with 'comma-separated-values'
dataFile.write('subject = ' + str(expInfo['ID']) + "; date = " + str(expInfo['date']) + ";gender = " + str(expInfo['gender']) + ";age =" + str(expInfo['age']) + "; native language = " + str(expInfo['native language']) + '\n')
dataFile.write('taskOrder = ' + str(taskOrder) + "; responses (Q,P) = " + str(responses) + '\n')
dataFile.close()

#create a window to draw in
myWin = visual.Window(resolution, winType='pyglet',allowGUI=False,units='norm', color=(0,0,0), fullscr = set_fullscr)

instructions = visual.TextStim(myWin,pos=[0,0],text="",height=.08,alignHoriz='center',wrapWidth=1.2)
CIDtext = 'Place your index fingers on the space bar now. \n\n Respond as soon as you recognize the word.'
CIDtext2 = 'Place your index fingers on the space bar now. \n\n Respond as soon as you recognize the word.'
SpanText = "You will now be shown letters one at a time. Please memorize them and recall them in order when asked."
ImageReelText = "You will now be shown a number of images. Please look carefully at them and keep them in mind as you will be asked questions about them later."

BetweenText = []
txt = 'This is the end of the first round of tasks. There will be two more rounds just like this one. \n\n'
#txt += 'In the "DOES IT HAVE MEANING?" task, please respond as quickly as possible. '
#txt += '\n\nThe Q key will always correspond to "' + responses[0] 
#txt += '" and the P key to "' + responses[1] + '". Make sure your index fingers rest on these keys.\n\n'
txt += 'Take a short break if you want to. Press any key to continue to the next block of the experiment.'
BetweenText.append(txt)
txt = 'This is the end of the second round of tasks. There will be one more rounds just like this one. \n\n'
#txt += 'In the "DOES IT HAVE MEANING?" task, please respond as quickly as possible. '
#txt += '\n\nThe Q key will always correspond to "' + responses[0] 
#txt += '" and the P key to "' + responses[1] + '". Make sure your index fingers rest on these keys.\n\n'
txt += 'Take a short break if you want to. Press any key to continue to the next block of the experiment.'
BetweenText.append(txt)

instr = Instructions.Instructions(myWin,responses)
instr.Run()

for tsk in range(3):
    if tsk == 1:
        # priming
        instructions.setText(ImageReelText)
        instructions.draw()
        myWin.flip()
        if tsk == 2:
            core.wait(interTaskTime2-.5)
            myWin.flip()
            core.wait(0.5)
        else:
            core.wait(interTaskTime-.5)
            myWin.flip()
            core.wait(0.5)
        task = ImageReelTask.Task(myWin,"Files/images/" + imageFolders[taskOrder[tsk]-1])
    else:
        task = AnchorTask.Task(myWin,fileName,tsk+1,comparativeQuestions[taskOrder[tsk]-1],units[taskOrder[tsk]-1],comparativeOptions[taskOrder[tsk]-1],1)
    task.Run()
    if tsk == 0:
        instructions.setText(CIDtext)
    else:
        instructions.setText(CIDtext2)
    instructions.draw()
    myWin.flip()
    if tsk == 0:
        core.wait(interTaskTime2-.5)
        myWin.flip()
        core.wait(0.5)
    else:
        core.wait(interTaskTime-.5)
        myWin.flip()
        core.wait(0.5)
    task = CIDTask.Task(myWin,fileName,tsk+1,taskOrder[tsk],responses,debug)
    task.Run()
    core.wait(interTaskTime-.5)
    myWin.flip()
    core.wait(0.5)
    if tsk == 1:
        which = "season"
        task = ImageQuestionTask.Task(myWin,fileName,tsk+1,which,imageFolders[taskOrder[tsk]-1])
    else:
        task = AnchorTask.Task(myWin,fileName,tsk+1,absoluteQuestions[taskOrder[tsk]-1],units[taskOrder[tsk]-1],comparativeOptions[taskOrder[tsk]-1],2)
    task.Run()
    if tsk < 2:
        instructions.setText(SpanText)
        instructions.draw()
        myWin.flip()
        if tsk == 0:
            core.wait(interTaskTime2-.5)
            myWin.flip()
            core.wait(0.5)
        else:
            core.wait(interTaskTime-.5)
            myWin.flip()
            core.wait(0.5)
        task = SpanTask.Task(myWin,fileName,tsk+1)
        task.Run()
        instructions.setText(BetweenText[tsk])
        instructions.draw()
        myWin.flip()
        event.waitKeys()

endText = "This is the end of the experiment. \n\n"
endText += "Thank you for your participation."
instructions.setText(endText) 
instructions.draw()
myWin.flip()

done = False
while not done:
    for key in event.getKeys():
        if key in ['escape']:
            done = True
            core.quit()
