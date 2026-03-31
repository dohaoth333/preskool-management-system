path = r'c:\Users\Elhad\preskool-management-system\templates\Home\base.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    '                     <li>\n'
    '                        <a href="holiday.html"><i class="fas fa-holly-berry"></i> <span>Holiday</span></a>\n'
    '                     </li>'
)

new = (
    '                     <li class="submenu">\n'
    '                        <a href="#"><i class="fas fa-holly-berry"></i> <span>Jours F\u00e9ri\u00e9s</span> <span class="menu-arrow"></span></a>\n'
    '                        <ul>\n'
    "                           <li><a href=\"{% url 'holiday_list' %}\">Liste des Jours F\u00e9ri\u00e9s</a></li>\n"
    '                           {% if user.is_admin or user.is_superuser %}\n'
    "                           <li><a href=\"{% url 'add_holiday' %}\">Ajouter un Jour F\u00e9ri\u00e9</a></li>\n"
    '                           {% endif %}\n'
    '                        </ul>\n'
    '                     </li>'
)

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS: sidebar updated.')
else:
    print('ERROR: target not found.')
