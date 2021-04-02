import os


#constants
BASE_URL = "https://cdn.tomon.co"

class Files:
	def __init__(self, key):
		self.key = key

	def file_url(self, path):
		return os.path.join(BASE_URL, path)

	def avatar_url(self):
		return self.file_url(os.path.join('avatars', self.key))

	def emoji_url(self):
		return self.file_url(os.path.join('emojis', self.key))

	def icon_url(self):
		return self.file_url(os.path.join('icons', self.key))

	def background_url(self):
		return self.file_url(os.path.join('backgrounds', self.key))

	def attachment_url(self):
		return self.file_url(os.path.join('attachments', self.key))

	def stamp_url(self):
		return self.file_url(os.path.join('stamps', self.key))

	def external_url(self):
		return self.file_url(os.path.join('externals', self.key))