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

# ============================================================================
# FUNZIONI
# ============================================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def popola_fornitori(cursor, n=20):
    print(f" >> Creazione di {n} Fornitori...")
    sql = """
        INSERT INTO fornitori (nome_fornitore, partita_iva, email, telefono, affidabilita)
        VALUES (%s, %s, %s, %s, %s)
    """
    ids = []
    piva_set = set()

    for _ in range(n):
        nome = f"{fake.company()} {random.choice(['Srl', 'SpA', 'Logistica', 'Distribuzione'])}"
        
        # Genera P.IVA univoca
        piva = fake.vat_id()
        while piva in piva_set:
            piva = fake.vat_id()
        piva_set.add(piva)
        
        email = f"ordini@{nome.split()[0].lower().replace('.','')}.com"
        telefono = fake.phone_number()
        affidabilita = random.randint(6, 10) # Scala 1-10

        cursor.execute(sql, (nome, piva, email, telefono, affidabilita))
        ids.append(cursor.lastrowid)
        
    return ids

def crea_catalogo_fornitori(cursor, id_fornitori):
    print(" >> Creazione Catalogo Fornitori (Chi vende cosa)...")
    
    # 1. Recupera tutti i prodotti e i loro prezzi di vendita
    cursor.execute("SELECT id_prodotto, prezzo_vendita FROM prodotti")
    prodotti = cursor.fetchall()
    
    sql = """
        INSERT INTO catalogo_fornitori (id_fornitore, id_prodotto, prezzo_offerta, data_inizio, data_fine)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    count = 0
    for id_prod, prezzo_vendita in prodotti:
        # Ogni prodotto è venduto da 1 a 3 fornitori diversi
        fornitori_scelti = random.sample(id_fornitori, k=random.randint(1, 3))
        
        for id_forn in fornitori_scelti:
            # Il fornitore vende al 40-70% del prezzo al pubblico (margine supermercato)
            prezzo_acquisto = round(float(prezzo_vendita) * random.uniform(0.4, 0.7), 2)
            
            # Validità offerta annuale
            data_inizio = date(2023, 1, 1)
            data_fine = date(2025, 12, 31)
            
            cursor.execute(sql, (id_forn, id_prod, prezzo_acquisto, data_inizio, data_fine))
            count += 1
            
    print(f"    -> Definite {count} voci di listino fornitori.")

def genera_ordini_storici(cursor, id_fornitori):
    print(" >> Generazione storico Ordini Fornitori...")
    
    sql_ordine = """
        INSERT INTO ordini_fornitore (id_fornitore, data_ordine, data_prevista_consegna, stato)
        VALUES (%s, %s, %s, %s)
    """
    sql_dettaglio = """
        INSERT INTO dettagli_ordine (id_ordine, id_prodotto, quantita, prezzo_unitario)
        VALUES (%s, %s, %s, %s)
    """
    
    # Creiamo ordini spalmati negli ultimi 6 mesi
    for _ in range(50): # 50 ordini totali
        id_forn = random.choice(id_fornitori)
        
        # Data ordine nel passato
        data_ord = fake.date_between(start_date='-6m', end_date='today')
        data_cons = data_ord + timedelta(days=random.randint(2, 10))
        stato = 'Consegnato' if data_cons < date.today() else 'In attesa'
        
        cursor.execute(sql_ordine, (id_forn, data_ord, data_cons, stato))
        id_ordine = cursor.lastrowid
        
        # Recupera prodotti venduti da questo fornitore
        cursor.execute("SELECT id_prodotto, prezzo_offerta FROM catalogo_fornitori WHERE id_fornitore = %s", (id_forn,))
        prodotti_disponibili = cursor.fetchall()
        
        if prodotti_disponibili:
            # Ordina 5-15 prodotti diversi
            items = random.sample(prodotti_disponibili, k=min(len(prodotti_disponibili), random.randint(5, 15)))
            
            for id_prod, prezzo in items:
                qty = random.randint(10, 100) # Scatole intere
                cursor.execute(sql_dettaglio, (id_ordine, id_prod, qty, prezzo))

# ============================================================================
# MAIN
# ============================================================================

def run():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        ids_fornitori = popola_fornitori(cursor)
        crea_catalogo_fornitori(cursor, ids_fornitori)
        genera_ordini_storici(cursor, ids_fornitori)

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