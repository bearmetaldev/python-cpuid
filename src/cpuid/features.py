import struct
from typing import Optional

from cpuid.bindings import cpuid

from cpuid.register_map import BooleanField, register_map, RegisterField


def vendor() -> bytes:
    _, ebx, ecx, edx = cpuid(0)
    return struct.pack("III", ebx, edx, ecx)


@register_map
class ProcessorFeaturesEax:
    extended_family = RegisterField(int, 20, 8)
    extended_model = RegisterField(int, 16, 4)
    base_family = RegisterField(int, 8, 4)
    base_model = RegisterField(int, 4, 4)
    stepping = RegisterField(int, 0, 4)


@register_map
class ProcessorFeaturesEbx:
    local_apic_id = RegisterField(int, 24, 8)
    logical_processor_count = RegisterField(int, 16, 8)
    cl_flush = RegisterField(int, 8, 8)
    brand_id_8bit = RegisterField(int, 0, 8)


@register_map
class ProcessorFeaturesEcx:
    has_rdrand = BooleanField(30)
    has_f16c = BooleanField(29)
    has_avx = BooleanField(28)
    has_osxsave = BooleanField(27)
    has_xsave = BooleanField(26)
    has_aes = BooleanField(25)
    has_popcnt = BooleanField(23)
    has_sse42 = BooleanField(20)
    has_sse41 = BooleanField(19)
    has_cmpxchg16b = BooleanField(13)
    has_fma = BooleanField(12)
    has_ssse3 = BooleanField(9)
    has_monitor = BooleanField(3)
    has_pclmulqdq = BooleanField(1)
    has_sse3 = BooleanField(0)


@register_map
class ProcessorFeaturesEdx:
    has_htt = BooleanField(28)
    has_sse2 = BooleanField(26)
    has_sse = BooleanField(25)
    has_fxsr = BooleanField(24)
    has_mmx = BooleanField(23)
    has_clfsh = BooleanField(19)
    has_pse36 = BooleanField(17)
    has_pat = BooleanField(16)
    has_cmov = BooleanField(15)
    has_mca = BooleanField(14)
    has_pge = BooleanField(13)
    has_mtrr = BooleanField(12)
    has_sysenter_sysexit = BooleanField(11)
    has_apic = BooleanField(9)
    has_cmpxchg8b = BooleanField(8)
    has_mce = BooleanField(7)
    has_pae = BooleanField(6)
    has_msr = BooleanField(5)
    has_tsc = BooleanField(4)
    has_pse = BooleanField(3)
    has_de = BooleanField(2)
    has_vme = BooleanField(1)
    has_fpu = BooleanField(0)


class ProcessorFeatures:
    def __init__(self, eax: int, ebx: int, ecx: int, edx: int):
        eax_map = ProcessorFeaturesEax.from_register_value(eax)
        ebx_map = ProcessorFeaturesEbx.from_register_value(ebx)
        ecx_map = ProcessorFeaturesEcx.from_register_value(ecx)
        edx_map = ProcessorFeaturesEdx.from_register_value(edx)

        # Remap register map attributes to this instance
        for reg_map in (eax_map, ebx_map, ecx_map, edx_map):
            for field in reg_map.__fields__:
                setattr(self, field, getattr(reg_map, field))


def processor_features() -> ProcessorFeatures:
    eax, ebx, ecx, edx = cpuid(1)
    return ProcessorFeatures(eax, ebx, ecx, edx)


@register_map
class SecureEncryptionEax:
    has_vmsa_register_protection = BooleanField(24)
    has_host_ibs_prevention = BooleanField(15)
    has_debug_swap = BooleanField(14)
    has_alternate_injection = BooleanField(13)
    has_restricted_injection = BooleanField(12)
    requires_64_bit_host = BooleanField(11)
    has_hw_enforced_cache_coherency = BooleanField(10)
    has_secure_tsc = BooleanField(8)
    has_vm_permission_levels = BooleanField(5)
    has_sev_snp = BooleanField(4)
    has_sev_es = BooleanField(3)
    has_page_flush_msr = BooleanField(2)
    has_sev = BooleanField(1)
    has_sme = BooleanField(0)


@register_map
class SecureEncryptionEbx:
    num_vm_permission_levels = RegisterField(int, 12, 4)
    phys_addr_reduction = RegisterField(int, 6, 6)
    c_bit_position = RegisterField(int, 0, 6)


class SecureEncryptionInfo:
    def __init__(self, eax: int, ebx: int, ecx: int, edx: int):
        eax_map = SecureEncryptionEax.from_register_value(eax)
        ebx_map = SecureEncryptionEbx.from_register_value(ebx)

        # Remap register map attributes to this instance
        for field in eax_map.__fields__:
            setattr(self, field, getattr(eax_map, field))
        for field in ebx_map.__fields__:
            setattr(self, field, getattr(ebx_map, field))

        self.num_encrypted_guests = ecx
        self.min_asid_value_for_sev_no_es = edx


def secure_encryption_info() -> Optional[SecureEncryptionInfo]:
    try:
        eax, ebx, ecx, edx = cpuid(0x8000001F)
    except ValueError:
        return None

    return SecureEncryptionInfo(eax, ebx, ecx, edx)
