class Passwords:
    # def __init__(self):
    #     self.site = None
    #     self.password = None

    def __str__(self):
        return f"Site: {self.site}; Username:{self.username}; Password: {self.password}"

    def __init__(self, site, username, passwrd):
        self.site = site
        self.username = username
        self.password = passwrd

    def get_site(self):
        return self.site

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password