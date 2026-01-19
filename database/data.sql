INSERT INTO departements (nom) VALUES
('Informatique'), ('Mathématiques'), ('Biologie'),
('Anglais'), ('Français'), ('Chimie'), ('Physique');

-- 20 formations
INSERT INTO formations (nom, dept_id) VALUES
('Licence Informatique', 1),
('Master Intelligence Artificielle', 1),
('Licence Mathématiques', 2),
('Master Math Appliquées', 2),
('Licence Biologie', 3),
('Master Biotechnologie', 3),
('Licence Anglais', 4),
('Master Linguistique Anglaise', 4),
('Licence Français', 5),
('Master Littérature Française', 5),
('Licence Chimie', 6),
('Master Chimie Organique', 6),
('Licence Physique', 7),
('Master Physique Appliquée', 7),
('MIAGE', 1),
('Réseaux & Télécom', 1),
('Analyse Mathématique', 2),
('Biochimie', 3),
('Didactique Anglais', 4),
('Didactique Français', 5);

-- Professeurs
INSERT INTO professeurs (nom, prenom, dept_id) VALUES
('Benaissa','Karim',1),
('Khelifi','Alae',1),
('Saidi','Mohamed',2),
('Benali','Amel',3),
('Haddad','Nadia',4),
('Cherif','Samir',5),
('Boualem','Yacine',6),
('Zerrouki','Rania',7);

-- Salles
INSERT INTO salles (nom, capacite) VALUES
('Amphi A', 300),
('Amphi B', 250),
('Salle 101', 20),
('Salle 102', 20),
('Salle 201', 20);

-- Utilisateurs
INSERT INTO users (username,password,role) VALUES
('admin','admin123','admin'),
('doyen','doyen123','doyen'),
('chef_info','chef123','chef');
