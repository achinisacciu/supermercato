import mysql.connector
import random
from datetime import date, timedelta, time

# ============================================================================
# CONFIGURAZIONE
# ============================================================================
DB_CONFIG = {
    'user': 'root',
    'password': 'andrea', 
    'host': 'localhost',
    'database': 'supermercato_db'
}

# Quanti scontrini generare? (Più alto è, meglio è per il ML, ma ci mette più tempo)
NUM_SCONTRINI = 4000 

# ============================================================================
# FUNZIONI DI SUPPORTO
# ============================================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_ids(cursor, table, col_id):
    cursor.execute(f"SELECT {col_id} FROM {table}")
    return [row[0] for row in cursor.fetchall()]

def get_prodotti_info(cursor):
    # Ritorna lista di tuple (id, prezzo)
    cursor.execute("SELECT id_prodotto, prezzo_vendita FROM prodotti")
    return cursor.fetchall()

def get_casse_info(cursor):
    # Ritorna lista di (id_cassa, id_edificio)
    cursor.execute("SELECT id_cassa, id_edificio FROM casse WHERE stato = 'Attiva'")
    return cursor.fetchall()

def get_dipendenti_cassa(cursor):
    # Ritorna ID dei dipendenti che sono Cassieri (o ruoli compatibili)
    cursor.execute("""
        SELECT d.id_dipendente 
        FROM dipendenti d 
        JOIN ruoli r ON d.id_ruolo = r.id_ruolo 
        WHERE r.nome_ruolo IN ('Cassiere', 'Direttore Punto Vendita', 'Responsabile Reparto')
    """)
    return [row[0] for row in cursor.fetchall()]

# ============================================================================
# GENERATORE VENDITE
# ============================================================================

def popola_vendite(cursor):
    print(f" >> Simulazione di {NUM_SCONTRINI} scontrini (può richiedere tempo)...")
    
    clienti_ids = get_ids(cursor, 'clienti', 'id_cliente')
    prodotti_list = get_prodotti_info(cursor) # [(id, prezzo), ...]
    casse_list = get_casse_info(cursor)       # [(id_cassa, id_edificio), ...]
    cassieri_ids = get_dipendenti_cassa(cursor)
    
    if not casse_list or not cassieri_ids or not prodotti_list:
        print(" !! Errore: Mancano dati base (Casse, Prodotti o Cassieri). Esegui script precedenti.")
        return

    sql_doc = """
        INSERT INTO documenti 
        (tipo_documento, data_documento, ora_documento, modalità_pagamento, importo, id_cassa, id_dipendente, id_cliente)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    sql_dettaglio = """
        INSERT INTO dettagli_scontrino 
        (id_documento, id_prodotto, quantita, prezzo_unitario, sconto_percentuale)
        VALUES (%s, %s, %s, %s, %s)
    """

    # Simuliamo vendite nell'ultimo anno
    start_date = date.today() - timedelta(days=365)
    
    for i in range(NUM_SCONTRINI):
        if i % 100 == 0:
            print(f"    ...Generati {i} scontrini")

        # 1. Genera Intestazione Scontrino
        # Data casuale pesata (più vendite recenti per realismo)
        days_offset = int(random.triangular(0, 365, 365)) # Tende verso oggi
        data_doc = start_date + timedelta(days=days_offset)
        
        # Ora (Picchi alle 12:00 e alle 18:00)
        hour = random.choices(
            range(8, 21), 
            weights=[1, 2, 4, 6, 8, 5, 4, 3, 5, 8, 9, 6, 2]
        )[0]
        ora_doc = time(hour, random.randint(0, 59), 0)
        
        # Dati operativi
        cassa = random.choice(casse_list)
        id_cassa = cassa[0]
        id_dipendente = random.choice(cassieri_ids)
        
        # Cliente: 70% identificato (Carta Fedeltà), 30% Anonimo
        id_cliente = random.choice(clienti_ids) if random.random() < 0.7 else None
        
        modalita = random.choice(['Contanti', 'Carta di Credito', 'Carta di Debito', 'Digital Wallet'])
        
        # Inserisci Documento con IMPORTO 0
        # Il Trigger 'update_totale_scontrino_insert' calcolerà il totale man mano che inseriamo righe
        cursor.execute(sql_doc, ('Scontrino', data_doc, ora_doc, modalita, 0, id_cassa, id_dipendente, id_cliente))
        id_documento = cursor.lastrowid
        
        # 2. Genera Dettagli (Prodotti nel carrello)
        # Quanti prodotti? 1-5 (spesa veloce) o 10-30 (spesa grossa)
        num_items = random.choices(
            [random.randint(1, 5), random.randint(6, 15), random.randint(16, 40)],
            weights=[40, 40, 20] # 40% piccola, 40% media, 20% carrello pieno
        )[0]
        
        items_scelti = random.choices(prodotti_list, k=num_items)
        
        dettagli_batch = []
        
        for prod in items_scelti:
            id_prod = prod[0]
            prezzo_base = float(prod[1])
            
            qty = random.randint(1, 3)
            if random.random() > 0.95: qty += 5 # Ogni tanto scorta grossa
            
            # Sconto simulato (Offerte volantino)
            sconto = 0.00
            rand_sconto = random.random()
            if rand_sconto > 0.8: sconto = 20.00
            elif rand_sconto > 0.95: sconto = 50.00
            
            # NOTA: Il prezzo unitario nello scontrino è quello "al momento della vendita".
            # Qui usiamo il prezzo attuale del DB, ma in un sistema reale potrebbe variare.
            dettagli_batch.append((id_documento, id_prod, qty, prezzo_base, sconto))
            
        # Esegui inserimento batch dettagli
        # I trigger scatteranno per ogni riga (su MySQL i trigger scattano anche con executemany)
        cursor.executemany(sql_dettaglio, dettagli_batch)

# ============================================================================
# MAIN
# ============================================================================

def run():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        popola_vendite(cursor)

        conn.commit()
        print(f" >> {NUM_SCONTRINI} Scontrini generati con successo.")
        
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