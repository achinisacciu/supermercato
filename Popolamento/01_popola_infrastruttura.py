import mysql.connector
from faker import Faker
import random

# ============================================================================
# CONFIGURAZIONE
# ============================================================================
DB_CONFIG = {
    'user': 'root',
    'password': 'andrea',      # Inserisci la tua password qui
    'host': 'localhost',
    'database': 'supermercato_db'
}

fake = Faker('it_IT')

# Liste di riferimento per rendere i dati realistici
LISTA_REPARTI = [
    "Ortofrutta", "Macelleria", "Pescheria", "Panetteria & Pasticceria",
    "Latticini & Salumi", "Surgelati", "Alimentari Confezionati",
    "Bevande & Vini", "Igiene Casa & Persona", "Elettronica & Bazar", "Pet Food"
]

# ============================================================================
# FUNZIONI DI POPOLAMENTO
# ============================================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def popola_edifici(cursor):
    print(" >> Inserimento Edifici...")
    edifici_ids = {'Sede': [], 'Magazzino': [], 'Punto Vendita': []}
    
    # 1. Sede Centrale
    sql = "INSERT INTO edifici (nome_edificio, indirizzo, superficie_mq, funzione_principale) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, ("Headquarter Supermercato", fake.address(), 1500, "Sede"))
    edifici_ids['Sede'].append(cursor.lastrowid)

    # 2. Magazzino Centrale
    cursor.execute(sql, ("Hub Logistico Nord", fake.address(), 5000, "Magazzino"))
    edifici_ids['Magazzino'].append(cursor.lastrowid)

    # 3. Punti Vendita (ne creiamo 3)
    for i in range(1, 4):
        nome_pv = f"Supermercato {fake.city()}"
        mq = random.randint(800, 2500)
        cursor.execute(sql, (nome_pv, fake.address(), mq, "Punto Vendita"))
        edifici_ids['Punto Vendita'].append(cursor.lastrowid)
    
    return edifici_ids

def popola_uffici(cursor, edifici_ids):
    print(" >> Inserimento Uffici...")
    sql = "INSERT INTO uffici (nome_ufficio, piano, id_edificio) VALUES (%s, %s, %s)"
    
    # Uffici nella Sede
    for id_sede in edifici_ids['Sede']:
        uffici_sede = ["Amministrazione", "Risorse Umane", "Marketing", "IT & Sviluppo", "Direzione Generale"]
        for i, nome in enumerate(uffici_sede):
            cursor.execute(sql, (nome, i % 3 + 1, id_sede))

    # Uffici nel Magazzino
    for id_mag in edifici_ids['Magazzino']:
        cursor.execute(sql, ("Ufficio Logistica", 0, id_mag))
        cursor.execute(sql, ("Controllo Qualità", 0, id_mag))

    # Uffici nei Punti Vendita
    for id_pv in edifici_ids['Punto Vendita']:
        cursor.execute(sql, ("Direzione Negozio", 1, id_pv))
        cursor.execute(sql, ("Back-office Amministrativo", 0, id_pv))

def popola_reparti(cursor):
    print(" >> Inserimento Reparti...")
    reparti_map = {} # Dizionario nome -> id
    sql = "INSERT INTO reparti (nome_reparto, descrizione) VALUES (%s, %s)"
    
    for nome in LISTA_REPARTI:
        desc = f"Reparto dedicato alla vendita di {nome.lower()}"
        cursor.execute(sql, (nome, desc))
        reparti_map[nome] = cursor.lastrowid
        
    return reparti_map

def collega_reparti_edifici(cursor, edifici_ids, reparti_map):
    print(" >> Collegamento Reparti agli Edifici...")
    sql = "INSERT INTO reparto_edificio (id_reparto, id_edificio) VALUES (%s, %s)"
    
    # Colleghiamo TUTTI i reparti ai Magazzini e ai Punti Vendita
    target_edifici = edifici_ids['Magazzino'] + edifici_ids['Punto Vendita']
    
    count = 0
    for id_ed in target_edifici:
        for id_rep in reparti_map.values():
            cursor.execute(sql, (id_rep, id_ed))
            count += 1
    print(f"    -> Create {count} associazioni Reparto-Edificio.")

def popola_scaffali(cursor, reparti_map):
    print(" >> Inserimento Scaffali...")
    sql = "INSERT INTO scaffali (tipo, capacita_peso, capacita_volume, id_reparto) VALUES (%s, %s, %s, %s)"
    
    count = 0
    for nome_rep, id_rep in reparti_map.items():
        # Determina il tipo di scaffale in base al reparto
        tipo = 'Normale'
        if 'Surgelati' in nome_rep:
            tipo = 'Congelatore'
        elif 'Latticini' in nome_rep or 'Macelleria' in nome_rep or 'Pescheria' in nome_rep:
            tipo = 'Frigorifero'
            
        # Crea N scaffali per ogni reparto
        num_scaffali = random.randint(5, 15) 
        for _ in range(num_scaffali):
            # Capacità casuali ma realistiche
            peso = random.choice([100.00, 250.00, 500.00])
            volume = random.choice([500.00, 1000.00, 2000.00]) # Litri
            
            cursor.execute(sql, (tipo, peso, volume, id_rep))
            count += 1
            
    print(f"    -> Creati {count} scaffali totali.")

def popola_casse(cursor, edifici_ids):
    print(" >> Inserimento Casse...")
    sql = "INSERT INTO casse (numero_cassa, tipo, stato, id_edificio) VALUES (%s, %s, %s, %s)"
    
    count = 0
    for id_pv in edifici_ids['Punto Vendita']:
        # Ogni supermercato ha tra 5 e 10 casse
        num_casse = random.randint(5, 10)
        for n in range(1, num_casse + 1):
            # Le prime 2 casse sono spesso automatiche, le altre manuali
            tipo = 'Automatica' if n <= 2 else 'Manuale'
            stato = random.choices(['Attiva', 'In manutenzione', 'Disattivata'], weights=[90, 5, 5])[0]
            
            cursor.execute(sql, (n, tipo, stato, id_pv))
            count += 1
            
    print(f"    -> Installate {count} casse nei punti vendita.")

# ============================================================================
# MAIN
# ============================================================================

def run():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Disabilita FK checks per evitare problemi se si riesegue su DB sporco (opzionale ma utile)
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        
        # 1. Edifici
        ids_edifici = popola_edifici(cursor)
        
        # 2. Uffici
        popola_uffici(cursor, ids_edifici)
        
        # 3. Reparti
        ids_reparti = popola_reparti(cursor)
        
        # 4. Reparto_Edificio
        collega_reparti_edifici(cursor, ids_edifici, ids_reparti)
        
        # 5. Scaffali
        popola_scaffali(cursor, ids_reparti)
        
        # 6. Casse
        popola_casse(cursor, ids_edifici)

        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()
        print(" >> Commit eseguito correttamente.")
        
    except mysql.connector.Error as err:
        print(f"Errore MySQL: {err}")
        if conn:
            conn.rollback()
        raise # Rilancia l'errore per farlo catturare al main.py padre
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    run()