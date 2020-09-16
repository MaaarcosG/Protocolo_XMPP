class Usuario():
    def __init__(self, user, status, show, online, registrer):
        self.user = user
        self.status = status
        self.show = show
        self.online = online
        self.register = registrer

    def states_user(self, status, show):
        self.status = status
        self.show = show
    
    def set_online(self, online):
        self.online = online

    def get_user(self):
        return [self.user, self.status, self.show, self.online, self.register]

