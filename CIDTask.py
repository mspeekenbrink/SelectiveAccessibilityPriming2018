import random, math, array, random, csv, os
from psychopy import core,visual,event
import numpy as np

class Task:

    fixTime = 0.5 # fixation time in seconds
    ITI = 1.0 # inter-trial interval in seconds
    punishTime = 10
    matchHashMaskLength = True #False #True

    def __init__(self,win,filename,tasknr,taskid,responses,debug):

        # Adapted from http://stackoverflow.com/questions/14091387/creating-a-dictionary-from-a-csv-file
        if debug:
            reader = csv.DictReader(open('Files/test/LDT' + str(taskid) + '.csv'))
        else:
            reader = csv.DictReader(open('Files/actual/LDT' + str(taskid) + '.csv'))
        result = []
        for row in reader:
            result.append(row)

        # randomize order within blocks
        block_id = []
        for i in range(len(result)):
            block_id.append(result[i]['block'])
        block_ids = np.sort(np.unique(block_id))

        stimuli = []
        for i in range(len(block_ids)):
            tmp_ids = []
            for j in range(len(result)):
                if result[j]['block'] == block_ids[i]:
                    tmp_ids.append(j)
            random.shuffle(tmp_ids)
            for j in range(len(tmp_ids)):
                stimuli.append(result[tmp_ids[j]])

        # self.instructionText = 'Q = ' + responses[0] + ', ' + 'P = ' + responses[1]
        self.stimuli = stimuli
        self.ntrials = len(stimuli)
        self.datafile = open(filename, 'a') #a simple text file with 'comma-separated-values'
        self.win = win
        self.tasknr = tasknr
        self.trial = 1
        self.responses = responses

        fontFile = os.getcwd() + '/Files/LiberationMono-Regular.ttf'
        # visuals
        #self.Instructions = visual.TextStim(self.win,text=self.instructionText,pos=(.0,-.8),height=.07,alignVert='center',wrapWidth=1.5)
        self.Stimulus = visual.TextStim(self.win,text="sadjhgsad",pos=(.0,.0),height=.1,alignVert='center',wrapWidth=1.5,fontFiles=[fontFile],font='LiberationMono')
        self.HashMask = visual.TextStim(self.win,text="######",pos=(.0,.0),height=.12,alignVert='center',wrapWidth=1.5,fontFiles=[fontFile],font='LiberationMono')
        #self.Stimulus.font = 'LiberationMono'
        #self.HashMask.font = 'LiberationMono'
        visualNoiseSize = 256
        visualNoiseWidth = 512 # Dimension in pixels of visual noise. Must be a power of 2
        visualNoiseHeight = 128 # Dimension in pixels of visual noise. Must be a power of 2
        noiseSize = 512
        noiseTexture = np.random.rand(128,128)*2-1
        self.NoiseMask = visual.GratingStim(win=self.win, tex=noiseTexture, size=(visualNoiseSize,visualNoiseSize), units='pix',interpolate=True)
        self.Mask = self.HashMask
        self.Question = visual.TextStim(self.win,text="Type the word here",pos=(.0,.3),height=.08,alignVert='center',wrapWidth=1.5)
        self.Feedback = visual.TextStim(self.win,text="",pos=(.0,.3),height=.08,alignVert='center',wrapWidth=1.5)
        self.Response = visual.TextStim(self.win,text="",pos=(.0,.0),height=.08,alignVert='center',wrapWidth=1.5)
        self.fixation = visual.ShapeStim(win,
            units='pix',
            lineColor='white',
            lineWidth=3.0,
            vertices=((-25, 0), (25, 0), (0,0), (0,25), (0,-25)),
            closeShape=False,
            pos= [0,0])

        self.trialClock = core.Clock()

        self.datafile.write('taskNr,trial,type,stimulus,identification,id_RT,response,response_RT\n')


    def Run(self):
        running = True
        trial = 1

        while running:

            # display fixation cross
            stimulus = self.stimuli[trial-1]['word']
            stype = self.stimuli[trial-1]['type']
            self.Stimulus.setText(stimulus)
            if self.matchHashMaskLength:
                self.HashMask.setText('#' * len(stimulus))
            self.fixation.draw()
            self.win.flip()
            core.wait(self.fixTime)

            # display word
            event.clearEvents()

            #self.Stimulus.draw()
            #self.Instructions.draw()
            #self.win.flip()

            self.trialClock.reset()

            # wait for response
            response = ''
            text = ''
            id_RT = ''
            response_RT = ''
            cycleN = 1
            identification = False
            while identification == False and cycleN < 16:
                # each cycle consists of 30 frames (500 ms on a 60 Hz monitor)
                for frameN in range(15):#for exactly 200 frames
                    if identification:
                        break
                    if frameN < cycleN:  # present fixation for a subset of frames
                        self.Stimulus.draw()
                    else:  # present stim for a different subset
                        self.Mask.draw()
                    self.win.flip()
                    for key in event.getKeys():
                        if key in ['space']:
                            id_RT = self.trialClock.getTime()
                            identification = True
                        if key in ['escape']:
                            self.win.close()
                            core.quit()
                    frameN += 1
                cycleN += 1

            if identification == True:
                # Type in response
                while event.getKeys(keyList=['return','num_enter'])==[] or len(text) == 0:
                    escape = event.getKeys(keyList=['escape'])
                    if escape == ['escape']:
                        self.win.close()
                        core.quit()
                    letterlist=event.getKeys(keyList=[#'1','2','3','4','5','6','7','8','9','0',
                    #'num_1','num_2','num_3','num_4','num_5','num_6','num_7','num_8','num_9','num_0',
                    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                    #'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                    #'comma','period','space','exclamation','question',
                    'backspace',])
                    for l in letterlist:
                        #if key isn't backspace, add key pressed to the string
                        if l !='backspace':
                            text+=l.replace('num_','').replace('comma',',').replace('period','.').replace('space',' ').replace('exclamation','!').replace('question','?')
                        #otherwise, take the last letter off the string
                        elif len(text)>0:
                            text=text[:-1]
                        elif len(text) < 1:
                            text=''
                    self.Response.setText(text)
                    self.Question.draw()
                    self.Response.draw()
                    #self.Instructions.draw()
                    self.win.flip()
                    #print text

                response_RT = self.trialClock.getTime() - id_RT
                # get response
                response = text
                # clear keypresses
                event.clearEvents()
            ## check responses
            if response != stimulus:
                if identification == False:
                    self.Feedback.setText('Too slow! \n\nPlease wait for the next trial.')
                else:
                    self.Feedback.setText('Incorrect! \n\nPlease wait for the next trial.')
                self.Feedback.draw()
                self.win.flip()
                core.wait(self.punishTime)

            # write data
            self.datafile.write(
                str(self.tasknr) + ',' +
                str(trial) + ',' +
                str(stype) + ',' +
                str(stimulus) + ',' +
                str(identification) + ',' +
                str(1000*id_RT) + ',' +
                str(response) + ',' +
                str(1000*response_RT) + '\n')

            # ITI
            self.win.flip()
            core.wait(self.ITI)

            trial += 1

            if trial > self.ntrials:
                running = False

        self.datafile.close()
