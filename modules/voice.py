import time
try:
    import speech_recognition as sr
except Exception:
    sr = None
try:
    import pyttsx3
except Exception:
    pyttsx3 = None

class VoiceEngine:
    def __init__(self, enable_tts=True):
        self.enable_tts = enable_tts and (pyttsx3 is not None)
        if self.enable_tts:
            try:
                self.tts = pyttsx3.init()
                self.tts.setProperty('rate', 160)
            except Exception:
                self.tts = None
        else:
            self.tts = None
        self.recognizer = sr.Recognizer() if sr is not None else None
        self.mic = sr.Microphone() if (sr is not None) else None

    def speak(self, text):
        print(f"[TTS] {text}")
        if self.tts:
            try:
                self.tts.say(text)
                self.tts.runAndWait()
            except Exception as e:
                print('[TTS ERROR]', e)

    def listen_once(self, timeout=5, phrase_time_limit=8):
        if self.recognizer is None or self.mic is None:
            return None, 'voice-not-available'
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        try:
            txt = self.recognizer.recognize_google(audio)
            return txt, None
        except Exception as e:
            return None, str(e)
