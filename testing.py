from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import wave

class CellularAutomaton:
    def __init__(self, rule, key):
        self.rule = rule
        self.state = key

    def evolve(self):
        next_state = ''
        for i in range(len(self.state)):
            left = self.state[i - 1]
            center = self.state[i]
            right = self.state[(i + 1) % len(self.state)]
            next_state += self.rule(left, center, right)
        self.state = next_state

def rule30(left, center, right):
    rule = {
        ('1', '1', '1'): '0',
        ('1', '1', '0'): '0',
        ('1', '0', '1'): '0',
        ('1', '0', '0'): '1',
        ('0', '1', '1'): '1',
        ('0', '1', '0'): '1',
        ('0', '0', '1'): '1',
        ('0', '0', '0'): '0'
    }
    return rule[(left, center, right)]

def convert_key_to_binary(key):
    binary_key = ''.join(format(ord(char), '08b') for char in key)
    return binary_key

def encrypt_audio(input_file, output_file, key):
    with wave.open(input_file, 'rb') as f:
        params = f.getparams()
        audio_frames = f.readframes(params.nframes)

    key_binary = convert_key_to_binary(key)

    automaton = CellularAutomaton(rule30, key_binary)
    automaton.evolve()
    keystream = automaton.state
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    padded_frames = pad(audio_frames, AES.block_size)
    encrypted_frames = cipher.encrypt(padded_frames)
    encrypted_audio_data = bytearray()
    for i in range(len(encrypted_frames)):
        encrypted_audio_data.append(encrypted_frames[i] ^ int(keystream[i % len(keystream)]))

    with wave.open(output_file, 'wb') as f:
        f.setparams(params)
        f.writeframes(encrypted_audio_data)




key = input("Enter the key: ")
input_file = 'input_audio.wav'
with wave.open(input_file, 'rb') as f:
    params = f.getparams()
    print(params)
    audio_frames = f.readframes(params.nframes)
    print("-----")
    print(audio_frames)

