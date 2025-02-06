from json import load

class Lang:
    def __init__(self, lang) -> None:
        with open(f"assets/lang/{lang}/game.json", encoding='utf-8') as file:
            self.lang_data = load(file)

    def get_string(self, name) -> str:
        return self.lang_data[name]

    def change_lang(self, lang) -> None:
        with open(f"assets/lang/{lang}/game.json", encoding='utf-8') as file:
            self.lang_data = load(file)
