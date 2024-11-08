from flask import Flask, render_template, request, redirect
from huggingface_hub import InferenceClient
import pyttsx3
import os

app = Flask(__name__)

def text_to_audio(text):
    """Converts text to audio and narrates it."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Choose a different index for other voices
    engine.setProperty('rate', 180)  # Adjust speaking rate
    engine.say(text)
    engine.runAndWait()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Render the homepage and handle URL submission."""
    story = ""
    if request.method == 'POST':
        image_url = request.form['image_url']
        if image_url:
            # Generate a story from the public image URL
            story = process_image(image_url)
            # Narrate the story
            text_to_audio(story)
            return render_template('index.html', image_url=image_url, story=story)
    return render_template('index.html', image_url=None, story=story)

def process_image(image_url):
    """Process the image URL and return a generated story."""
    # Get the API key from your token module
    client = InferenceClient(os.getenv('myapi'))

    # Create a prompt for generating a story
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Create a fun and engaging story with simple language involving characters, where this image becomes part of an adventure led by a main character. the start should be very catchy"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]
        }
    ]

    # Generate the story from the model
    stream = client.chat.completions.create(
        model="meta-llama/Llama-3.2-11B-Vision-Instruct",
        messages=messages,
        max_tokens=500,
        stream=True
    )

    # Concatenate the story as it streams
    story = ""
    for chunk in stream:
        story_chunk = chunk.choices[0].delta.content
        story += story_chunk

    return story

if __name__ == '__main__':
    app.run(debug=True)
