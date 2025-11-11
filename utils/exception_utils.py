#Exception classes defined here
# These classes are used in global handlers of the app, where they have a corresponding logic assigned.

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