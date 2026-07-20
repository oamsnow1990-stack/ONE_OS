from typing import Dict, Set

class PermissionManager:
    """ระบบควบคุมสิทธิ์ (RBAC) เพื่อป้องกัน Agent รันคำสั่งอันตรายโดยไม่ได้รับอนุมัติจาก Boss"""
    
    def __init__(self):
        # โครงสร้าง: { "role_name": set("action1", "action2") }
        self._roles_permissions: Dict[str, Set[str]] = {}

    def grant_permission(self, role: str, action: str) -> None:
        """มอบสิทธิ์ให้ Role นั้นๆ ทำ Action ได้"""
        if role not in self._roles_permissions:
            self._roles_permissions[role] = set()
        self._roles_permissions[role].add(action)

    def revoke_permission(self, role: str, action: str) -> None:
        """ริบสิทธิ์คืนจาก Role"""
        if role in self._roles_permissions and action in self._roles_permissions[role]:
            self._roles_permissions[role].remove(action)

    def has_permission(self, role: str, action: str) -> bool:
        """ตรวจสอบว่า Role มีสิทธิ์ทำ Action นี้หรือไม่"""
        # BOSS คือ Super Admin เสมอ ทำได้ทุกอย่าง
        if role == "BOSS":
            return True
            
        permissions = self._roles_permissions.get(role, set())
        # ตรวจสอบสิทธิ์แบบระบุเจาะจง หรือสิทธิ์แบบครอบจักรวาล (*)
        return action in permissions or "*" in permissions

    def require_permission(self, role: str, action: str) -> None:
        """เหมือน has_permission แต่ถ้าไม่มีสิทธิ์ จะโยน Error ทันที (ใช้คั่นก่อนรันฟังก์ชัน)"""
        if not self.has_permission(role, action):
            raise PermissionError(f"Access Denied: Role '{role}' does not have permission for '{action}'.")