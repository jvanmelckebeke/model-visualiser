class TikzElement:
    def to_code(self):
        raise NotImplementedError()


class TikzArg(TikzElement):
    def __init__(self, key, value=None):
        self.key = key
        self.value = value

    def to_code(self):
        return str(self)

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.value is None:
            return str(self.key)
        return f"{self.key}={self.value}"


class TikzOptions(TikzElement):
    def __init__(self, *args, **kwargs):
        self.options = [TikzArg(arg) for arg in args]
        self.options.extend([TikzArg(key, value) for key, value in kwargs.items()])

    def to_code(self):
        return str(self)

    def __str__(self):
        return ",".join([str(option) for option in self.options]) if self.options else ""
