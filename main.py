
def run_quickstart():
    # [START tts_quickstart]
    """Synthesise speech from text or ssl"""

    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.types.SynthesisInput(text="Hello Niklas. I am reading this in a Swedish Accent")

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='sv-SE',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    #response = client.synthesize_speech(synthesis_input, voice, audio_config)

    #with open('output.mp3', 'wb') as out:
        #out.write(response.audio_content)
        #print('Audio written to "output.mp3"')

    play_sound("output.mp3")
    # [END tts_quickstart]

def play_sound(filename):
    import pygame
    import time

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    print('Playing...')
    while(pygame.mixer.music.get_busy()):
        print(pygame.mixer.music.get_pos() / 1000)
        time.sleep(1)
        #print('.', end="")
    print("Complete")

if __name__ == '__main__':
    run_quickstart()