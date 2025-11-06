# Aqui van clases de excepciones para mantener el codigo comprensible
# Antes estabamos usando ValueError para todo

# Estas clases se usan en los manejadores globales de la app donde
# se les asigna el codigo correspondiente.

class AuthError(Exception):
    pass

class InactiveUserError(Exception):
    pass

class RegisterError(Exception):
    pass

class UpdateError(Exception):
    pass

class DeleteError(Exception):
    pass

class ConflictError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class NotFoundError(Exception):
    pass