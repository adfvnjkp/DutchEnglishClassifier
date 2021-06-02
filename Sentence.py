class Sentence:
    def __init__(self, language: str, text: str):
        """
        sentence instance initialization
        :param language: String label of language current sentence holds
        :param text: String text of current sentence

        """
        self.language = language
        self.text = text.split(" ")
        self.attr = [
            self.contain_english(),
            self.contain_dutch(),
            self.contain_de(),
            self.contain_a(),
            self.contain_van(),
            self.contain_een(),
            self.contain_het(),
            self.contain_the(),
            self.contain_and(),
            self.contain_preposition()
        ]

    def contain_english(self):
        common_en = "I It will me mine no not he him his she her it we our us they them their there here about for " \
                     "with as so be to As".split(" ")
        for word in self.text:
            if word in common_en:
                return True

        return False

    def contain_dutch(self):
        common_du = "Naar naar Deze deze Ik Ons ben Ben ons Meest meest Voor voor niet met hij zijn be ik het ze" \
                     " wij hem weten jouw dan ook onze ze er hun zo over".split(" ")
        for word in self.text:
            if word in common_du:
                return True

        return False

    def contain_de(self):
        for word in self.text:
            if (word == "de") or (word == "De"):
                return True

        return False

    def contain_a(self):
        for word in self.text:
            if word in ["a", "an", "A", "An"]:
                return True

        return False

    def contain_van(self):
        for word in self.text:
            if word in ["van", "voor", "Voor", "Van"]:
                return True

        return False

    def contain_een(self):
        for word in self.text:
            if word in ["een", "Een", "En", "en"]:
                return True

        return False

    def contain_het(self):
        for word in self.text:
            if word in ["Het", "het"]:
                return True

        return False

    def contain_the(self):
        for word in self.text:
            if word in ["The", "the"]:
                return True

        return False

    def contain_and(self):
        for word in self.text:
            if word in ["and", "And"]:
                return True

        return False

    def contain_preposition(self):
        for word in self.text:
            if word in ("in on at by for since to toward into with which without within In At and When Where What "
                        "when where what Which".split(" ")):
                return True

        return False

    def __str__(self) -> str:
        """
        helper func print string format

        """
        return "Text: " + self.text + "\nLanguage: " + self.language + "\nAttributes: " + str(self.attr)
