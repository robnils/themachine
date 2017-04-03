from __future__ import unicode_literals
import time

import os
import vlc
import speech_recognition
import pyglet

from gtts import gTTS


class Speak:
    response = ''
    def __init__(self):
        self.audio = "tmpfile.mp3"
        self.recog = speech_recognition.Recognizer()
        self.mic = speech_recognition.Microphone()

        self.stop_listening = None

    def play(self):
        print "Playing..."
        music = pyglet.resource.media(self.audio)
        music.play()

        #time.sleep(0.1)
        #while p.is_playing():
        #    time.sleep(0.1)

    @property
    def listening(self):
        return self.stop_listening is None

    @staticmethod
    def remove_if_exists(path):
        if os.path.exists(path):
            os.remove(path)

    def speak(self, string):
        """
        Uses a google rest api
        :param string:
        :return:
        """
        if not string:
            print('No input...')
            return

        print(string)
        tts = gTTS(text=string, lang='en')

        # print("Saving...")
        Speak.remove_if_exists(self.audio)
        tts.save(self.audio)

        # self.play()

    def start(self):
        Speak.response = ''
        print("Listening...")
        with self.mic as source:
            self.recog.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

        self.stop_listening = self.recog.listen_in_background(self.mic, self._callback)

    def stop(self):
        if self.stop_listening:
            self.stop_listening()
            self.stop_listening = None
            print("Stopped listening")

    def _callback(self, recog, audio):
        """

        """
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            # print("Speech Recognition thinks you said '" + recognizer.recognize_sphinx(audio) + "'")
            # print("Speech Recognition thinks you said '" + recognizer.recognize_sphinx(audio) + "'")

            audio_string = recog.recognize_sphinx(audio)
            Speak.response = audio_string
            self.speak(audio_string)
            # print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
        except speech_recognition.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except speech_recognition.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))


