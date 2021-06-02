class TreeNode:
    def __init__(self, attr: int, language: str):
        """
        Tree Node instance initialization for current tree node
        :param attr: Integer (0, 9), labelling correlate to Sentence Class's attribute list value
        :param language: String "en" / "nl", labelling language classification of current tree node

        """
        self.attr = attr
        self.language = language
        self.left = None
        self.right = None

    def setLeft(self, newNode):
        self.left = newNode

    def setRight(self, newNode):
        self.right = newNode

    def setLanguage(self, language: str):
        self.language = language

    def setAttr(self, attr: int):
        self.attr = attr

    def __str__(self):
        """
        for output tree structure

        :return:
        """
        if self.language != "":
            return "<" + self.language + "> - attr: (" + str(self.attr) + ")"
        else:
            return "attr < " + str(self.attr) + "> \nleft: { " + str(self.left) + "} \nright: {" + str(self.right) + "}"
