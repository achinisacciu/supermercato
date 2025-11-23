import mysql.connector

# ============================================================================
# CONFIGURAZIONE
# ============================================================================
DB_CONFIG = {
    'user': 'root',
    'password': 'andrea', 
    'host': 'localhost',
    'database': 'supermercato_db'
}

def reset_database():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print(" >> AVVIO PULIZIA DATABASE (TRUNCATE)...")

        # 1. Disabilita controlli chiavi esterne per poter svuotare in qualsiasi ordine
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # 2. Elenco tabelle da svuotare (ordine non importante grazie al punto 1)
        tabelle = [
            "dettagli_scontrino", "documenti",
            "dettagli_ordine", "ordini_fornitore", "catalogo_fornitori", "fornitori",
            "giacenze", "lotti", "prodotti", "marche", "produttori", "sottocategorie", "categorie",
            "clienti_titoli", "clienti",
            "dipendenti_titoli", "ruoli_titoli", "dipendenti", "titoli", "ruoli",
            "casse", "scaffali", "reparto_edificio", "reparti", "uffici", "edifici",
            "promozioni_prodotti", "promozioni"
        ]

        for tabella in tabelle:
            try:
                cursor.execute(f"TRUNCATE TABLE {tabella};")
                print(f"    - Svuotata tabella: {tabella}")
            except mysql.connector.Error as err:
                # Se la tabella non esiste (magari non creata), ignora
                print(f"    ! Warning su {tabella}: {err}")

        # 3. Riabilita controlli chiavi esterne
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        conn.commit()
        print(" >> PULIZIA COMPLETATA CON SUCCESSO.\n")

    except mysql.connector.Error as err:
        print(f"Errore MySQL: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    reset_database()