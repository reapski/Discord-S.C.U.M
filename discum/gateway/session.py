class Session:
	settings_ready = {}
	settings_ready_supp = {}
	def __init__(self, input_settings_ready, input_settings_ready_supp):
		Session.settings_ready = input_settings_ready
		Session.settings_ready_supp = input_settings_ready_supp
		self.guild = guild
		self.DM = DM
		self.relationship = relationship
		self.userGuildSetting = userGuildSetting

	def read(self): #returns all Session settings
		return [self.settings_ready, self.settings_ready_supp]

	def saveMemory(self): #deletes some unused data
		self.settings_ready['users'] = []
		self.settings_ready_supp['merged_members'] = []
		self.settings_ready_supp['merged_presences']['guilds'] = []

	###***USER***###
	@property
	def user(self):
		return self.settings_ready['user']

	###***GUILDS***### (general)
	@property
	def guilds(self):
		return self.settings_ready['guilds']

	@property
	def allGuildIDs(self): #even if you're not in that guild
		return list(self.settings_ready['guilds'])

	@property
	def guildIDs(self): #only for guilds that you're in
		return [guildID for guildID in self.guilds if "removed" not in self.guilds[guildID]]

	def setGuildData(self, guildID, guildData):
		self.settings_ready['guilds'][guildID] = guildData

	def removeGuildData(self, guildID):
		self.settings_ready['guilds'].pop(guildID, None)

	def setDmData(self, channelID, channelData):
		self.settings_ready['private_channels'][channelID] = channelData

	def removeDmData(self, channelID):
		self.settings_ready['private_channels'].pop(channelID, None)

	def setVoiceStateData(self, guildID, voiceStateData):
		self.settings_ready_supp['voice_states'][guildID] = voiceStateData

	###***RELATIONSHIPS***### (general)
	@property
	def relationships(self):
		return self.settings_ready['relationships']
	
	@property
	def relationshipIDs(self):
		return list(self.settings_ready['relationships'])

	#friends
	@property
	def friends(self):
		return {
		    i: self.relationships[i]
		    for i in self.relationships if self.relationships[i]['type'] == 'friend'
		}
	
	@property
	def friendIDs(self):
		return list(self.friends)

	#blocked	
	@property
	def blocked(self):
		return {
		    i: self.relationships[i]
		    for i in self.relationships if self.relationships[i]['type'] == 'blocked'
		}
	
	@property
	def blockedIDs(self):
		return list(self.blocked)
	
	#incoming	
	@property
	def incomingFriendRequests(self):
		return {
		    i: self.relationships[i]
		    for i in self.relationships
		    if self.relationships[i]['type'] == 'pending_incoming'
		}
	
	@property
	def incomingFriendRequestIDs(self):
		return list(self.incomingFriendRequests)

	#outgoing
	@property
	def outgoingFriendRequests(self):
		return {
		    i: self.relationships[i]
		    for i in self.relationships
		    if self.relationships[i]['type'] == 'pending_outgoing'
		}
	
	@property
	def outgoingFriendRequestIDs(self):
		return list(self.outgoingFriendRequests)

	#friend merged presences	
	@property
	def onlineFriends(self):
		return self.settings_ready_supp['online_friends']
	
	@property
	def onlineFriendIDs(self):
		return list(self.onlineFriends)
		

	###***DMs***### (general)
	@property
	def DMs(self):
		return self.settings_ready['private_channels']

	@property
	def DMIDs(self):
		return list(self.DMs)
		

	###***USER SETTINGS***### (general)
	@property
	def userGuildSettings(self):
		return self.settings_ready['user_guild_settings'] #so uh...this is not only for guilds. It also covers group DMs so uh yea...weird naming
	
	@property
	def userSettings(self):
		return self.settings_ready['user_settings']
	
	@property
	def optionsForUserSettings(self):
		return list(self.settings_ready['user_settings'])
		
	def updateUserSettings(self, data):
		self.settings_ready['user_settings'].update(data)

	###other stuff
	@property
	def analyticsToken(self):
		return self.settings_ready['analytics_token']

	@property
	def connectedAccounts(self):
		return self.settings_ready['connected_accounts']

	@property
	def consents(self):
		return self.settings_ready['consents']

	@property
	def experiments(self):
		return self.settings_ready['experiments']

	@property
	def friendSuggestionCount(self):
		return self.settings_ready['friend_suggestion_count']

	@property
	def guildExperiments(self):
		return self.settings_ready['guild_experiments']

	@property
	def readStates(self):
		return self.settings_ready['read_state'] #another advantage of using websockets instead of requests (see https://github.com/discord/discord-api-docs/issues/13)

	@property
	def geoOrderedRtcRegions(self):
		return self.settings_ready['geo_ordered_rtc_regions']

	@property
	def cachedUsers(self): #idk what these are
		return self.settings_ready['users']

	@property
	def tutorial(self):
		return self.settings_ready['tutorial'] #that tutorial you get when you first make an account


###specific guild
class guild(Session):
	def __init__(self, guildID):
		self.guildID = guildID

	@property
	def data(self): #self.settings_ready['guilds']
		return Session.settings_ready['guilds'][self.guildID]

	def setData(self, newData):
		Session.settings_ready['guilds'][self.guildID] = newData

	def updateData(self, data):
		Session.settings_ready['guilds'][self.guildID].update(data)

	@property
	def unavailable(self):
		return 'unavailable' in Session.settings_ready['guilds'][self.guildID]

	@property
	def hasMembers(self):
		return len(Session.settings_ready['guilds'][self.guildID]['members']) >= 0

	@property
	def members(self):
		return Session.settings_ready['guilds'][self.guildID]['members']

	@property
	def memberIDs(self):
		return list(self.members)

	def resetMembers(self):
		Session.settings_ready['guilds'][self.guildID]['members'] = {}

	def updateOneMember(self, userID, userProperties):
		Session.settings_ready['guilds'][self.guildID]['members'][userID] = userProperties

	def updateMembers(self, memberdata): #where member data is a dictionary --> {userId: {properties}, ...}
		Session.settings_ready['guilds'][self.guildID]['members'].update(memberdata)

	@property
	def owner(self):
		return Session.settings_ready['guilds'][self.guildID]['owner_id'] #returns type int

	@property
	def boostLvl(self):
		return Session.settings_ready['guilds'][self.guildID]['premium_tier']

	@property
	def emojis(self):
		return Session.settings_ready['guilds'][self.guildID]['emojis']

	@property
	def emojiIDs(self):
		return list(self.emojis)

	@property
	def banner(self):
		return Session.settings_ready['guilds'][self.guildID]['banner']

	@property
	def discoverySplash(self): #not sure what this is about, something about server discoverability i guess (https://discord.com/developers/docs/resources/guild)
		return Session.settings_ready['guilds'][self.guildID]['discovery_splash']

	@property
	def msgNotificationSettings(self): #returns an int, 0=all messages, 1=only mentions (https://discord.com/developers/docs/resources/guild#guild-object-default-message-notification-level)
		return Session.settings_ready['guilds'][self.guildID]['default_message_notifications']

	@property
	def rulesChannelID(self):
		return Session.settings_ready['guilds'][self.guildID]['rules_channel_id']

	@property
	def verificationLvl(self): #returns an int, 0-4 (https://discord.com/developers/docs/resources/guild#guild-object-verification-level)
		return Session.settings_ready['guilds'][self.guildID]['verification_level']

	@property
	def features(self): #returns a list of strings (https://discord.com/developers/docs/resources/guild#guild-object-guild-features)
		return Session.settings_ready['guilds'][self.guildID]['features']

	@property
	def joinTime(self): #returns when you joined the server, type string
		return Session.settings_ready['guilds'][self.guildID]['joined_at']

	@property
	def region(self):
		return Session.settings_ready['guilds'][self.guildID]['region']

	@property
	def applicationID(self): #returns application id of the guild creator if it is bot-created (https://discord.com/developers/docs/resources/guild#guild-object-guild-features)
		return Session.settings_ready['guilds'][self.guildID]['application_id']

	@property
	def afkChannelID(self): #not sure what this is
		return Session.settings_ready['guilds'][self.guildID]['afk_channel_id']

	@property
	def icon(self): #https://discord.com/developers/docs/reference#image-formatting
		return Session.settings_ready['guilds'][self.guildID]['icon']

	@property
	def name(self):
		return Session.settings_ready['guilds'][self.guildID]['name']

	@property
	def maxVideoChannelUsers(self):
		return Session.settings_ready['guilds'][self.guildID]['max_video_channel_users']

	@property
	def roles(self): #https://discord.com/developers/docs/topics/permissions#role-object
		return Session.settings_ready['guilds'][self.guildID]['roles']

	@property
	def publicUpdatesChannelID(self):
		return Session.settings_ready['guilds'][self.guildID]['public_updates_channel_id']

	@property
	def systemChannelFlags(self): #https://discord.com/developers/docs/resources/guild#guild-object-system-channel-flags
		return Session.settings_ready['guilds'][self.guildID]['system_channel_flags']

	@property
	def mfaLvl(self): #https://discord.com/developers/docs/resources/guild#guild-object-mfa-level
		return Session.settings_ready['guilds'][self.guildID]['mfa_level']

	@property
	def afkTimeout(self): #returns type int, unit seconds, https://discord.com/developers/docs/resources/guild
		return Session.settings_ready['guilds'][self.guildID]['afk_timeout']

	@property
	def hashes(self): #https://github.com/discord/discord-api-docs/issues/1642
		return Session.settings_ready['guilds'][self.guildID]['guild_hashes']

	@property
	def systemChannelID(self): #returns an int, the id of the channel where guild notices such as welcome messages and boost events are posted
		return Session.settings_ready['guilds'][self.guildID]['system_channel_id']

	@property
	def lazy(self): #slightly different naming format since it returns a boolean (https://luna.gitlab.io/discord-unofficial-docs/lazy_guilds.html)
		return Session.settings_ready['guilds'][self.guildID]['lazy']

	@property
	def numBoosts(self): #get number of boosts the server has gotten
		return Session.settings_ready['guilds'][self.guildID]['premium_subscription_count']

	@property
	def large(self): #slightly different naming format since it returns a boolean, large if more than 250 members
		return Session.settings_ready['guilds'][self.guildID]['large']

	@property
	def threads(self):
		return Session.settings_ready['guilds'][self.guildID]['threads']

	@property
	def explicitContentFilter(self): #https://discord.com/developers/docs/resources/guild#guild-object-explicit-content-filter-level
		return Session.settings_ready['guilds'][self.guildID]['explicit_content_filter']

	@property
	def splashHash(self): #not sure what this is for
		return Session.settings_ready['guilds'][self.guildID]['splash']

	@property
	def memberCount(self):
		return Session.settings_ready['guilds'][self.guildID]['member_count']

	@property
	def description(self):
		return Session.settings_ready['guilds'][self.guildID]['description']

	@property
	def vanityUrlCode(self):
		return Session.settings_ready['guilds'][self.guildID]['vanity_url_code']

	@property
	def preferredLocale(self):
		return Session.settings_ready['guilds'][self.guildID]['preferred_locale']

	def updateChannelData(self, channelID, channelData): #can also be used to update categories
		Session.settings_ready['guilds'][self.guildID]['channels'][channelID].update(channelData)

	def setChannelData(self, channelID, channelData): #can also be used to update categories
		Session.settings_ready['guilds'][self.guildID]['channels'][channelID] = channelData

	def removeChannelData(self, channelID):
		Session.settings_ready['guilds'][self.guildID]['channels'].pop(channelID, None)

	@property
	def channelsAndCategories(self): #returns all categories and all channels, all the data about that, wall of data so it can be a bit overwhelming, useful if you want to check how many channels your server has since discord counts categories as channels
		return Session.settings_ready['guilds'][self.guildID]['channels']

	@property
	def allChannelAndCategoryIDs(self): #all of them, even ones you've been removed from
		return list(self.channelsAndCategories)

	@property
	def channelAndCategoryIDs(self):
		return [channelID for channelID in self.channelsAndCategories if "removed" not in self.channelsAndCategories[channelID]]

	@property
	def categories(self): #all data about guild categories, can be overwhelming
		return {
		    i: self.channelsAndCategories[i]
		    for i in self.channelsAndCategories
		    if self.channelsAndCategories[i]['type'] == 4
		}

	@property
	def categoryIDs(self):
		return list(self.categories)

	def category(self, categoryID):
		return self.categories[categoryID]

	@property
	def channels(self): #all data about all guild channels, can be overwhelming
		return {
		    i: self.channelsAndCategories[i]
		    for i in self.channelsAndCategories
		    if self.channelsAndCategories[i]['type'] != 4
		}

	@property
	def channelIDs(self):
		return list(self.channels)

	def channel(self, channelID):
		return self.channels[channelID]

	@property
	def voiceStates(self): #https://discord.com/developers/docs/resources/voice#voice-state-object
		return Session.settings_ready_supp['voice_states'][self.guildID]

	@property
	def me(self): #my roles, nick, etc in a guild
		return Session.settings_ready['guilds'][self.guildID]['my_data']

	@property
	def applicationCommandCount(self):
		return Session.settings_ready['guilds'][self.guildID].get('application_command_count')

	@property
	def maxMembers(self):
		return Session.settings_ready['guilds'][self.guildID]['max_members']
	
	@property
	def stages(self):
		return Session.settings_ready['guilds'][self.guildID]['stage_instances']

	@property
	def stickers(self):
		return Session.settings_ready['guilds'][self.guildID]['stickers']

###specific relationship
class relationship(Session): #not the same organization as class guild
	def __init__(self, userID):
		self.userID = userID

	@property
	def data(self): #usernames and discriminators are no longer provided in this data
		return Session.settings_ready['relationships'][self.userID]

###specific DM
class DM(Session):
	def __init__(self, DMID):
		self.DMID = DMID

	@property
	def data(self):
		return Session.settings_ready['private_channels'][self.DMID]

	def updateData(self, data):
		Session.settings_ready['private_channels'][self.DMID].update(data)

	@property
	def recipients(self): #returns everyone in that DM except you
		return self.data['recipient_ids']

###specific User Guild Settings; keep in mind that user guild settings also includes some group dm notification settings stuff
class userGuildSetting(Session):
	def __init__(self, guildID):
		self.guildID = guildID

	@property
	def data(self):
		if len(Session.settings_ready['user_guild_settings']['entries']) == 0:
			return None
		for i in range(len(Session.settings_ready['user_guild_settings']['entries'])):
			if Session.settings_ready['user_guild_settings']['entries'][i]['guild_id'] == self.guildID:
				return Session.settings_ready['user_guild_settings']['entries'][i]
		return None
