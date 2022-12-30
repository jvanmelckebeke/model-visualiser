from tools import generate_uuid


class TikzElement:
    def __init__(self, internal_name, depends_on=None):
        self.internal_name = internal_name
        self.depends_on = depends_on if depends_on is not None else []

    def to_code(self):
        raise NotImplementedError()


class TikzArg(TikzElement):
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        super().__init__(generate_uuid(), depends_on=None)

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
        super().__init__(generate_uuid(), depends_on=None)

    def to_code(self):
        return str(self)

    def __str__(self):
        return ",".join([str(option) for option in self.options]) if self.options else ""
