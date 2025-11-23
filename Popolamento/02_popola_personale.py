import mysql.connector
from faker import Faker
import random
from datetime import date, timedelta

# ============================================================================
# CONFIGURAZIONE
# ============================================================================
DB_CONFIG = {
    'user': 'root',
    'password': 'andrea', 
    'host': 'localhost',
    'database': 'supermercato_db'
}

fake = Faker('it_IT')

# Definizioni Ruoli e Stipendi Base indicativi
RUOLI_DATA = {
    "Direttore Punto Vendita": 2800.00,
    "Responsabile Reparto": 1900.00,
    "Amministrativo": 1600.00,
    "Cassiere": 1300.00,
    "Scaffalista": 1250.00,
    "Magazziniere": 1350.00,
    "Addetto Pulizie": 1100.00,
    "Gastronomo": 1450.00
}

# Definizioni Titoli
TITOLI_LIST = [
    ("Licenza Media", "Ministero Istruzione", 0),
    ("Diploma Scuola Superiore", "Ministero Istruzione", 4),
    ("Laurea Triennale", "Università", 6),
    ("Laurea Magistrale", "Università", 7),
    ("HACCP Livello 1 (Base)", "Ente Certificatore Sanitario", 3),
    ("HACCP Livello 2 (Responsabile)", "Ente Certificatore Sanitario", 4),
    ("Patentino Muletto", "Ente Sicurezza Lavoro", 3),
    ("Certificazione Sicurezza Alto Rischio", "INAIL", 3)
]

# Mappa dei requisiti (Ruolo -> Lista di Titoli Obbligatori/Preferenziali)
# Usiamo stringhe per i nomi per facilità, poi convertiremo in ID
REQUISITI_RUOLO = {
    "Magazziniere": ["Patentino Muletto", "Certificazione Sicurezza Alto Rischio"],
    "Gastronomo": ["HACCP Livello 2 (Responsabile)"],
    "Responsabile Reparto": ["HACCP Livello 1 (Base)"],
    "Direttore Punto Vendita": ["Laurea Triennale"], # Preferenziale
    "Cassiere": ["HACCP Livello 1 (Base)"] # Spesso maneggiano alimenti confezionati
}

# ============================================================================
# FUNZIONI DI POPOLAMENTO
# ============================================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def popola_ruoli(cursor):
    print(" >> Inserimento Ruoli...")
    ruoli_map = {} # Nome -> ID
    sql = "INSERT INTO ruoli (nome_ruolo, descrizione, livello_autorizzazione) VALUES (%s, %s, %s)"
    
    for nome, stipendio_base in RUOLI_DATA.items():
        livello = 1
        desc = "Mansioni operative standard"
        
        if "Direttore" in nome:
            livello = 5
            desc = "Gestione completa del punto vendita"
        elif "Responsabile" in nome:
            livello = 3
            desc = "Coordinamento del reparto"
        elif "Amministrativo" in nome:
            livello = 2
            desc = "Gestione documentale e contabile"
            
        cursor.execute(sql, (nome, desc, livello))
        ruoli_map[nome] = cursor.lastrowid
        
    return ruoli_map

def popola_titoli(cursor):
    print(" >> Inserimento Titoli e Certificazioni...")
    titoli_map = {} # Nome -> ID
    sql = "INSERT INTO titoli (nome_titolo, ente_emittente, data_conseguimento, data_scadenza, eqf) VALUES (%s, %s, %s, %s, %s)"
    
    for nome, ente, eqf in TITOLI_LIST:
        # Per i titoli generici nel DB inseriamo date NULL o fittizie, 
        # ma nella tabella di collegamento dipendenti_titoli metteremo le date reali.
        # Qui stiamo definendo il "TIPO" di titolo.
        cursor.execute(sql, (nome, ente, None, None, eqf))
        titoli_map[nome] = cursor.lastrowid
        
    return titoli_map

def associa_requisiti_ruoli(cursor, ruoli_map, titoli_map):
    print(" >> Definizione requisiti Ruoli-Titoli...")
    sql = "INSERT INTO ruoli_titoli (id_ruolo, id_titolo) VALUES (%s, %s)"
    
    count = 0
    for ruolo_nome, titoli_req_list in REQUISITI_RUOLO.items():
        if ruolo_nome in ruoli_map:
            id_ruolo = ruoli_map[ruolo_nome]
            for titolo_nome in titoli_req_list:
                if titolo_nome in titoli_map:
                    id_titolo = titoli_map[titolo_nome]
                    cursor.execute(sql, (id_ruolo, id_titolo))
                    count += 1
    print(f"    -> Definiti {count} requisiti obbligatori.")

def get_uffici_ids(cursor):
    cursor.execute("SELECT id_ufficio FROM uffici")
    return [row[0] for row in cursor.fetchall()]

def popola_dipendenti(cursor, ruoli_map, titoli_map, uffici_ids, num_dipendenti=50):
    print(f" >> Assunzione di {num_dipendenti} dipendenti...")
    
    sql_dip = """
        INSERT INTO dipendenti 
        (nome, cognome, data_nascita, email, telefono, data_assunzione, stipendio, id_ruolo, id_ufficio) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    sql_tit_dip = "INSERT INTO dipendenti_titoli (id_dipendente, id_titolo) VALUES (%s, %s)"

    if not uffici_ids:
        raise Exception("Nessun ufficio trovato! Esegui prima lo script 01.")

    ruoli_keys = list(ruoli_map.keys())
    
    for _ in range(num_dipendenti):
        # 1. Dati Anagrafici
        sesso = random.choice(['M', 'F'])
        nome = fake.first_name_male() if sesso == 'M' else fake.first_name_female()
        cognome = fake.last_name()
        
        # Genera data di nascita (età 19-60)
        data_nascita = fake.date_of_birth(minimum_age=19, maximum_age=60)
        
        # Genera email unica
        email = f"{nome.lower()}.{cognome.lower()}{random.randint(1,999)}@supermercato.it"
        telefono = fake.phone_number()
        
        # 2. Ruolo e Ufficio
        nome_ruolo = random.choice(ruoli_keys)
        id_ruolo = ruoli_map[nome_ruolo]
        id_ufficio = random.choice(uffici_ids)
        
        # Stipendio con una variazione del 10% rispetto alla base
        base_stipendio = RUOLI_DATA[nome_ruolo]
        stipendio = round(base_stipendio * random.uniform(0.95, 1.10), 2)
        
        # Data assunzione: deve essere dopo la nascita + 18 anni
        data_min_assunzione = date(data_nascita.year + 18, data_nascita.month, data_nascita.day)
        data_assunzione = fake.date_between(start_date=data_min_assunzione, end_date='today')
        
        # ESECUZIONE INSERT DIPENDENTE
        cursor.execute(sql_dip, (nome, cognome, data_nascita, email, telefono, data_assunzione, stipendio, id_ruolo, id_ufficio))
        id_dipendente = cursor.lastrowid
        
        # 3. Assegnazione Titoli (Cruciale per vincoli e realismo)
        # A. Assegna i titoli obbligatori per il ruolo
        titoli_da_assegnare = set()
        
        if nome_ruolo in REQUISITI_RUOLO:
            for t_nome in REQUISITI_RUOLO[nome_ruolo]:
                titoli_da_assegnare.add(titoli_map[t_nome])
        
        # B. Assegna un titolo di studio base a tutti (Diploma o Licenza Media)
        titolo_base = random.choice(["Diploma Scuola Superiore", "Licenza Media"])
        titoli_da_assegnare.add(titoli_map[titolo_base])
        
        # C. Random chance per titoli extra
        if random.random() > 0.7:
             extra = random.choice(list(titoli_map.values()))
             titoli_da_assegnare.add(extra)
             
        # INSERT DIPENDENTI_TITOLI
        for id_tit in titoli_da_assegnare:
            # Ignora duplicati se il set non ha funzionato (safety)
            try:
                cursor.execute(sql_tit_dip, (id_dipendente, id_tit))
            except mysql.connector.Error:
                pass # Già presente

    print(f"    -> Assunti {num_dipendenti} dipendenti e assegnati i relativi titoli.")

# ============================================================================
# MAIN
# ============================================================================

def run():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Popola Ruoli
        map_ruoli = popola_ruoli(cursor)
        
        # 2. Popola Titoli
        map_titoli = popola_titoli(cursor)
        
        # 3. Collega Ruoli e Titoli (Requisiti)
        associa_requisiti_ruoli(cursor, map_ruoli, map_titoli)
        
        # 4. Recupera Uffici esistenti
        ids_uffici = get_uffici_ids(cursor)
        
        # 5. Crea Dipendenti e assegna titoli personali
        popola_dipendenti(cursor, map_ruoli, map_titoli, ids_uffici, num_dipendenti=60)

        conn.commit()
        print(" >> Commit eseguito correttamente.")
        
    except mysql.connector.Error as err:
        print(f"Errore MySQL: {err}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    run()