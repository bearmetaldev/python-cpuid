from cpuid.register_map import BooleanField, RegisterField, register_map


@register_map
class Register32Bits:
    version = RegisterField(int, offset=16, length=16)
    has_feature1 = BooleanField(2)
    has_feature2 = BooleanField(1)
    has_feature3 = BooleanField(0)


def test_register_map_32_bits():
    version = 23

    base_reg_value = version << 16

    all_features = Register32Bits.from_register_value(base_reg_value | 0x7)
    assert all_features.version == version
    assert all_features.has_feature1
    assert all_features.has_feature2
    assert all_features.has_feature3

    no_features = Register32Bits.from_register_value(base_reg_value)
    assert no_features.version == version
    assert not no_features.has_feature1
    assert not no_features.has_feature2
    assert not no_features.has_feature3

    max_int_reg = Register32Bits.from_register_value(0xFFFFFFFF)
    assert max_int_reg.version == 0xFFFF
    assert max_int_reg.has_feature1
    assert max_int_reg.has_feature2
    assert max_int_reg.has_feature3
