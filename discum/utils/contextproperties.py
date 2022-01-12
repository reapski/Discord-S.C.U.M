#x-context-properties
#some of these values are hardcoded cause that's just faster

import base64
import json

class ContextProperties(object):
	@staticmethod
	def encodeData(data):
		binaryData = json.dumps(data).encode()
		return base64.b64encode(binaryData).decode("utf-8")

	@staticmethod
	def get(location, guild_id=None, channel_id=None, channel_type=None):
		loc = location.lower()
		if loc == "friends":
			return "eyJsb2NhdGlvbiI6IkZyaWVuZHMifQ==" # {"location":"Friends"}
		elif loc == "context menu":
			return "eyJsb2NhdGlvbiI6IkNvbnRleHRNZW51In0=" # {"location":"ContextMenu"}
		elif loc == "user profile":
			return "eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9" # {"location":"User Profile"}
		elif loc == "add friend":
			return "eyJsb2NhdGlvbiI6IkFkZCBGcmllbmQifQ==" # {"location":"Add Friend"}
		elif loc == "guild header":
			return "eyJsb2NhdGlvbiI6Ikd1aWxkIEhlYWRlciJ9" # {"location":"Guild Header"}
		elif loc in ("accept invite page", "join guild"):
			data = {
				"location": "Accept Invite Page",
				"location_guild_id": guild_id,
				"location_channel_id": channel_id,
				"location_channel_type": channel_type,
			}
			if loc == "join guild":
				data["location"] = "Join Guild"
			return ContextProperties.encodeData(data)
		else:
			data = {"location":location}
			return ContextProperties.encodeData(data)