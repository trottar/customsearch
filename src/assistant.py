#! /usr/bin/python3.8

#
# Description:
# ================================================================
# Time-stamp: "2021-12-21 01:43:58 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

import speech_recognition as sr
import pyttsx3

def test_voices():
    engine = pyttsx3.init()
    # getter method(gets the current value
    # of engine property)
    voices = engine.getProperty('voices')
    for v in voices:
        print(v)
        print(v.name)
        engine.setProperty('voice', v.id)
        engine.say('Hello world from ' + v.name)
        engine.runAndWait()        
        
def speak(audio):
      
    engine = pyttsx3.init()
    # getter method(gets the current value
    # of engine property)
    voices = engine.getProperty('voices')

    engine.setProperty('rate', 130) 
    #engine.setProperty('voice', voices[-5].id) 
    #engine.setProperty('voice', 'english+f1')
    #engine.setProperty('voice', 'english+f2')
    #engine.setProperty('voice', 'english+f3')
    #engine.setProperty('voice', 'english+f4')
    #engine.setProperty('voice', 'english_rp+f3') 
    #engine.setProperty('voice', 'english_rp+f4')
    engine.setProperty('voice', 'english-us') # my preference

      
    # Method for the speaking of the the assistant
    engine.say(audio)  
      
    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()


def Hello():
    # This function is for when the assistant 
    # is called it will say hello and then 
    # take query
    speak("hello sir I am your desktop assistant. Tell me how may I help you")    
    
# this method is for taking the commands
# and recognizing the command from the
# speech_Recognition module we will use
# the recongizer method for recognizing
def takeCommand():
  
    r = sr.Recognizer()
  
    # from the speech_Recognition module 
    # we will use the Microphone module
    # for listening the command
    with sr.Microphone() as source:
        print('Listening')
          
        # seconds of non-speaking audio before 
        # a phrase is considered complete
        r.pause_threshold = 0.7
        audio = r.listen(source)
          
        # Now we will be using the try and catch
        # method so that if sound is recognized 
        # it is good else we will have exception 
        # handling
        try:
            print("Recognizing")
              
            Query = r.recognize_google(audio, language='en')
            print("the command is printed=", Query)
              
        except Exception as e:
            print(e)
            print("Say that again sir")
            return "None"
          
        return Query

#test_voices()
#Hello()
takeCommand()
