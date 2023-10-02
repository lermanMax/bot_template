from asyncpg.exceptions import UniqueViolationError


AlreadyExist = UniqueViolationError
DoesNotExist = 0