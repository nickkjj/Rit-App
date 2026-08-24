from django.db import migrations

def popular_funcionarios(apps, schema_editor):
    Employee = apps.get_model('table_administration_service', 'Employee')
    LeaderLead = apps.get_model('table_administration_service', 'LeaderLead')

    # Seed data
    alice = Employee.objects.create(name='Alice Hartman', email='alice.hartman@company.com', position_name='CEO')
    bob = Employee.objects.create(name='Bob Sinclair', email='bob.sinclair@company.com', position_name='CTO')
    carol = Employee.objects.create(name='Carol Nguyen', email='carol.nguyen@company.com', position_name='CFO')
    david = Employee.objects.create(name='David Okafor', email='david.okafor@company.com', position_name='Engineering Manager')
    eva = Employee.objects.create(name='Eva Müller', email='eva.muller@company.com', position_name='Engineering Manager')
    frank = Employee.objects.create(name='Frank Rossi', email='frank.rossi@company.com', position_name='Product Manager')
    grace = Employee.objects.create(name='Grace Kim', email='grace.kim@company.com', position_name='UX Designer')
    henry = Employee.objects.create(name='Henry Patel', email='henry.patel@company.com', position_name='Senior Software Engineer')
    isabelle = Employee.objects.create(name='Isabelle Dubois', email='isabelle.dubois@company.com', position_name='Senior Software Engineer')
    james = Employee.objects.create(name='James Watanabe', email='james.watanabe@company.com', position_name='Software Engineer')
    karen = Employee.objects.create(name='Karen Oliveira', email='karen.oliveira@company.com', position_name='Software Engineer')
    liam = Employee.objects.create(name='Liam Johansson', email='liam.johansson@company.com', position_name='Software Engineer')
    mia = Employee.objects.create(name='Mia Fernandez', email='mia.fernandez@company.com', position_name='Data Engineer')
    noah = Employee.objects.create(name='Noah Chukwu', email='noah.chukwu@company.com', position_name='Data Analyst')
    olivia = Employee.objects.create(name='Olivia Brooks', email='olivia.brooks@company.com', position_name='QA Engineer')
    paul = Employee.objects.create(name='Paul Nakamura', email='paul.nakamura@company.com', position_name='QA Engineer')
    quinn = Employee.objects.create(name='Quinn Santos', email='quinn.santos@company.com', position_name='DevOps Engineer')
    rachel = Employee.objects.create(name='Rachel Ivanova', email='rachel.ivanova@company.com', position_name='Finance Analyst')
    samuel = Employee.objects.create(name='Samuel Osei', email='samuel.osei@company.com', position_name='Finance Analyst')
    tina = Employee.objects.create(name='Tina Bergmann', email='tina.bergmann@company.com', position_name='HR Specialist')
    nicolas = Employee.objects.create(name='Nicolas', email='macielniiicolas@gmail.com', position_name='Software Analyst')
    
    # Alice (CEO) leads
    LeaderLead.objects.create(leader=alice, lead=bob)
    LeaderLead.objects.create(leader=alice, lead=carol)
    LeaderLead.objects.create(leader=alice, lead=frank)
    LeaderLead.objects.create(leader=alice, lead=tina)

    # Bob (CTO) leads
    LeaderLead.objects.create(leader=bob, lead=david)
    LeaderLead.objects.create(leader=bob, lead=eva)
    LeaderLead.objects.create(leader=bob, lead=grace)
    LeaderLead.objects.create(leader=bob, lead=quinn)
    LeaderLead.objects.create(leader=bob, lead=paul)
    LeaderLead.objects.create(leader=bob, lead=nicolas)

    # David leads
    LeaderLead.objects.create(leader=david, lead=henry)
    LeaderLead.objects.create(leader=david, lead=liam)

    # Henry leads
    LeaderLead.objects.create(leader=henry, lead=james)
    LeaderLead.objects.create(leader=henry, lead=karen)

    # Eva leads
    LeaderLead.objects.create(leader=eva, lead=isabelle)
    LeaderLead.objects.create(leader=eva, lead=mia)
    LeaderLead.objects.create(leader=eva, lead=noah)

    # Carol leads
    LeaderLead.objects.create(leader=carol, lead=rachel)
    LeaderLead.objects.create(leader=carol, lead=samuel)

    # Frank leads
    LeaderLead.objects.create(leader=frank, lead=olivia)

class Migration(migrations.Migration):

    dependencies = [
        ('table_administration_service', '0002_employee_is_authenticated'),
    ]

    operations = [
        migrations.RunPython(popular_funcionarios),
    ]



"""
-- ============================================================
--  employees_dump.sql
--  Creates the employee table and a self-referencing
--  leader_lead relationship, then seeds 20 employees.
-- ============================================================

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS leader_lead;
DROP TABLE IF EXISTS employee;

-- ------------------------------------------------------------
--  Table: employee
-- ------------------------------------------------------------
CREATE TABLE employee (
    id            SERIAL          PRIMARY KEY,
    name          VARCHAR(100)    NOT NULL,
    email         VARCHAR(150)    NOT NULL UNIQUE,
    position_name VARCHAR(100)    NOT NULL
);

-- ------------------------------------------------------------
--  Table: leader_lead
--  Models a many-to-many "leader → subordinate" relationship.
--  leader_id : the employee who leads
--  lead_id   : the employee being led
-- ------------------------------------------------------------
CREATE TABLE leader_lead (
    leader_id  INT NOT NULL,
    lead_id    INT NOT NULL,
    PRIMARY KEY (leader_id, lead_id),
    CONSTRAINT fk_leader
        FOREIGN KEY (leader_id) REFERENCES employee(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_lead
        FOREIGN KEY (lead_id)   REFERENCES employee(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    -- An employee cannot lead themselves
    CONSTRAINT chk_no_self_lead CHECK (leader_id <> lead_id)
);

-- ------------------------------------------------------------
--  Seed data – 20 employees
-- ------------------------------------------------------------
INSERT INTO employee (id, name, email, position_name) VALUES
( 1, 'Alice Hartman',    'alice.hartman@company.com',    'CEO'),
( 2, 'Bob Sinclair',     'bob.sinclair@company.com',     'CTO'),
( 3, 'Carol Nguyen',     'carol.nguyen@company.com',     'CFO'),
( 4, 'David Okafor',     'david.okafor@company.com',     'Engineering Manager'),
( 5, 'Eva Müller',       'eva.muller@company.com',       'Engineering Manager'),
( 6, 'Frank Rossi',      'frank.rossi@company.com',      'Product Manager'),
( 7, 'Grace Kim',        'grace.kim@company.com',        'UX Designer'),
( 8, 'Henry Patel',      'henry.patel@company.com',      'Senior Software Engineer'),
( 9, 'Isabelle Dubois',  'isabelle.dubois@company.com',  'Senior Software Engineer'),
(10, 'James Watanabe',   'james.watanabe@company.com',   'Software Engineer'),
(11, 'Karen Oliveira',   'karen.oliveira@company.com',   'Software Engineer'),
(12, 'Liam Johansson',   'liam.johansson@company.com',   'Software Engineer'),
(13, 'Mia Fernandez',    'mia.fernandez@company.com',    'Data Engineer'),
(14, 'Noah Chukwu',      'noah.chukwu@company.com',      'Data Analyst'),
(15, 'Olivia Brooks',    'olivia.brooks@company.com',    'QA Engineer'),
(16, 'Paul Nakamura',    'paul.nakamura@company.com',    'QA Engineer'),
(17, 'Quinn Santos',     'quinn.santos@company.com',     'DevOps Engineer'),
(18, 'Rachel Ivanova',   'rachel.ivanova@company.com',   'Finance Analyst'),
(19, 'Samuel Osei',      'samuel.osei@company.com',      'Finance Analyst'),
(20, 'Tina Bergmann',    'tina.bergmann@company.com',    'HR Specialist'),
(21, 'Nicolas',          'macielniiicolas@gmail.com',    'Software Analyst');

-- Reset sequence so future INSERTs auto-increment correctly
SELECT setval('employee_id_seq', 21);

-- ------------------------------------------------------------
--  Seed data – leader / lead relationships
--
--  Org hierarchy overview:
--  Alice (CEO)
--    ├─ Bob (CTO)
--    │    ├─ David (Eng Manager)
--    │    │    ├─ Henry  (Sr Engineer)
--    │    │    │    ├─ James  (Engineer)
--    │    │    │    └─ Karen  (Engineer)
--    │    │    └─ Liam   (Engineer)
--    │    ├─ Eva   (Eng Manager)
--    │    │    ├─ Isabelle (Sr Engineer)
--    │    │    ├─ Noah   (Data Analyst)
--    │    │    └─ Mia    (Data Engineer)
--    │    ├─ Grace  (UX Designer)
--    │    ├─ Quinn  (DevOps)
--    │    └─ Paul   (QA)
--    ├─ Carol (CFO)
--    │    ├─ Rachel (Finance Analyst)
--    │    └─ Samuel (Finance Analyst)
--    ├─ Frank (Product Manager)
--    │    └─ Olivia (QA Engineer)
--    └─ Tina  (HR Specialist)
-- ------------------------------------------------------------
INSERT INTO leader_lead (leader_id, lead_id) VALUES
-- Alice leads top-level reports
(1,  2),   -- Alice → Bob
(1,  3),   -- Alice → Carol
(1,  6),   -- Alice → Frank
(1, 20),   -- Alice → Tina

-- Bob leads his direct reports
(2,  4),   -- Bob → David
(2,  5),   -- Bob → Eva
(2,  7),   -- Bob → Grace
(2, 17),   -- Bob → Quinn
(2, 16),   -- Bob → Paul

-- David leads his engineers
(4,  8),   -- David → Henry
(4, 12),   -- David → Liam

-- Henry leads junior engineers
(8, 10),   -- Henry → James
(8, 11),   -- Henry → Karen

-- Eva leads her engineers
(5,  9),   -- Eva → Isabelle
(5, 13),   -- Eva → Mia
(5, 14),   -- Eva → Noah

-- Carol leads finance team
(3, 18),   -- Carol → Rachel
(3, 19),   -- Carol → Samuel

-- Frank leads QA
(6, 15);   -- Frank → Olivia
"""