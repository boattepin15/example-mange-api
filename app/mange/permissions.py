from rest_framework.permissions import BasePermission, SAFE_METHODS
class PublicReadOnly(BasePermission):
    """
    ปรับแต่ง permission เพื่อผู้ใช้งานทั่วไป ผ่านได้อย่างเดียว read-only.
    """

    def has_permission(self, request, view):
        # กำหนดให้ User ทั่วไป อ่านได้เท่านั้น
        if request.method in SAFE_METHODS:
            return True
        # ถ้ากรณีที่ไม่ใช่ ผู้ใช้งานทั่วไป ก็ตะสามารถแก้ไขได้
        return request.user and request.user.is_staff and request.user.is_supueruser