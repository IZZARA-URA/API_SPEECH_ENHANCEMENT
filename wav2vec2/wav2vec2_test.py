from wav2vec2 import Wav2Vec2_larynx

variableX1 = './wavTest/0001_0003.wav' 
'''
In the API this file it will upload to server 
Then, passed to Wav2Vec2_larynx function 
return txt to part FRONT-END
'''

variableX2 = Wav2Vec2_larynx(variableX1, True)

print(variableX2)