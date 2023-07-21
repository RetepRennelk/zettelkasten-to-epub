class Wikilink:
    def __init__(self, embed, name, alias):
        self.embed, self.name, self.alias = embed, name, alias

    def __str__(self):
        return f'embed={self.embed},name={self.name},alias={self.alias}'