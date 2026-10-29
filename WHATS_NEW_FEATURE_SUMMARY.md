# What's New Feature — Implementation Summary
Date: 2026-09-19

---

## Overview
Built a "What's New" feature update system that:
- Displays a feed card on the staff home dashboard
- Lets superadmins add/edit/delete feature entries from within the app (no Django admin required)
- Has a management link in the sidebar (superadmin only)

---

## 1. Model — `setup/models.py`

Added `AppUpdate` at the bottom of the file:

```python
class AppUpdate(models.Model):
    BADGE_CHOICES = [
        ('New', 'New'),
        ('Improved', 'Improved'),
        ('Fixed', 'Fixed'),
    ]
    title       = models.CharField(max_length=200)
    description = models.TextField()
    date        = models.DateField()
    badge       = models.CharField(max_length=20, choices=BADGE_CHOICES, default='New')
    icon        = models.CharField(max_length=60, default='ri-star-line',
                                   help_text='Remix icon class, e.g. ri-star-line')
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
```

**Migration created:** `setup/migrations/0014_appupdate.py`
Run in production:
```bash
python manage.py migrate
```

---

## 2. Admin — `setup/admin.py`

Import added:
```python
from .models import academicyr, currentacademicyr, sclass, receipt_template, section, AppUpdate
```

Admin class added:
```python
@admin.register(AppUpdate)
class AppUpdateAdmin(admin.ModelAdmin):
    list_display  = ('title', 'badge', 'date', 'is_active')
    list_filter   = ('badge', 'is_active')
    list_editable = ('is_active',)
    ordering      = ('-date',)
```

---

## 3. Form — `setup/forms.py`

Import added:
```python
from .models import ..., AppUpdate
```

Form class added:
```python
class AppUpdateForm(forms.ModelForm):
    class Meta:
        model  = AppUpdate
        fields = ('title', 'description', 'date', 'badge', 'icon', 'is_active')
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'pc-input', 'placeholder': 'e.g. Morning Report'}),
            'description': forms.Textarea(attrs={'class': 'pc-input', 'rows': 3}),
            'date':        forms.DateInput(attrs={'class': 'pc-input', 'type': 'date'}),
            'badge':       forms.Select(attrs={'class': 'pc-input'}),
            'icon':        forms.TextInput(attrs={'class': 'pc-input', 'placeholder': 'e.g. ri-star-line', 'id': 'icon-input'}),
            'is_active':   forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
```

---

## 4. Views — `setup/views.py`

Imports added:
```python
from .models import ..., AppUpdate
from .forms  import ..., AppUpdateForm
```

Four views added (all restricted to `superadmin`):

```python
@allowed_users(allowed_roles=['superadmin'])
def app_update_list(request):
    updates = AppUpdate.objects.order_by('-date')
    return render(request, 'setup/app_update_list.html', {'updates': updates})


@allowed_users(allowed_roles=['superadmin'])
def app_update_add(request):
    if request.method == 'POST':
        form = AppUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature update added successfully.')
            return redirect('app_update_list')
    else:
        form = AppUpdateForm()
    return render(request, 'setup/app_update_form.html', {'form': form, 'edit': False})


@allowed_users(allowed_roles=['superadmin'])
def app_update_edit(request, pk):
    update = AppUpdate.objects.get(pk=pk)
    if request.method == 'POST':
        form = AppUpdateForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature update saved.')
            return redirect('app_update_list')
    else:
        form = AppUpdateForm(instance=update)
    return render(request, 'setup/app_update_form.html', {'form': form, 'edit': True, 'update': update})


@allowed_users(allowed_roles=['superadmin'])
def app_update_delete(request, pk):
    AppUpdate.objects.filter(pk=pk).delete()
    messages.success(request, 'Feature update deleted.')
    return redirect('app_update_list')
```

---

## 5. URLs — `setup/urls.py`

Four paths added:
```python
path('whats-new/',                login_required(views.app_update_list),   name='app_update_list'),
path('whats-new/add/',            login_required(views.app_update_add),    name='app_update_add'),
path('whats-new/<int:pk>/edit/',  login_required(views.app_update_edit),   name='app_update_edit'),
path('whats-new/<int:pk>/delete/',login_required(views.app_update_delete), name='app_update_delete'),
```

---

## 6. Dashboard View — `dashboards/views.py`

Import updated:
```python
from setup.models import currentacademicyr, academicyr, sclass, section, AppUpdate
```

Query added inside `home_dashboard`:
```python
app_updates = AppUpdate.objects.filter(is_active=True).order_by('-date')[:6]
```

Context key added:
```python
'app_updates': app_updates,
```

---

## 7. Templates

### New templates created
| File | Purpose |
|------|---------|
| `templates/setup/app_update_list.html` | List all updates; Edit/Delete with confirm modal |
| `templates/setup/app_update_form.html` | Add/Edit form with live icon preview and styled badge selector |

### Modified templates

**`templates/dashboards/home_dashboard.html`**
- Added CSS for `.wn-item`, `.wn-icon`, `.wn-badge`, `.wn-title`, `.wn-desc`, `.wn-date`
- Added blinking animation `wn-star-blink` used by both What's New badges and Notice Board titles
- Added "What's New" card in the right column of the 2-col grid (below Notice Board)
- Notice board `h4` titles styled: gold background (`#d4af37`), white text, rounded, blinking

**`templates/panel/index.html`**
- Added sidebar link under the superadmin block (Settings section):
```html
<li class="menu-item">
  <a href="{% url 'app_update_list' %}" class="menu-link"><div>What's New</div></a>
</li>
```

---

## 8. Initial Data (seeded via shell)

Three entries created on 2026-09-19:

| Title | Badge | Icon |
|-------|-------|------|
| Google Login | New | `ri-google-fill` |
| Morning Report | New | `ri-sun-line` |
| Change Username & Password Reset | New | `ri-user-settings-line` |

To re-seed in production:
```bash
python manage.py shell -c "
from setup.models import AppUpdate
from datetime import date

updates = [
    {'title': 'Google Login', 'description': 'Sign in using your Google account — no password needed.', 'date': date(2026, 9, 19), 'badge': 'New', 'icon': 'ri-google-fill'},
    {'title': 'Morning Report', 'description': 'Daily morning summary report for principals — attendance, absentees, and highlights at a glance.', 'date': date(2026, 9, 19), 'badge': 'New', 'icon': 'ri-sun-line'},
    {'title': 'Change Username & Password Reset', 'description': 'Staff can now update their username and reset their password directly from the Profile page.', 'date': date(2026, 9, 19), 'badge': 'New', 'icon': 'ri-user-settings-line'},
]
for u in updates:
    AppUpdate.objects.get_or_create(title=u['title'], defaults=u)
    print('Created:', u['title'])
"
```

---

## 9. Production Deployment Checklist

- [ ] Pull latest code
- [ ] `python manage.py migrate` — applies `setup/0014_appupdate.py`
- [ ] Run the seed shell script above (skip if entries already exist)
- [ ] Restart the server (gunicorn/uwsgi)
- [ ] Verify at `/setup/whats-new/` (superadmin login required)
- [ ] Verify dashboard card visible at home dashboard

---

## Badge Color Reference

| Badge | Background | Text | Use for |
|-------|-----------|------|---------|
| New | `#d03b3b` (red, blinking) | `#fff` | Brand new features |
| Improved | `#e8f0fc` | `#2a78d6` | Enhancements to existing features |
| Fixed | `#fdf1de` | `#c98500` | Bug fixes |

## Icon Reference
Uses **Remix Icons** — browse at https://remixicon.com  
Example classes: `ri-star-line`, `ri-sun-line`, `ri-google-fill`, `ri-user-settings-line`, `ri-file-chart-line`
