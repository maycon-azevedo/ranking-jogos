class NotFoundError(Exception):
    def __init__(self, detail: str = "Recurso não encontrado"):
        self.detail = detail


class ForbiddenError(Exception):
    def __init__(self, detail: str = "Sem permissão"):
        self.detail = detail
