import mysql.connector
from faker import Faker
import random

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

# Lista di professioni per rendere i dati vari
LAVORI = [
    "Impiegato", "Libero Professionista", "Insegnante", "Pensionato", 
    "Studente", "Operaio", "Medico", "Avvocato", "Casalinga", 
    "Disoccupato", "Imprenditore", "Programmatore", "Commesso"
]

# ============================================================================
# FUNZIONI
# ============================================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def generate_unique_email(nome, cognome, existing_emails):
    """
    Genera un'email unica tentando diverse combinazioni.
    """
    base = f"{nome.lower()}.{cognome.lower()}"
    # Pulisce caratteri speciali (es. spazi o accenti se presenti)
    base = base.replace(" ", "").replace("'", "")
    
    domains = ["gmail.com", "yahoo.it", "hotmail.com", "libero.it", "outlook.com"]
    
    # Tentativo 1: nome.cognome@domain
    email = f"{base}@{random.choice(domains)}"
    if email not in existing_emails:
        return email
        
    # Tentativo 2: nome.cognome123@domain
    email = f"{base}{random.randint(1, 9999)}@{random.choice(domains)}"
    if email not in existing_emails:
        return email
        
    # Tentativo 3: nome.cognome.anno@domain
    email = f"{base}.{random.randint(1950, 2005)}@{random.choice(domains)}"
    return email

def popola_clienti(cursor, n=1000):
    print(f" >> Generazione di {n} profili clienti...")
    
    sql = """
        INSERT INTO clienti 
        (nome, cognome, data_nascita, sesso, lavoro, email, telefono, residenza, newsletter)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    clienti_data = []
    existing_emails = set() # Per garantire unicità lato Python prima dell'insert
    
    for _ in range(n):
        # 1. Genere e Nome coerente
        sesso = random.choices(['M', 'F', 'Altro'], weights=[48, 48, 4])[0]
        if sesso == 'M':
            nome = fake.first_name_male()
        elif sesso == 'F':
            nome = fake.first_name_female()
        else:
            nome = fake.first_name() # Neutro/Casuale
            
        cognome = fake.last_name()
        
        # 2. Dati Anagrafici
        # Età tra 18 e 90 anni
        data_nascita = fake.date_of_birth(minimum_age=18, maximum_age=90)
        
        lavoro = random.choice(LAVORI)
        residenza = fake.address().replace('\n', ', ')
        
        # 3. Contatti unici
        email = generate_unique_email(nome, cognome, existing_emails)
        existing_emails.add(email)
        
        telefono = fake.phone_number()
        
        # 4. Marketing
        newsletter = random.choice([0, 1])
        
        clienti_data.append((
            nome, cognome, data_nascita, sesso, lavoro, 
            email, telefono, residenza, newsletter
        ))
        
    # Esecuzione Batch (Molto più veloce di insert singoli)
    try:
        # Usa INSERT IGNORE per saltare eventuali (rari) duplicati di telefono generati da Faker
        # Nota: La sintassi INSERT IGNORE è specifica di MySQL
        sql_ignore = sql.replace("INSERT INTO", "INSERT IGNORE INTO")
        
        cursor.executemany(sql_ignore, clienti_data)
        print(f"    -> Inseriti {cursor.rowcount} nuovi clienti.")
        
    except mysql.connector.Error as err:
        print(f"Errore durante l'inserimento batch: {err}")
        raise

# ============================================================================
# MAIN
# ============================================================================

def run():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Generiamo un numero sufficiente di clienti per rendere interessante il Machine Learning
        popola_clienti(cursor, n=1000)

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