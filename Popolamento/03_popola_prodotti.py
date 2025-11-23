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

# STRUTTURA CATALOGO (Categoria -> [Sottocategorie])
CATALOGO_STRUTTURA = {
    "Ortofrutta": ["Frutta Fresca", "Verdura Fresca", "Frutta Secca"],
    "Macelleria": ["Carne Rossa", "Carne Bianca", "Preparati Carne"],
    "Pescheria": ["Pesce Fresco", "Crostacei"],
    "Latticini & Salumi": ["Latte & Panna", "Formaggi", "Salumi Affettati", "Yogurt"],
    "Surgelati": ["Verdure Surgelate", "Pizze Surgelate", "Gelati", "Pesce Surgelato"],
    "Dispensa": ["Pasta & Riso", "Conserve", "Biscotti & Dolci", "Caffè & Tè", "Olio & Aceto"],
    "Bevande": ["Acqua", "Bibite Gassate", "Birra", "Vino"],
    "Igiene Casa": ["Detersivi", "Carta Casa", "Accessori Pulizia"],
    "Cura Persona": ["Saponi & Bagnoschiuma", "Shampoo", "Igiene Orale"]
}

# ESEMPI PRODOTTI PER SOTTOCATEGORIA (Per generare nomi realistici)
PRODOTTI_MAP = {
    "Frutta Fresca": ["Mele Golden", "Banane", "Arance Tarocco", "Fragole", "Uva Italia"],
    "Verdura Fresca": ["Insalata Iceberg", "Pomodori Pachino", "Zucchine", "Carote", "Patate"],
    "Latte & Panna": ["Latte Intero 1L", "Latte Parz. Scremato", "Panna da Cucina"],
    "Formaggi": ["Mozzarella", "Parmigiano Reggiano DOP", "Gorgonzola", "Ricotta"],
    "Pasta & Riso": ["Spaghetti n.5", "Penne Rigate", "Riso Carnaroli", "Fusilli"],
    "Biscotti & Dolci": ["Frollini al Cacao", "Biscotti Integrali", "Merendine Cioccolato"],
    "Detersivi": ["Detersivo Piatti Limone", "Detersivo Lavatrice Liquido", "Ammorbidente"],
    "Vino": ["Chianti DOCG", "Prosecco", "Pinot Grigio", "Lambrusco"],
    "Gelati": ["Vaschetta Gelato Vaniglia", "Coni Gelato (4pz)", "Ghiaccioli Assortiti"]
}

# MAPPING CONSERVAZIONE (Sottocategoria -> Tipo Scaffale Richiesto)
TIPO_CONSERVAZIONE = {
    "Surgelati": "Congelatore",
    "Gelati": "Congelatore",
    "Pesce Surgelato": "Congelatore",
    "Pizze Surgelate": "Congelatore",
    "Verdure Surgelate": "Congelatore",
    
    "Latticini & Salumi": "Frigorifero",
    "Latte & Panna": "Frigorifero",
    "Formaggi": "Frigorifero",
    "Yogurt": "Frigorifero",
    "Salumi Affettati": "Frigorifero",
    "Macelleria": "Frigorifero",
    "Carne Rossa": "Frigorifero",
    "Carne Bianca": "Frigorifero",
    "Pesce Fresco": "Frigorifero",
    
    # Default: Normale
}

# ============================================================================
# FUNZIONI
# ============================================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def popola_categorie_sottocategorie(cursor):
    print(" >> Creazione Albero Categorie...")
    sottocategorie_ids = {} # Nome Sottocategoria -> ID
    
    sql_cat = "INSERT INTO categorie (nome_categoria, descrizione) VALUES (%s, %s)"
    sql_sub = "INSERT INTO sottocategorie (nome_sottocategoria, id_categoria) VALUES (%s, %s)"
    
    for cat_nome, sub_list in CATALOGO_STRUTTURA.items():
        cursor.execute(sql_cat, (cat_nome, f"Prodotti reparto {cat_nome}"))
        id_cat = cursor.lastrowid
        
        for sub_nome in sub_list:
            cursor.execute(sql_sub, (sub_nome, id_cat))
            sottocategorie_ids[sub_nome] = cursor.lastrowid
            
    return sottocategorie_ids

def popola_produttori_marche(cursor, n_produttori=20):
    print(f" >> Creazione {n_produttori} Produttori e Marche...")
    marche_ids = []
    
    sql_prod = "INSERT INTO produttori (nome_produttore, nazione, sito_web, telefono) VALUES (%s, %s, %s, %s)"
    sql_marca = "INSERT INTO marche (nome_marca, id_produttore) VALUES (%s, %s)"
    
    for _ in range(n_produttori):
        # Crea Produttore
        nome_prod = fake.company()
        cursor.execute(sql_prod, (nome_prod, "Italia", fake.url(), fake.phone_number()))
        id_prod = cursor.lastrowid
        
        # Crea 1-3 marche per questo produttore
        num_marche = random.randint(1, 3)
        for _ in range(num_marche):
            # Genera nome marca (es. "Nature", "Bio", "Delizia") + suffisso casuale
            suffix = fake.word().capitalize()
            nome_marca = f"{suffix} {random.choice(['Foods', 'Italia', 'Bio', 'Gusto', 'Casa'])}"
            
            cursor.execute(sql_marca, (nome_marca, id_prod))
            marche_ids.append(cursor.lastrowid)
            
    return marche_ids

def determina_tipo_scaffale(nome_sottocategoria):
    # Cerca corrispondenze nel dizionario TIPO_CONSERVAZIONE
    for key, value in TIPO_CONSERVAZIONE.items():
        if key in nome_sottocategoria:
            return value
    return "Normale"

def popola_prodotti(cursor, sottocategorie_ids, marche_ids):
    print(" >> Creazione Catalogo Prodotti...")
    prodotti_info = [] # Lista di dizionari per passare info ai lotti
    
    sql_prod = """
        INSERT INTO prodotti 
        (nome_prodotto, prezzo_vendita, peso_kg, volume_cm3, id_marca, id_sottocategoria, scadenza, is_alimentare)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for sub_nome, id_sub in sottocategorie_ids.items():
        # Determina se è alimentare (semplificazione: Igiene e Cura Persona NO, resto SI)
        is_alimentare = 0 if sub_nome in CATALOGO_STRUTTURA["Igiene Casa"] or sub_nome in CATALOGO_STRUTTURA["Cura Persona"] else 1
        
        # Genera prodotti specifici o generici
        lista_prodotti = PRODOTTI_MAP.get(sub_nome, [f"Prodotto {sub_nome} Generico"])
        
        # Per ogni "tipo" di prodotto in lista, ne creiamo un paio di varianti
        for base_name in lista_prodotti:
            num_varianti = random.randint(1, 3)
            for _ in range(num_varianti):
                id_marca = random.choice(marche_ids)
                
                # Attributi fisici
                peso = round(random.uniform(0.1, 2.0), 3)
                volume = int(peso * 1000 * random.uniform(0.8, 1.5)) # stima volume in cm3
                prezzo = round(random.uniform(0.99, 15.99), 2)
                
                # Nome completo
                nome_prodotto = f"{base_name} {fake.word().upper()}"
                
                # Data scadenza (campo descrittivo sul prodotto, non vincolante come il lotto)
                scadenza_indicativa = None
                if is_alimentare:
                    scadenza_indicativa = fake.date_between(start_date='+1m', end_date='+2y')
                
                cursor.execute(sql_prod, (nome_prodotto, prezzo, peso, volume, id_marca, id_sub, scadenza_indicativa, is_alimentare))
                id_prodotto = cursor.lastrowid
                
                # Salva info per step successivo (Lotti)
                tipo_scaffale = determina_tipo_scaffale(sub_nome)
                prodotti_info.append({
                    'id': id_prodotto,
                    'is_alimentare': is_alimentare,
                    'tipo_scaffale_richiesto': tipo_scaffale,
                    'peso': peso,
                    'volume': volume
                })
                
    print(f"    -> Inseriti {len(prodotti_info)} prodotti a catalogo.")
    return prodotti_info

def get_scaffali_disponibili(cursor):
    # Ritorna dizionario: 'Frigorifero': [id1, id2...], 'Normale': [...]
    scaffali = {'Normale': [], 'Frigorifero': [], 'Congelatore': []}
    cursor.execute("SELECT id_scaffale, tipo FROM scaffali")
    for row in cursor.fetchall():
        scaffali[row[1]].append(row[0])
    return scaffali

def popola_lotti_giacenze(cursor, prodotti_info, scaffali_map):
    print(" >> Generazione Lotti e Stoccaggio su Scaffali...")
    
    sql_lotto = """
        INSERT INTO lotti (codice_lotto, id_prodotto, data_produzione, data_scadenza)
        VALUES (%s, %s, %s, %s)
    """
    sql_giacenza = """
        INSERT INTO giacenze (id_lotto, id_scaffale, quantita)
        VALUES (%s, %s, %s)
    """
    
    count_lotti = 0
    
    for p in prodotti_info:
        # Creiamo 1 o 2 lotti per prodotto
        num_lotti = random.randint(1, 2)
        
        for _ in range(num_lotti):
            # 1. Dati Lotto
            codice = fake.ean13() # Usa EAN come codice lotto per semplicità
            data_prod = fake.date_between(start_date='-6m', end_date='today')
            
            data_scad = None
            if p['is_alimentare']:
                # Scadenza: Breve per freschi, lunga per secchi
                giorni_scadenza = 30 if p['tipo_scaffale_richiesto'] == 'Frigorifero' else 365
                data_scad = data_prod + timedelta(days=random.randint(10, giorni_scadenza))
                # Assicuriamoci che non sia già scaduto per il caricamento iniziale (o magari qualcuno sì per testare viste scaduti)
                if random.random() > 0.95: 
                    # 5% probabilità prodotto già scaduto (per testare viste)
                    data_scad = date.today() - timedelta(days=random.randint(1, 10))
                else:
                    # Normalmente scade in futuro
                    data_scad = date.today() + timedelta(days=random.randint(5, giorni_scadenza))
            
            try:
                cursor.execute(sql_lotto, (codice, p['id'], data_prod, data_scad))
                id_lotto = cursor.lastrowid
                count_lotti += 1
                
                # 2. Collocazione su Scaffale (Giacenza)
                tipo_req = p['tipo_scaffale_richiesto']
                possibili_scaffali = scaffali_map.get(tipo_req, [])
                
                if possibili_scaffali:
                    id_scaffale = random.choice(possibili_scaffali)
                    # Quantità limitata per non far scattare trigger capacità scaffale subito
                    qty = random.randint(5, 50)
                    
                    cursor.execute(sql_giacenza, (id_lotto, id_scaffale, qty))
                
            except mysql.connector.Error as err:
                # Ignora errori duplicati su codice lotto o trigger scaffale pieno
                # print(f"Warning: {err}") 
                pass

    print(f"    -> Creati {count_lotti} lotti e relative giacenze.")

# ============================================================================
# MAIN
# ============================================================================

def run():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Categorie e Sottocategorie
        map_sottocat = popola_categorie_sottocategorie(cursor)
        
        # 2. Produttori e Marche
        ids_marche = popola_produttori_marche(cursor)
        
        # 3. Prodotti
        list_prodotti = popola_prodotti(cursor, map_sottocat, ids_marche)
        
        # 4. Recupera Scaffali per tipo
        map_scaffali = get_scaffali_disponibili(cursor)
        
        # 5. Lotti e Giacenze
        popola_lotti_giacenze(cursor, list_prodotti, map_scaffali)

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