import os
import pydub

# download images, linux only
def download_image(img_link: str, name: str, extension='.png', where="lambdrive/images/", dalle_type= ""):
	# Create the wget command
	wget_command = f'wget "{img_link}" -O "{where}{name}{extension}"'
	# Execute the wget command
	if os.environ["dev"] != "yes":
		# download the img
		os.system(wget_command)
		# and copy it to dalle
		os.system(f"cp {where}{name}{extension} lambdrive/dalle/{dalle_type}_{name}{extension}")
	# else, just print the variables
	else:
		print(img_link)
	# return the image path
	return f"{where}{name}{extension}"

# function to generate hashes, it must not be used to security operations
def generate_hash(data: str):
	# generate a numerical hash with python
    # convert it to hexadecimal
    return hex(hash(data) & 0xFFFFFFFFFFFFFFFF)[2:].zfill(16)

# function to get the minutes of an audio
def audio_minutes(audio_file: str):
	# read the audio
	audio = pydub.AudioSegment.from_file(audio_file)
	# return the audio minutes
	return audio.duration_seconds / 60