import streamlit as st
from backend.auth import login
from backend.scheduler import generate_exam_schedule
from backend.db import get_conn
from backend.analytics import *

# Page config
st.set_page_config(
    page_title="Faculté de Science - Gestion des Examens"
)

# Load custom CSS
with open("frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------
# Login logic
# -----------------------------
if "role" not in st.session_state:
    # Header
    st.markdown("""
        <div class="login-header">
            <h1>Faculté de Science</h1>
            <p>Plateforme de Gestion des Examens</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Login container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h2 class="login-title">Connexion</h2>', unsafe_allow_html=True)
        
        username = st.text_input("Nom d'utilisateur", key="username")
        password = st.text_input("Mot de passe", type="password", key="password")
        
        if st.button("Se connecter", use_container_width=True):
            role = login(username, password)
            if role:
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Identifiants incorrects")

# -----------------------------
# Main app after login
# -----------------------------
else:
    # Top navigation bar
    st.markdown(f"""
        <div class="top-navbar">
            <div class="navbar-title">
                <h1>Faculté de Science - Gestion des Examens</h1>
            </div>
            <div class="navbar-role">
                <span>Rôle: <strong>{st.session_state.role.upper()}</strong></span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-header">Menu</div>', unsafe_allow_html=True)
        
        # Admin actions
        if st.session_state.role == "admin":
            st.markdown("**Actions Administrateur**")
            if st.button("Générer emplois du temps", use_container_width=True):
                with st.spinner("Génération en cours..."):
                    generate_exam_schedule()
                st.success("EDT généré avec succès")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation
        st.markdown("**Navigation**")
        page = st.radio("", ["Planning", "Statistiques", "Conflits"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Logout
        if st.button("Déconnexion", use_container_width=True):
            del st.session_state.role
            st.rerun()
    
    # Main content area
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Page: Planning
    if page == "Planning":
        st.markdown('<h2 class="section-title">Planning des Examens</h2>', unsafe_allow_html=True)
        
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        m.nom AS Module, 
                        e.date_exam AS Date, 
                        e.heure AS Heure, 
                        s.nom AS Salle
                    FROM examens e
                    JOIN modules m ON e.module_id = m.id
                    JOIN salles s ON e.salle_id = s.id
                    ORDER BY e.date_exam, e.heure
                """)
                data = cur.fetchall()
        finally:
            conn.close()
        
        if data:
            st.dataframe(data, use_container_width=True, hide_index=True)
        else:
            st.info("Aucun examen planifié pour le moment")
    
    # Page: Statistiques
    elif page == "Statistiques":
        st.markdown('<h2 class="section-title">Statistiques Globales</h2>', unsafe_allow_html=True)
        
        # KPIs in columns
        kpis = global_kpis()
        if not kpis.empty:
            cols = st.columns(len(kpis.columns))
            for idx, col_name in enumerate(kpis.columns):
                with cols[idx]:
                    st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-value">{kpis[col_name].iloc[0]}</div>
                            <div class="kpi-label">{col_name}</div>
                        </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Utilisation des salles
        st.markdown('<h3 class="subsection-title">Utilisation des Salles</h3>', unsafe_allow_html=True)
        salle_data = salle_utilisation()
        if not salle_data.empty:
            st.dataframe(salle_data, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        
        # Charge des professeurs
        st.markdown('<h3 class="subsection-title">Charge des Professeurs</h3>', unsafe_allow_html=True)
        df_prof = charge_professeurs()
        if not df_prof.empty:
            st.bar_chart(df_prof.set_index("professeur"))
        else:
            st.info("Aucune donnée disponible")

    
    # Page: Conflits
    elif page == "Conflits":
        st.markdown('<h2 class="section-title">Détection des Conflits</h2>', unsafe_allow_html=True)
        
        # Conflits Professeurs
        st.markdown('<h3 class="subsection-title">Conflits Professeurs</h3>', unsafe_allow_html=True)
        prof_conflicts = conflits_professeurs()
        if not prof_conflicts.empty:
            st.dataframe(prof_conflicts, use_container_width=True, hide_index=True)
        else:
            st.success("Aucun conflit détecté")
        
        st.markdown("---")
        
        # Conflits Étudiants
        st.markdown('<h3 class="subsection-title">Conflits Étudiants</h3>', unsafe_allow_html=True)
        student_conflicts = conflits_etudiants()
        if not student_conflicts.empty:
            st.dataframe(student_conflicts, use_container_width=True, hide_index=True)
        else:
            st.success("Aucun conflit détecté")
    
    st.markdown('</div>', unsafe_allow_html=True)