from django.shortcuts import redirect
from django.contrib import messages


class GroupPermissionMiddleware:
    """
    View-level enforcement of GroupMenuPermission.

    For every incoming request, maps the URL prefix to a module name,
    then checks whether the user's group has that module enabled for the
    current school (stored in session).

    Rules:
    - Unauthenticated requests pass through (login_required handles those).
    - Superadmin always passes.
    - If the user has no group, or no school in session, passes through.
    - If a GroupMenuPermission record exists and the module is False → redirect.
    - If no record exists yet → passes through (default: all open).
    """

    # (url_prefix, module_field_name_in_GroupMenuPermission)
    URL_MODULE_MAP = [
        ('/admission/',    'admission'),
        ('/students/',     'students'),
        ('/staff/',        'staffs'),
        ('/academic/',     'academics'),
        ('/lessonplan/',   'academics'),
        ('/grievance/',    'academics'),
        ('/timetable/',    'timetable'),
        ('/fees/',         'finance'),
        ('/payroll/',      'payroll'),
        ('/transport/',    'transport'),
        ('/hostel/',       'hostel'),
        ('/pettycash/',    'petty_cash'),
        ('/examination/',  'examination'),
        ('/qbank/',        'question_bank'),
        ('/library/',      'library'),
        ('/assets/',       'assets'),
        ('/inventory/',    'inventory'),
        ('/visitors/',     'visitors'),
        ('/reports/',      'reports'),
        ('/automate/',     'reports'),
        ('/jacobreports/', 'jacob_reports'),
        ('/setup/',        'configurations'),
        ('/digiattend/',   'staffs'),
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            module = self._resolve_module(request.path)
            if module and not self._has_access(request, module):
                messages.error(request, 'You do not have permission to access this section.')
                return redirect('home_dashboard')
        return self.get_response(request)

    # ── helpers ──────────────────────────────────────────────────────────────

    def _resolve_module(self, path):
        for prefix, module in self.URL_MODULE_MAP:
            if path.startswith(prefix):
                return module
        return None

    def _has_access(self, request, module):
        # Superadmin bypasses all checks
        if request.user.groups.filter(name='superadmin').exists():
            return True

        sch_id     = request.session.get('sch_id')
        first_group = request.user.groups.first()

        # No group assigned or no school selected → allow through
        if not first_group or not sch_id:
            return True

        from institutions.models import GroupMenuPermission
        try:
            perm = GroupMenuPermission.objects.get(group=first_group, school_id=sch_id)
            return bool(getattr(perm, module, True))
        except GroupMenuPermission.DoesNotExist:
            # No record configured yet → allow (open by default)
            return True
