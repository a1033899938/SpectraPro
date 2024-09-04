class OutputRedirector:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        self.text_edit.insertPlainText(message)
        self.text_edit.ensureCursorVisible()

    def flush(self):
        # This method is needed for Python 3.x
        pass
