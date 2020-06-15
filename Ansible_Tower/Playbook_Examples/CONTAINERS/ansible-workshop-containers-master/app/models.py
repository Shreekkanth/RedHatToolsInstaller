class ItemModel:
    def __init__(self, fqdn, ip_address, mac_address, owned_by, serial_number):
        # We will automatically generate the new id
        self.id = 0
        self.fqdn = fqdn
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.owned_by = owned_by
        self.serial_number = serial_number
