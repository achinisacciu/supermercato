# 🛒 Supermercato León - Database Project

> **Progetto Didattico di Database Relazionale**  
> *Simulazione completa di un sistema informativo per una catena di supermercati.*

## 📘 Panoramica
Questo repository ospita il progetto **Supermercato León**, un caso di studio didattico ideato per l'applicazione pratica di tecniche di progettazione di basi di dati (concettuale, logica e fisica) su piattaforma **MySQL**.

Il progetto simula una realtà aziendale complessa ("Supermercato S.r.l."), permettendo di esplorare:
- Modellazione ER avanzata.
- Scrittura di query SQL complesse, Viste, Stored Procedures e Trigger.
- Analisi dei dati e Business Intelligence.

> ℹ️ **Per il contesto completo**: Leggi il documento [**Scheda del Progetto (Brief)**](supermercato_brief.md) per dettagli su obiettivi formativi, contesto aziendale e infrastruttura.

---

## 📂 Struttura del Repository

Il progetto è organizzato nelle seguenti cartelle principali:

| Cartella | Descrizione |
|----------|-------------|
| **`/sql`** | Contiene gli script SQL DDL per la creazione del database. <br> - `tables.sql`: Definizione delle tabelle. <br> - `view.sql` / `analisys_view.sql`: Viste per l'applicazione e l'analisi. <br> - `triggers.sql`: Logica di business automatizzata. |
| **`/Popolamento`** | Script Python per la generazione di dati sintetici realistici. Utilizza librerie come `Faker` per popolare il DB con migliaia di record (clienti, prodotti, vendite). |
| **`/supermercato-db-docs`** | Documentazione tecnica dettagliata: <br> - **ERD.dbml**: Diagramma Entità-Relazione. <br> - **Dizionario Dati**, **Regole di Vincolo**, **Modello Logico**. |

---

## 🚀 Guida Rapida (Getting Started)

### Prerequisiti
- **MySQL Server** (8.0 o superiore)
- **Python 3.x**
- Librerie Python richieste:
  ```bash
  pip install mysql-connector-python faker
  ```

### Installazione e Setup

1.  **Creazione Schema**:
    Esegui gli script nella cartella `/sql` nel seguente ordine (tramite MySQL Workbench o CLI):
    1.  `tables.sql`
    2.  `view.sql`
    3.  `triggers.sql`
    4.  `analisys_view.sql`

2.  **Popolamento Dati**:
    Il database viene popolato tramite script Python che generano dati coerenti.
    - Configura le credenziali del database. 
        *Nota: Di default usa user='root', password='andrea'*.
    - Esegui lo script principale:
      ```bash
      cd Popolamento
      python main.py
      ```
    Questo script orchestrerà l'esecuzione di tutti i moduli di popolamento (infrastruttura, personale, prodotti, clienti, vendite).

---

## 📊 Funzionalità Chiave
- **Gestione Inventario**: Tracciamento lotti, scadenze e giacenze.
- **Fidelizzazione Clienti**: Sistema carte fedeltà e analisi abitudini di acquisto.
- **Analisi Vendite**: Viste dedicate per il monitoraggio di KPI e performance prodotti.

---

## 📝 Autore e Licenza
**Autore**: Andrea Palazzo  
**Licenza**: MIT (Vedi file `LICENSE`)

*Questo progetto è a puro scopo didattico. Ogni riferimento a persone o aziende reali è puramente casuale.*