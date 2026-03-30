import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from department.models import Department
from student.models import Student, Parent
from subject.models import Subject

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
    ('Omar',   'Berrada',  '2024005', 'Male',   '2002-08-30', 'IDAG', '2024-09-01', '0661234505', 'ADM005', 'B', 'Ali Berrada',   'Architecte',   '0661000009', 'ali@email.com',    'Khadija Berrada', 'Avocate',     '0661000010', 'khadija@email.com', '22 Rue Agadir',    '22 Rue Agadir'),
    ('Hiba',   'Mansouri', '2024006', 'Female', '2003-05-18', 'IDAI', '2024-09-01', '0661234506', 'ADM006', 'A', 'Mourad Mansouri','Ingenieur',   '0661000011', 'mourad@email.com', 'Samira Mansouri', 'Dentiste',    '0661000012', 'samira@email.com',  '7 Av Tanger',      '7 Av Tanger'),
    ('Yassine','Lahrichi', '2024007', 'Male',   '2002-12-01', 'IDAG', '2024-09-01', '0661234507', 'ADM007', 'B', 'Nabil Lahrichi','Comptable',    '0661000013', 'nabil@email.com',  'Rajae Lahrichi',  'Pharmacienne','0661000014', 'rajae@email.com',   '15 Rue Meknes',    '15 Rue Meknes'),
    ('Salma',  'Oufkir',   '2024008', 'Female', '2003-09-09', 'IDAI', '2024-09-01', '0661234508', 'ADM008', 'C', 'Bilal Oufkir',  'Pilote',       '0661000015', 'bilal@email.com',  'Widad Oufkir',    'Avocate',     '0661000016', 'widad@email.com',   '9 Av Oujda',       '9 Av Oujda'),
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
info = Department.objects.get(department_id='INFO')
math = Department.objects.get(department_id='MATH')
phy  = Department.objects.get(department_id='PHY')
lang = Department.objects.get(department_id='LANG')
econ = Department.objects.get(department_id='ECON')

subjects = [
    ('ALGO101', 'Algorithmique et Programmation', info, 4, 'Bases de lalgorithmique et structures de donnees'),
    ('WEB201',  'Developpement Web',              info, 3, 'HTML CSS JavaScript Python Django'),
    ('DB301',   'Bases de Donnees',               info, 3, 'SQL NoSQL et conception de BDD'),
    ('NET101',  'Reseaux Informatiques',           info, 3, 'TCP IP routage et protocoles'),
    ('CALC101', 'Calcul Differentiel',             math, 4, 'Derivees integrales et series'),
    ('STAT201', 'Statistiques et Probabilites',   math, 3, 'Probabilites inferences et tests'),
    ('ALG201',  'Algebre Lineaire',               math, 3, 'Vecteurs matrices et determinants'),
    ('MECA101', 'Mecanique Classique',             phy,  4, 'Cinematique dynamique et energie'),
    ('ELEC201', 'Electronique',                    phy,  3, 'Circuits composants et signaux'),
    ('ANG101',  'Anglais Technique',               lang, 2, 'Redaction et communication professionnelle en anglais'),
    ('FRA101',  'Francais Professionnel',          lang, 2, 'Expression ecrite et orale en francais'),
    ('ECO101',  'Microeconomie',                   econ, 3, 'Offre demande et theorie des marches'),
    ('COMPTA',  'Comptabilite Generale',           econ, 3, 'Bilan compte de resultat et flux'),
]
for code, name, dept, cr, desc in subjects:
    obj, created = Subject.objects.get_or_create(subject_code=code, defaults={
        'subject_name': name, 'department': dept, 'credits': cr, 'description': desc
    })
    print(f"  {'[NEW]' if created else '[OK] '} Matiere: {obj.subject_name}")

# ── TEACHERS ──────────────────────────────────────────────────
from teacher.models import Teacher

teachers_data = [
    ('TCH001', 'Karim',   'Idrissi',  'Male',   '1978-03-15', '0661100001', '2015-09-01', '10 ans', '5 Rue Atlas, Casablanca',   'INFO'),
    ('TCH002', 'Fatima',  'Zahra',    'Female', '1982-07-22', '0661100002', '2017-09-01', '8 ans',  '12 Av Hassan II, Rabat',    'MATH'),
    ('TCH003', 'Yassine', 'Benali',   'Male',   '1980-11-10', '0661100003', '2016-09-01', '9 ans',  '8 Rue Fes, Meknes',         'PHY'),
    ('TCH004', 'Sara',    'Alaoui',   'Female', '1985-04-05', '0661100004', '2018-09-01', '7 ans',  '3 Av Mohammed V, Tanger',   'LANG'),
    ('TCH005', 'Omar',    'Tazi',     'Male',   '1975-09-30', '0661100005', '2012-09-01', '13 ans', '20 Rue Oued, Marrakech',    'ECON'),
    ('TCH006', 'Houda',   'Mansouri', 'Female', '1988-01-18', '0661100006', '2019-09-01', '6 ans',  '7 Bd Zerktouni, Agadir',    'INFO'),
    ('TCH007', 'Rachid',  'El Fassi', 'Male',   '1979-06-25', '0661100007', '2014-09-01', '11 ans', '15 Rue Moulay, Fes',        'MATH'),
    ('TCH008', 'Zineb',   'Chraibi',  'Female', '1983-12-03', '0661100008', '2016-09-01', '9 ans',  '2 Av Allal, Oujda',         'PHY'),
]
for t in teachers_data:
    dept = Department.objects.get(department_id=t[9])
    obj, created = Teacher.objects.get_or_create(teacher_id=t[0], defaults={
        'first_name': t[1], 'last_name': t[2], 'gender': t[3],
        'date_of_birth': t[4], 'mobile_number': t[5], 'joining_date': t[6],
        'experience': t[7], 'address': t[8], 'department': dept
    })
    print(f"  {'[NEW]' if created else '[OK] '} Teacher: {obj.first_name} {obj.last_name} ({dept.department_name})")

print("\n=== TOUT EST INSERE AVEC SUCCES ! ===")
