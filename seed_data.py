import os
import django

# 1. Initialisation de Django (Darouri tji l'fouq ga3)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

# 2. Les Imports des modèles (Mora setup)
from home_auth.models import CustomUser
from department.models import Department
from student.models import Student, Parent
from subject.models import Subject
from teacher.models import Teacher

print("=== DEBUT DE L'INITIALISATION DES DONNEES ===")

# ── COMPTES DE TEST (AUTH) ────────────────────────────────────
users = [
    {'username': 'admin1@gmail.com', 'email': 'admin@school.ma', 'password': 'doha12az', 'is_admin': True},
    {'username': 'teacher@preskool.ma', 'email': 'teacher@school.ma', 'password': 'doha12az', 'is_teacher': True},
    {'username': 'student1@gmail.com', 'email': 'student@school.ma', 'password': 'doha12az', 'is_student': True},
]

for u in users:
    if not CustomUser.objects.filter(username=u['username']).exists():
        CustomUser.objects.create_user(
            username=u['username'],
            email=u['email'],
            password=u['password'],
            is_admin=u.get('is_admin', False),
            is_teacher=u.get('is_teacher', False),
            is_student=u.get('is_student', False)
        )
        print(f"  [NEW] Utilisateur crée: {u['username']}")
    else:
        print(f"  [OK]  Utilisateur: {u['username']} (existe déjà)")

# ── DEPARTEMENTS ──────────────────────────────────────────────
depts = [
    {'department_id': 'INFO', 'department_name': 'Informatique',  'head_of_department': 'Dr. Ahmed Bennani', 'start_date': '2020-09-01', 'no_of_students': 45},
    {'department_id': 'MATH', 'department_name': 'Mathematiques', 'head_of_department': 'Dr. Fatima Zahra',  'start_date': '2019-09-01', 'no_of_students': 38},
    {'department_id': 'PHY',  'department_name': 'Physique',      'head_of_department': 'Dr. Karim Idrissi', 'start_date': '2021-09-01', 'no_of_students': 30},
    {'department_id': 'LANG', 'department_name': 'Langues',       'head_of_department': 'Prof. Sara Alaoui', 'start_date': '2018-09-01', 'no_of_students': 52},
    {'department_id': 'ECON', 'department_name': 'Economie',      'head_of_department': 'Dr. Youssef Tazi',  'start_date': '2020-01-15', 'no_of_students': 41},
]
for d in depts:
    obj, created = Department.objects.get_or_create(department_id=d['department_id'], defaults=d)
    print(f"  {'[NEW]' if created else '[OK] '} Departement: {obj.department_name}")

# ── ETUDIANTS ─────────────────────────────────────────────────
students_data = [
    ('Ayoub',  'Benali',   '2024001', 'Male',   '2003-04-12', 'IDAI', '2024-09-01', '0661234501', 'ADM001', 'A', 'Omar Benali',    'Ingenieur',    '0661000001', 'omar@email.com',   'Amina Benali',    'Prof',        '0661000002', 'amina@email.com',   '12 Rue Fes',       '12 Rue Fes'),
    ('Sana',   'El Fassi', '2024002', 'Female', '2003-07-22', 'IDAI', '2024-09-01', '0661234502', 'ADM002', 'B', 'Hassan El Fassi','Medecin',      '0661000003', 'hassan@email.com', 'Zineb El Fassi',  'Infirmiere',  '0661000004', 'zineb@email.com',   '5 Av Casablanca',  '5 Av Casablanca'),
    ('Mehdi',  'Chraibi',  '2024003', 'Male',   '2002-11-05', 'IDAG', '2024-09-01', '0661234503', 'ADM003', 'A', 'Rachid Chraibi','Comercant',    '0661000005', 'rachid@email.com', 'Houda Chraibi',   'Enseignante', '0661000006', 'houda@email.com',   '8 Rue Rabat',      '8 Rue Rabat'),
    ('Imane',  'Ziani',    '2024004', 'Female', '2003-02-14', 'IDAI', '2024-09-01', '0661234504', 'ADM004', 'C', 'Said Ziani',    'Fonctionnaire','0661000007', 'said@email.com',   'Naima Ziani',     'Menagere',    '0661000008', 'naima@email.com',   '3 Bd Marrakech',   '3 Bd Marrakech'),
]
for s in students_data:
    if not Student.objects.filter(student_id=s[2]).exists():
        p = Parent.objects.create(
            father_name=s[10], father_occupation=s[11], father_mobile=s[12], father_email=s[13],
            mother_name=s[14], mother_occupation=s[15], mother_mobile=s[16], mother_email=s[17],
            present_address=s[18], permanent_address=s[19]
        )
        Student.objects.create(
            first_name=s[0], last_name=s[1], student_id=s[2], gender=s[3],
            date_of_birth=s[4], student_class=s[5], joining_date=s[6],
            mobile_number=s[7], admission_number=s[8], section=s[9], parent=p
        )
        print(f"  [NEW] Etudiant: {s[0]} {s[1]}")
    else:
        print(f"  [OK]  Etudiant: {s[0]} {s[1]} (existe deja)")

# ── MATIERES ──────────────────────────────────────────────────
subjects_list = [
    ('ALGO101', 'Algorithmique', 'INFO', 4, 'Bases de l’algo'),
    ('WEB201',  'Developpement Web', 'INFO', 3, 'HTML CSS JS'),
    ('CALC101', 'Calcul Differentiel', 'MATH', 4, 'Analyse'),
]
for code, name, dept_id, cr, desc in subjects_list:
    dept = Department.objects.get(department_id=dept_id)
    obj, created = Subject.objects.get_or_create(subject_code=code, defaults={
        'subject_name': name, 'department': dept, 'credits': cr, 'description': desc
    })
    print(f"  {'[NEW]' if created else '[OK] '} Matiere: {obj.subject_name}")

# ── TEACHERS ──────────────────────────────────────────────────
teachers_data = [
    ('TCH001', 'Karim', 'Idrissi', 'Male', '1978-03-15', '0661100001', '2015-09-01', '10 ans', 'Casablanca', 'INFO'),
    ('TCH002', 'Fatima', 'Zahra', 'Female', '1982-07-22', '0661100002', '2017-09-01', '8 ans', 'Rabat', 'MATH'),
]
for t in teachers_data:
    dept = Department.objects.get(department_id=t[9])
    obj, created = Teacher.objects.get_or_create(teacher_id=t[0], defaults={
        'first_name': t[1], 'last_name': t[2], 'gender': t[3],
        'date_of_birth': t[4], 'mobile_number': t[5], 'joining_date': t[6],
        'experience': t[7], 'address': t[8], 'department': dept
    })
    print(f"  {'[NEW]' if created else '[OK] '} Teacher: {obj.first_name} {obj.last_name}")

print("\n=== INITIALISATION TERMINEE AVEC SUCCES ! ===")