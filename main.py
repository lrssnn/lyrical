
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
    while pygame.mixer.music.get_busy():
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


# I am thinking about how to generate sentences with some coherence...
# I think we will need to choose a tense that the entire sentence lives under,
# Then generate our subject and predicate. We should also consider the placement
# of subject and predicate. I suppose
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


def process_dictionary():
    delimiter = ">>|<<"
    types = {}
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print("Processing " + letter)
        with open('dict\\OPTED v0.03 Letter '+letter+'.html', 'r') as dict:
            #for i in range(20):
            for line_raw in dict:

                #line = dict.readline().strip()
                line = line_raw.strip()
                if not line.startswith("<p>"):
                    continue

                #print(line)

                line = line.replace('<p>', '').replace("<b>", "").replace("</p>", "").replace("</b> ", delimiter)
                line = line.replace("(<i>", "").replace("</i>) ", delimiter)

                #print(line)
                parts = line.split(delimiter)
                if len(parts) != 3:
                    print("Error: " + line_raw)
                    continue

                type = parts[1]
                if len(type) == 0:
                    continue
                type_parts = type.split(" &amp; ")
                for part in type_parts:
                    if part not in types:
                        types[part] = part


    junk = open("processed\\JUNK.txt", "w+")
    for type in types.keys():
        print(type)
        try:
            file = open("processed\\ProcessedDict-" + type + ".txt", "w+")
            types[type] = file
        except:
            print("oop:" + type)
            types[type] = junk

    # Naughty, now we're doing it for real
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print("Processing " + letter)
        with open('dict\\OPTED v0.03 Letter '+letter+'.html', 'r') as dict:
            for line_raw in dict:

                line = line_raw.strip()
                if not line.startswith("<p>"):
                    continue

                line = line.replace('<p>', '').replace("<b>", "").replace("</p>", "").replace("</b> ", delimiter)
                line = line.replace("(<i>", "").replace("</i>) ", delimiter)

                parts = line.split(delimiter)
                if len(parts) != 3:
                    print("Error: " + line_raw)
                    continue

                type = parts[1]
                if len(type) == 0:
                    continue
                type_parts = type.split(" &amp; ")
                for type in type_parts:
                    types[type].writelines(line + "\n")

    for key in types.keys():
        types[key].close()



if __name__ == '__main__':
    #print(generate_sentence())
    # generate_speech_from_text(text)
    process_dictionary()

