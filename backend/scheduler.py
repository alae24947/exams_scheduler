from backend.db import get_conn
from datetime import date, timedelta, time
from collections import defaultdict

CRENEAUX = [
    time(9, 0),
    time(11, 0),
    time(14, 0),
    time(16, 0)
]

def generate_exam_schedule():
    """
    Génère un emploi du temps d'examens SANS CONFLITS
    RÈGLE CRITIQUE: 1 seul examen par jour par étudiant
    """
    
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # Effacer les examens existants
            cur.execute("DELETE FROM examens")
            conn.commit()
            
            print("🗑️ Examens existants supprimés")
            
            # Récupération des données
            cur.execute("SELECT id, dept_id FROM professeurs")
            profs = cur.fetchall()
            
            cur.execute("SELECT id, nom, capacite FROM salles ORDER BY capacite DESC")
            salles = cur.fetchall()
            
            # Structures de tracking GLOBALES
            prof_daily_count = defaultdict(int)  # (prof_id, date) -> nombre d'examens
            prof_time_slots = set()              # (prof_id, date, heure)
            salle_time_slots = set()             # (salle_id, date, heure)
            student_exam_dates = defaultdict(set)  # etudiant_id -> {dates où il a examen}
            
            start_date = date.today()
            
            # Récupérer tous les modules à planifier
            cur.execute("""
                SELECT m.id, m.nom, m.formation_id
                FROM modules m
                ORDER BY m.formation_id, m.id
            """)
            modules = cur.fetchall()
            
            print(f"\n Planification de {len(modules)} modules...")
            print("="*70)
            
            scheduled_count = 0
            failed_count = 0
            
            for module_id, module_nom, formation_id in modules:
                
                # Récupérer TOUS les étudiants de cette formation
                cur.execute("""
                    SELECT id
                    FROM etudiants
                    WHERE formation_id = %s
                """, (formation_id,))
                
                student_ids = [row[0] for row in cur.fetchall()]
                
                if not student_ids:
                    print(f"  {module_nom}: Aucun étudiant inscrit")
                    failed_count += 1
                    continue
                
                nb_etudiants = len(student_ids)
                
                # Chercher un créneau disponible
                scheduled = False
                current_date = start_date
                max_attempts = 100  # Limite pour éviter boucle infinie
                
                for attempt in range(max_attempts):
                    
                    #  VÉRIFICATION CRITIQUE #1: Est-ce qu'un étudiant a déjà un examen ce jour?
                    has_conflict = False
                    for student_id in student_ids:
                        if current_date in student_exam_dates[student_id]:
                            has_conflict = True
                            break
                    
                    if has_conflict:
                        # Passer au jour suivant
                        current_date += timedelta(days=1)
                        continue
                    
                    # Essayer chaque créneau horaire de cette journée
                    for exam_time in CRENEAUX:
                        
                        #  Trouver un professeur disponible
                        prof_id = None
                        for p_id, p_dept in profs:
                            # Vérifier: moins de 3 examens ce jour ET créneau libre
                            if (prof_daily_count[(p_id, current_date)] < 3 and
                                (p_id, current_date, exam_time) not in prof_time_slots):
                                prof_id = p_id
                                break
                        
                        if not prof_id:
                            continue  # Passer au créneau suivant
                        
                        #  Trouver une salle avec capacité suffisante
                        salle_id = None
                        for s_id, s_nom, s_cap in salles:
                            if (s_cap >= nb_etudiants and
                                (s_id, current_date, exam_time) not in salle_time_slots):
                                salle_id = s_id
                                salle_nom = s_nom
                                break
                        
                        if not salle_id:
                            continue  # Passer au créneau suivant
                        
                        # TOUT EST BON - INSÉRER L'EXAMEN
                        cur.execute("""
                            INSERT INTO examens 
                            (module_id, prof_id, salle_id, date_exam, heure, duree)
                            VALUES (%s, %s, %s, %s, %s, 120)
                        """, (module_id, prof_id, salle_id, current_date, exam_time))
                        
                        # Mettre à jour le tracking
                        prof_daily_count[(prof_id, current_date)] += 1
                        prof_time_slots.add((prof_id, current_date, exam_time))
                        salle_time_slots.add((salle_id, current_date, exam_time))
                        
                        #  MARQUER TOUS LES ÉTUDIANTS COMME OCCUPÉS CE JOUR
                        for student_id in student_ids:
                            student_exam_dates[student_id].add(current_date)
                        
                        print(f" {module_nom[:30]:30} | {current_date} {exam_time} | {salle_nom:15} | {nb_etudiants:3} étudiants")
                        
                        scheduled = True
                        scheduled_count += 1
                        break  # Sortir de la boucle des créneaux
                    
                    if scheduled:
                        break  # Sortir de la boucle des jours
                    
                    # Passer au jour suivant
                    current_date += timedelta(days=1)
                
                if not scheduled:
                    print(f"{module_nom}: ÉCHEC après {max_attempts} tentatives")
                    failed_count += 1
            
            # Commit final
            conn.commit()
            
            print("="*70)
            print(f"\n Génération terminée:")
            print(f"   - Examens planifiés: {scheduled_count}")
            print(f"   - Échecs: {failed_count}")
            print(f"   - Total modules: {len(modules)}")
            
            # Vérification finale
            verify_no_conflicts(cur)
            
    except Exception as e:
        print(f"\n ERREUR: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()


def verify_no_conflicts(cur):
    """Vérifie qu'il n'y a aucun conflit étudiant"""
    
    print("\n Vérification des conflits...")
    
    # Vérifier les conflits étudiants
    cur.execute("""
        SELECT 
            e.id,
            e.nom,
            e.prenom,
            ex.date_exam,
            COUNT(*) as nb_examens
        FROM etudiants e
        JOIN modules m ON e.formation_id = m.formation_id
        JOIN examens ex ON ex.module_id = m.id
        GROUP BY e.id, e.nom, e.prenom, ex.date_exam
        HAVING COUNT(*) > 1
        ORDER BY nb_examens DESC, ex.date_exam
    """)
    
    conflicts = cur.fetchall()
    
    if conflicts:
        print(f"\  {len(conflicts)} CONFLITS DÉTECTÉS:")
        for conflict in conflicts[:10]:  # Afficher max 10
            print(f"   - {conflict[1]} {conflict[2]}: {conflict[4]} examens le {conflict[3]}")
        return False
    else:
        print(" Aucun conflit détecté!")
        return True


def detect_conflicts():
    """
    Détecte les conflits dans l'emploi du temps actuel
    Retourne un rapport détaillé
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            conflicts = []
            
            # 1. Conflits étudiants (plusieurs examens le même jour)
            cur.execute("""
                SELECT 
                    e.id as etudiant_id,
                    e.nom,
                    e.prenom,
                    ex.date_exam,
                    COUNT(*) as nb_examens,
                    ARRAY_AGG(m.nom) as modules
                FROM etudiants e
                JOIN modules m ON e.formation_id = m.formation_id
                JOIN examens ex ON ex.module_id = m.id
                GROUP BY e.id, e.nom, e.prenom, ex.date_exam
                HAVING COUNT(*) > 1
                ORDER BY ex.date_exam, e.nom
            """)
            
            student_conflicts = cur.fetchall()
            
            if student_conflicts:
                conflicts.append({
                    'type': 'ÉTUDIANTS - Plusieurs examens le même jour',
                    'count': len(student_conflicts),
                    'details': student_conflicts
                })
            
            # 2. Conflits professeurs (plus de 3 examens/jour)
            cur.execute("""
                SELECT 
                    p.id,
                    p.nom,
                    p.prenom,
                    ex.date_exam,
                    COUNT(*) as nb_examens
                FROM professeurs p
                JOIN examens ex ON ex.prof_id = p.id
                GROUP BY p.id, p.nom, p.prenom, ex.date_exam
                HAVING COUNT(*) > 3
                ORDER BY ex.date_exam
            """)
            
            prof_conflicts = cur.fetchall()
            
            if prof_conflicts:
                conflicts.append({
                    'type': 'PROFESSEURS - Plus de 3 examens/jour',
                    'count': len(prof_conflicts),
                    'details': prof_conflicts
                })
            
            return conflicts
            
    finally:
        conn.close()


def print_conflict_report():
    """Affiche un rapport de conflits formaté"""
    conflicts = detect_conflicts()
    
    if not conflicts:
        print(" Aucun conflit détecté!")
        return
    
    print("\n" + "="*60)
    print("  RAPPORT DE CONFLITS")
    print("="*60)
    
    for conflict in conflicts:
        print(f"\n {conflict['type']}")
        print(f"   Nombre: {conflict['count']}")
        print("-" * 60)
        
        for detail in conflict['details'][:5]:  # Afficher max 5 exemples
            print(f"   {detail}")
        
        if len(conflict['details']) > 5:
            print(f"   ... et {len(conflict['details']) - 5} autres")
    
    print("\n" + "="*60)