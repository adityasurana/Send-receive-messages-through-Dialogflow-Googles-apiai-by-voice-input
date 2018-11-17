import sys
import json
import time
import os.path
import RPi.GPIO as GPIO
from subprocess import call
import speech_recognition as sr

try:
    import apiai

except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
CLIENT_ACCESS_TOKEN = '#putt your client acces token from dialogflow here#'


def audio_to_text():
    recognize_obj = sr.Recognizer()

    with sr.Microphone() as source:                                                                       
        audio = recognize_obj.listen(source)   

    try:
        return (recognize_obj.recognize_google(audio))

    except Exception as e:
        return ("Could not understand audio")



def AI_response():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    print ("Please Wait...")

    request = ai.text_request()

    request.lang = 'de'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    
    request.query = audio_to_text()

    print ("Processing Statement...")

    response = request.getresponse()

    return (response.read())


def AIresponse_to_audio():
    response = AI_response()
    response_dict = json.loads(response)
    response_text = response_dict["result"]["fulfillment"]["speech"]
    time.sleep(5)
    print (response_text)
    call(['espeak -g7 -s150 -ven+f3 "'+response_text+'"'],shell=True)
    return "DONE"



if __name__ == '__main__':

    while True:
          input_state = GPIO.input(23)

          if input_state == 0:
              print('Listening...')
              print(AIresponse_to_audio())
              print("Stopped Listening...")
          else:
              print ("Idle...")
              time.sleep(1)
