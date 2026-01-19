CREATE TABLE departements (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) UNIQUE
);

CREATE TABLE formations (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    dept_id INT REFERENCES departements(id)
);

CREATE TABLE etudiants (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    formation_id INT REFERENCES formations(id),
    promo INT
);

CREATE TABLE professeurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    dept_id INT REFERENCES departements(id)
);

CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    formation_id INT REFERENCES formations(id)
);

CREATE TABLE salles (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50),
    capacite INT
);

CREATE TABLE examens (
    id SERIAL PRIMARY KEY,
    module_id INT REFERENCES modules(id),
    prof_id INT REFERENCES professeurs(id),
    salle_id INT REFERENCES salles(id),
    date_exam DATE,
    heure TIME,
    duree INT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(100),
    role VARCHAR(20)
);
