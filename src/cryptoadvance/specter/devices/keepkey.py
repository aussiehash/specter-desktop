from .hwi_device import HWIDevice

class Keepkey(HWIDevice):
    def __init__(self, name, alias, device_type, keys, fullpath, manager):
        HWIDevice.__init__(self, name, alias, 'keepkey', keys, fullpath, manager)
        self.sd_card_support = False
        self.qr_code_support = False
        self.supports_hwi_multisig_display_address = True
