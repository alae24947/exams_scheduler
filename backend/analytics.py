import pandas as pd
from backend.db import get_conn

def global_kpis():
    conn = get_conn()
    try:
        query = """
        SELECT
            (SELECT COUNT(*) FROM etudiants) AS "Total Étudiants",
            (SELECT COUNT(*) FROM examens) AS "Total Examens",
            (SELECT COUNT(*) FROM professeurs) AS "Total Professeurs",
            (SELECT COUNT(*) FROM salles) AS "Total Salles"
        """
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()
        
def salle_utilisation():
    conn = get_conn()
    try:
        query = """
        SELECT
            s.nom AS salle,
            COUNT(e.id) AS nombre_examens,
            s.capacite
        FROM salles s
        LEFT JOIN examens e ON s.id = e.salle_id
        GROUP BY s.id, s.nom, s.capacite
        ORDER BY nombre_examens DESC
        """
        return pd.read_sql(query, conn)
    finally:
        conn.close()
        
def charge_professeurs():
    """
    Number of surveillances per professor
    """
    conn = get_conn()
    query = """
    SELECT
        CONCAT(p.nom, ' ', p.prenom) AS professeur,
        d.nom AS departement,
        COUNT(e.id) AS nb_surveillance
    FROM professeurs p
    JOIN departements d ON p.dept_id = d.id
    LEFT JOIN examens e ON e.prof_id = p.id
    GROUP BY professeur, departement
    ORDER BY nb_surveillance DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def conflits_etudiants():
    """
    Retourne les étudiants ayant plusieurs examens le même jour
    Colonnes: nom, prenom, date_exam, nb_examens
    """
    conn = get_conn()
    try:
        query = """
            SELECT 
                e.nom,
                e.prenom,
                ex.date_exam,
                COUNT(*) as nb_examens
            FROM etudiants e
            JOIN modules m ON e.formation_id = m.formation_id
            JOIN examens ex ON ex.module_id = m.id
            GROUP BY e.id, e.nom, e.prenom, ex.date_exam
            HAVING COUNT(*) > 1
            ORDER BY ex.date_exam, nb_examens DESC, e.nom
        """
        
        df = pd.read_sql(query, conn)
        return df
        
    finally:
        conn.close()


def conflits_professeurs():
    """
    Retourne les professeurs ayant plus de 3 examens le même jour
    """
    conn = get_conn()
    try:
        query = """
            SELECT 
                p.nom,
                p.prenom,
                ex.date_exam,
                COUNT(*) as nb_examens
            FROM professeurs p
            JOIN examens ex ON ex.prof_id = p.id
            GROUP BY p.id, p.nom, p.prenom, ex.date_exam
            HAVING COUNT(*) > 3
            ORDER BY ex.date_exam, nb_examens DESC
        """
        
        df = pd.read_sql(query, conn)
        return df
        
    finally:
        conn.close()