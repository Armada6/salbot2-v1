from .config_helper import ConfigHelper


class PermissionManager:
    def __init__(self):
        self.conf = ConfigHelper("./config/perms.json")
        self.cfg = self.conf.read()

    def has_perms(self, roles: list, uid: str, required: int):
        overrides = self.cfg["overrides"]
        if uid in overrides:
            return overrides[uid] >= required

        role_perms = self.cfg["roles"]
        for role in roles:
            if role in role_perms:
                if role_perms[role] >= required:
                    return True
        return False

    def add_role(self, name: str, level: int):
        perms = self.conf.read()
        perms["roles"][name] = level
        self.conf.write(perms)

    def modify_role(self, name: str, level: int):
        self.add_role(name, level)

    def del_role(self, name: str):
        perms = self.conf.read()
        perms["roles"].pop(name)
        self.conf.write(perms)

    def add_override(self, uid: str, level: int):
        perms = self.conf.read()
        perms["overrides"][uid] = level
        self.conf.write(perms)

    def modify_override(self, uid: str, level: int):
        self.add_override(uid, level)

    def del_override(self, uid: str):
        perms = self.conf.read()
        perms["overrides"].pop(uid)
        self.conf.write(perms)