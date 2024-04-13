class RollException(BaseException):
    def __init__(self, information):
        super().__init__()
        self.information = information
