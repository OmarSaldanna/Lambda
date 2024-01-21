# module to read the youtube transcript
from youtube_transcript_api import YouTubeTranscriptApi
from core.modules import OpenAI


def get_video_id(link: str):
    start = link.find("youtu.be/") + len("youtu.be/")
    end = link.find("?")
    if end == -1:
        end = len(link)
    return link[start:end]

# 0   1  2     3  4      5 6
# vee el video de [link] y ...
# same for ve, mira, analiza
def main(params: tuple):
	# catch params
	message, author, server = params
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# split the message
	splited_message = message.split(' ')
	# read the video link
	link = splited_message[4]
	# get the id
	video_id = get_video_id(link)
	# try to read the video
	transcript = "Eres un asistente inteligente, respone basado en el contenido del archivo:\n"
	try:
		text_dic = YouTubeTranscriptApi.get_transcript(video_id, languages=['es', 'en'])
		# extract the text
		for t in text_dic:
  			transcript += t['text'] + " "
	except:
		return [{"type": "error", "content": "Error en video, quizá no tenga subtítulos"}]
	# and check if the text has not more tokens than the limit
	if openai.token_counter(transcript) > 15500:
    	# then trow a warning that the text is too long
		return [{
	      "type": "error",
	      "content": f"Lo siento el video excede el límite de **tokens**. Tu texto tiene **{openai.token_counter(transcript)} tokens**."
	    }]
	# then get the question
	question = ' '.join(splited_message[6:])
	# and use GPT
	return openai.gpt(question, model="gpt-3.5-turbo-16k", context=False, system=transcript)
  	


# info about the skill
info = """
Visor de YouTube
Esta función te permitirá hacerle preguntas a Lambda sobre videos de YouTube, solamente debes de pasarle a Lambda el link del video, ese que copias y pegas del botón de compartir.
Comando:Lambda [ve|mira|observa|analiza] el video de [link] y [tus preguntas]
Ejemplo:Lambda ve el video de https://youtu.be/kCudFI4tcpg?si=G-tBUt74yeompR2v y dime de que habla y las ideas principales en una lista.
Ejemplo:Lambda ve el video de https://youtu.be/kCudFI4tcpg?si=G-tBUt74yeompR2v y dame las palabras clave en una lista.
"""