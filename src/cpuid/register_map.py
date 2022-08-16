from typing import Type, Dict


class RegisterField:
    def __init__(self, field_type: Type, offset: int, length: int):
        self.field_type = field_type
        self.offset = offset
        self.length = length


class BooleanField(RegisterField):
    def __init__(self, offset):
        super().__init__(field_type=bool, offset=offset, length=1)


def _init_fn(fields: Dict[str, RegisterField]):
    def init(self, **kwargs):
        expected_fields = set(fields)
        provided_fields = set(kwargs)

        if missing_fields := expected_fields - provided_fields:
            raise ValueError(f"Missing fields: {missing_fields}")

        for field in fields:
            setattr(self, field, kwargs[field])

    return init


def _from_register_value(fields):
    def from_reg_val(cls, reg_value: int):

        field_values = {}
        for field_name, field in fields.items():
            field_mask = (1 << field.length) - 1
            field_value = field.field_type((reg_value >> field.offset) & field_mask)
            field_values[field_name] = field_value

        return cls(**field_values)

    return from_reg_val


def _generate_regmap_methods(cls):
    fields = {
        field_name: getattr(cls, field_name)
        for field_name in dir(cls)
        if isinstance(getattr(cls, field_name), RegisterField)
    }

    cls.__fields__ = fields
    cls.__init__ = _init_fn(fields)
    cls.from_register_value = classmethod(_from_register_value(fields))

    return cls


# TODO: this implementation is quite rudimentary. Possible improvements:
#       * proper declaration of __init__, using the same pattern as dataclasses
#       * support for initialization from bytes
def register_map(cls):
    """
    A decorator for register map classes.

    Automatically generates methods to initialize register map classes
    from a register value.
    """
    def wrap(cls):
        return _generate_regmap_methods(cls)

    return wrap(cls)
