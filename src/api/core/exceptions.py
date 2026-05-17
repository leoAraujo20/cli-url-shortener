class InvalidURLException(ValueError):
    def __init__(self, url: str, message: str):
        self.url = url
        self.message = message
        super().__init__(f"Erro de validação de URL: {message} (URL: {url})")
