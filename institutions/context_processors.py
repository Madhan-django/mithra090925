from .models import SchoolMenuPermission, GroupMenuPermission
from jacobreports.models import PrincipalLogAccessMapping
from staff.models import staff


class _AllEnabled:
    """Returned for superadmin or when no permission record exists — all menus visible."""
    def __getattr__(self, name):
        return True


def menu_permissions(request):
    if not request.user.is_authenticated:
        return {'menu_perm': None, 'group_perm': None}

    is_superadmin = request.user.groups.filter(name='superadmin').exists()
    sch_id = request.session.get('sch_id')

    # ── School-level module permissions ──────────────────────────────────────
    if is_superadmin:
        menu_perm = _AllEnabled()
    elif sch_id:
        try:
            menu_perm = SchoolMenuPermission.objects.get(school_id=sch_id)
        except SchoolMenuPermission.DoesNotExist:
            menu_perm = _AllEnabled()
    else:
        menu_perm = _AllEnabled()

    # ── Group-level menu permissions (per school) ─────────────────────────────
    if is_superadmin:
        group_perm = _AllEnabled()
    else:
        first_group = request.user.groups.first()
        if first_group and sch_id:
            try:
                group_perm = GroupMenuPermission.objects.get(
                    group=first_group, school_id=sch_id
                )
            except GroupMenuPermission.DoesNotExist:
                # No record for this group+school yet — allow everything
                group_perm = _AllEnabled()
        else:
            group_perm = _AllEnabled()

    # ── Principal Log access ──────────────────────────────────────────────────
    has_principal_log_access = False
    if request.user.groups.filter(name__in=['superadmin', 'Admin']).exists():
        has_principal_log_access = True
    elif sch_id:
        try:
            current_staff = staff.objects.get(staff_user=request.user)
            has_principal_log_access = PrincipalLogAccessMapping.objects.filter(
                school_name_id=sch_id, staff_member=current_staff
            ).exists()
        except staff.DoesNotExist:
            pass

    return {'menu_perm': menu_perm, 'group_perm': group_perm, 'current_sch_id': sch_id,
            'has_principal_log_access': has_principal_log_access}
