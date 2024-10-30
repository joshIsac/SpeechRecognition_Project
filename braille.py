from flask import Flask, request, jsonify, send_file, render_template, url_for
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__)

# Simulated Braille Dictionary
braille_dict = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵'
}

# Convert text to Braille
def convert_to_braille(text):
    return ''.join([braille_dict.get(char.lower(), char) for char in text])

# Convert Braille back to text (for Braille-to-speech)
def convert_braille_to_text(braille):
    reverse_braille_dict = {v: k for k, v in braille_dict.items()}
    return ''.join([reverse_braille_dict.get(char, char) for char in braille])

# Route for home page (sample.html)
@app.route('/')
def home():
    return render_template('sample.html')

# Route for speech-to-braille.html page
@app.route('/speech-to-braille-page')
def speech_to_braille_page():
    return render_template('speech-to-braille.html')

# Speech to Braille API
@app.route('/speech-to-braille', methods=['GET'])
def speech_to_braille():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Speak anything...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        braille_text = convert_to_braille(text)
        return jsonify({"braille": braille_text})
    except sr.UnknownValueError:
        return jsonify({"error": "Sorry, could not understand what you said."})
    except sr.RequestError:
        return jsonify({"error": "Sorry, could not connect to the speech recognition service."})

# Braille to Speech API
@app.route('/braille-to-speech', methods=['POST'])
def braille_to_speech():
    data = request.get_json()
    braille_input = data.get('braille')
    
    # Convert Braille to text
    text_output = convert_braille_to_text(braille_input)
    
    # Convert text to speech using gTTS
    tts = gTTS(text=text_output, lang='en')
    audio_file = 'braille_speech.mp3'
    tts.save(audio_file)
    
    # Return the audio file to the client
    return send_file(audio_file, mimetype='audio/mp3')

if __name__ == '__main__':
    app.run(debug=True)
