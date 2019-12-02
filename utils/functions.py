import ulid


def pipe(*functions):
    def piped(arg):
        result = arg
        for f in functions:
            result = f(result)
        return result

    return piped


def create_id():
    return str(ulid.new())
