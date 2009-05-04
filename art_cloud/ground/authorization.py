
# this isn't used by anyone.  yet.

AUTHORIZATION_META_NAME = 'AuthorizationMeta'


class Authorization:
	def __init__(self, create=False, read_all=False, read_own=False, update_all=False, update_own=False, delete_all=False, delete_own=False):
		self.create = create
		self.read_all = read_all
		self.read_own = read_own
		self.update_all = update_all
		self.update_own = update_own
		self.delete_all = delete_all
		self.delete_own = delete_own
