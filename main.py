
def generate_speech_from_text(input):
    from google.cloud import texttospeech
    from google.cloud.texttospeech  import types as speech

    client = texttospeech.TextToSpeechClient()

    synthesis_input = speech.SynthesisInput(text=input)

    voice = speech.VoiceSelectionParams(
        language_code='en-AU',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL
    )

    audio_config = speech.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio written to "output.mp3"')

    play_sound("output.mp3")

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

def generate_sentence():
    # I suppose we would like to choose:
    #  - A length
    #  - A valid syntax
    #  - Words for each slot??
    import random
    sentence_length = random.randint(3, 8)
    print(sentence_length)

    # A clause is asubject followed by a predicate. For now we only make simple sentences
    # TODO: Compound sentences (multiple independent clauses) or complex sentences (dependent clauses)

    subject = generate_subject()
    predicate = generate_predicate()

    return subject.to_string() + ' ' + predicate.to_string() + '.'

# From here I am stubbing out
class TreeNode:
    def __init__(self, type, content):
        self.children = []
        self.type = type
        self.content = content

    def add_child(self, child):
        self.children.append(child)

    def to_string(self):
        if self.type == "Leaf":
            return self.content
        else:
            result = ""
            for child in self.children:
                result += child.to_string()
                result += " "
            return result.strip(' ')



def generate_subject():
    return TreeNode("Leaf", "I")


def generate_predicate():
    root = TreeNode("Branch", "VP")
    verb = TreeNode("Leaf", "hit")
    object = TreeNode("Branch", "AN")
    article = TreeNode("Leaf", "the")
    noun = TreeNode("Leaf", "ball")

    object.add_child(article)
    object.add_child(noun)

    root.add_child(verb)
    root.add_child(object)

    return root

if __name__ == '__main__':
    text = "This is a test"
    print(generate_sentence())
    # generate_speech_from_text(text)