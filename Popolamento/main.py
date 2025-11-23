import subprocess
import sys
import os
import time

# Configurazione colori per output terminale
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def run_script(script_name, description):
    """
    Esegue uno script python come sottoprocesso.
    """
    print(f"{Colors.HEADER}[START] {description} ({script_name})...{Colors.ENDC}")
    start_time = time.time()
    
    # --- MODIFICA IMPORTANTE PER I PERCORSI ---
    # Ottiene la directory assoluta dove si trova QUESTO file (main.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Cerca prima in una sottocartella 'scripts'
    script_path = os.path.join(current_dir, "scripts", script_name)
    
    # Se non esiste, cerca nella stessa cartella di main.py
    if not os.path.exists(script_path):
         script_path = os.path.join(current_dir, script_name)
    
    # Verifica finale
    if not os.path.exists(script_path):
        print(f"{Colors.FAIL}[ERROR] Impossibile trovare il file: {script_path}{Colors.ENDC}")
        sys.exit(1)
    # ------------------------------------------

    try:
        # Esegue lo script e attende la fine. 
        result = subprocess.run([sys.executable, script_path], check=True, text=True, capture_output=True)
        
        elapsed = time.time() - start_time
        print(f"{Colors.OKGREEN}[SUCCESS] {script_name} completato in {elapsed:.2f} secondi.{Colors.ENDC}")
        
        # (Opzionale) Se vuoi vedere l'output di ogni singolo script, togli il commento qui sotto:
        # print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}[ERROR] Errore durante l'esecuzione di {script_name}.{Colors.ENDC}")
        print(f"{Colors.WARNING}Dettagli errore:\n{e.stderr}{Colors.ENDC}")
        sys.exit(1) # Ferma tutto se uno script fallisce
    except Exception as e:
        print(f"{Colors.FAIL}[ERROR] Errore generico: {e}{Colors.ENDC}")
        sys.exit(1)

def main():
    print(f"{Colors.OKBLUE}=== INIZIO POPOLAMENTO DATABASE SUPERMERCATO ==={Colors.ENDC}\n")

    # Assicurati che tutti i file 01_..., 02_... siano nella cartella 'Popolamento' 
    # insieme a questo main.py (oppure in una sottocartella 'scripts' dentro Popolamento)

    # 0. PULIZIA PRELIMINARE (Così puoi lanciare lo script quante volte vuoi)
    run_script("00_reset_db.py", "Reset e Pulizia Tabelle")
    # 1. Infrastruttura (Dipendenze zero)
    run_script("01_popola_infrastruttura.py", "Popolamento Edifici, Reparti, Scaffali")

    # 2. Personale (Dipende da Uffici e Ruoli)
    run_script("02_popola_personale.py", "Popolamento Dipendenti e Ruoli")

    # 3. Prodotti (Catena logica lunga: Produttori -> Marche -> Categorie -> Prodotti)
    run_script("03_popola_prodotti.py", "Popolamento Catalogo Prodotti e Magazzino")

    # 4. Clienti (Indipendente, ma necessario per le vendite)
    run_script("04_popola_clienti.py", "Popolamento Anagrafica Clienti")

    # 5. Fornitori (Dipende da Prodotti per il catalogo fornitori)
    run_script("05_popola_fornitori.py", "Popolamento Fornitori e Ordini di acquisto")

    # 6. Vendite (Dipende da TUTTO: Prodotti, Clienti, Casse, Dipendenti)
    run_script("06_popola_vendite.py", "Simulazione Vendite (Scontrini e Dettagli)")

    print(f"\n{Colors.OKGREEN}=== TUTTI GLI SCRIPT COMPLETATI CON SUCCESSO ==={Colors.ENDC}")

if __name__ == "__main__":
    main()