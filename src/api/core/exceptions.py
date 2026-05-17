class InvalidURLException(ValueError):
    def __init__(self, url: str, message: str):
        self.url = url
        self.message = message
        super().__init__(f"Erro de validação de URL: {message} (URL: {url})")


class URLNotFoundException(ValueError):
    def __init__(self, short_id: str):
        self.short_id = short_id
        self.message = f"URL com short_id '{short_id}' não encontrada."
        super().__init__(self.message)
