import pyttsx3

def text_to_audio(text):
  """Converts text to audio with a more human-like tone.

  Args:
    text: The text to be converted to audio.
  """

  engine = pyttsx3.init()

  # Adjust voice and rate for a more natural tone
  voices = engine.getProperty('voices')
  engine.setProperty('voice', voices[0].id)  # Change index for different voices
  engine.setProperty('rate', 180)  # Adjust speaking rate

  # Add pauses and emphasis (basic example)
  text_with_pauses = text.replace(".", ". ")  # Add space after periods
  text_with_pauses = text_with_pauses.replace("!", "! ")

  engine.say(text_with_pauses)
  engine.runAndWait()

# if __name__ == "__main__":
#   text = """

# """
#   text_to_audio(text)
