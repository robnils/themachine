# NOTE: this example requires PyAudio because it uses the Microphone class
import os
import time

import speech_recognition as sr


from gtts import gTTS



def play(path):
    import vlc

    print "playing..."
    p = vlc.MediaPlayer(path)

    p.play()
    time.sleep(0.1)
    while p.is_playing():
        time.sleep(0.1)


def play_pyglet(path):
    """

    :param path:
    :return:
    """
    import pyglet

    print "playing..."
    song = pyglet.media.load(path)
    song.play()
    pyglet.app.run()


def play_wave(path):
    """

    :param path:
    :return:
    """
    import wave
    import pyaudio

    CHUNK = 1024

    wf = wave.open(path, 'rb')
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()
    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()

def speak(audioString):
    """
    Uses a google rest api
    :param audioString:
    :return:
    """
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    path = "audio.mp3"
    print "saving..."
    tts.save(path)
    play(path)

    #os.system("mpg321 audio.mp3")

# this is called from the background thread
def callback(recognizer, audio):
    """

    :param recognizer:
    :param audio:
    :return:
    """
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        #print("Speech Recognition thinks you said '" + recognizer.recognize_sphinx(audio) + "'")
        #print("Speech Recognition thinks you said '" + recognizer.recognize_sphinx(audio) + "'")

        audio_string = recognizer.recognize_sphinx(audio)
        speak(audio_string)
        # print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))

r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some other computation for 5 seconds, then stop listening and keep doing other computations
for _ in range(50):
    time.sleep(0.1) # we're still listening even though the main thread is doing other things

stop_listening() # calling this function requests that the background listener stop listening

while True:
    time.sleep(0.1)