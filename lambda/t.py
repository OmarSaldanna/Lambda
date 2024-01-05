from core.modules import OpenAI

ai = OpenAI("alphabeta", "0")
image_path = "../lambdrive/images/0kf.png"

print(ai.gpt_vision(image_path, "dime que ves en la imagen"))
