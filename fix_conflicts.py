from backend.db import get_conn
from backend.scheduler import generate_exam_schedule

print("="*70)
print(" CORRECTION DES CONFLITS D'EXAMENS")
print("="*70)

# Supprimer les examens existants
print("\n Suppression des examens existants...")
conn = get_conn()
with conn.cursor() as cur:
    cur.execute("DELETE FROM examens")
    conn.commit()
conn.close()

print(" Anciens examens supprimés")
print("\n Génération d'un nouvel emploi du temps SANS CONFLITS...")
print("-"*70)

# Générer sans conflits
generate_exam_schedule()

print("\n" + "="*70)
print(" TERMINÉ! Vérifiez votre application Streamlit")
print("="*70)