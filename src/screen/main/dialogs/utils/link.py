import webbrowser

from kivymd.uix.boxlayout import MDBoxLayout

class Link(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super(Link, self).__init__(*args, **kwargs)

    def openLink(self, linkURL):
        loginPhrase = '&a=login&pojam=zetovci'
        webbrowser.open(linkURL + loginPhrase)