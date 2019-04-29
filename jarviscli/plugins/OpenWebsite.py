import webbrowser
import os
from plugin import plugin, require

FILE_PATH = os.path.abspath(os.path.dirname(__file__))


@require(network=True)
@plugin("open website")
class OpenWebsite:
    """
    This plugin will open a website using some params.

    The user can open a simple website giving a complete link or
    inputting the name of the website like the examples:

    > open website www.google.com
    > open website github
    > open website github username
    """
    def __call__(self, jarvis, link):
        inputs = link.split(' ', 1)
        self.main_link = inputs[0]
        complement = ""
        if len(inputs) > 1:
            complement = inputs[1]

        if self.has_on_links_dictionary():
            webbrowser.open(self.main_link + complement)
        elif self.verify_link():
            webbrowser.open(self.main_link)
        else:
            print("Sorry, I can't open this link please try again.")

    def has_on_links_dictionary(self):
        websites_csv = \
            open(os.path.join(FILE_PATH, "../data/websites.csv"), 'r')
        for website in websites_csv:
            information = website.split(',', 1)
            if self.main_link == information[0]:
                self.main_link = information[1]
                return True

        return False

    def verify_link(self):
        if ((self.main_link[:8] != "https://" and
             self.main_link[:7] != "http://" and
             self.main_link[:3] != "www") or
                ("com" not in self.main_link)):
            return False
        self.fix_link()
        return True

    def fix_link(self):
        """
        When the links come as input they come without '.'
        > open website www.google.com
        What I get here:
        wwwgooglecom

        So this function get the link without '.' and add the '.'
        """
        if "www" in self.main_link:
            splited_link = self.main_link.split('www', 1)
            self.main_link = splited_link[0] + 'www.' + splited_link[1]

        if self.main_link[:3] == "www":
            self.main_link = "http://" + self.main_link

        if "com" in self.main_link:
            splited_link = self.main_link.split('com', 1)
            self.main_link = ""
            for index in range(len(splited_link) - 1):
                self.main_link += splited_link[index]

            self.main_link += ".com" + splited_link[len(splited_link) - 1]