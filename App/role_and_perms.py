from enum import Enum
from typing import List

class Role(str, Enum):
    admin = "admin"
    user = "user"
    
    def __str__(self):
        return self.value

class Permission(str, Enum):
    read = "read"
    write = "write"
    delete = "delete"
    
    def __str__(self):
        return self.value


permissions = {
    Role.admin: [Permission.read, Permission.write, Permission.delete],
    Role.user: [Permission.read],
}

def has_permission(user_roles: List[Role], required_permission: Permission) -> bool:
    for role in user_roles:
        if required_permission in permissions.get(role, []):
            return True
    return False

