# Dizionario dei Dati – Database Supermercato

Questo documento fornisce una descrizione dettagliata di ogni tabella e attributo presente nel database del supermercato, basandosi sul modello logico relazionale.

---

## Gestione Personale

### Tabella: dipendenti
**Descrizione:** Memorizza i dati anagrafici e professionali di tutti i dipendenti del supermercato.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_dipendente | INT | Identificativo univoco del dipendente | PRIMARY KEY, AUTO_INCREMENT |
| nome | VARCHAR(100) | Nome del dipendente | NOT NULL |
| cognome | VARCHAR(100) | Cognome del dipendente | NOT NULL |
| data_nascita | DATE | Data di nascita del dipendente | NOT NULL |
| email | VARCHAR(150) | Indirizzo email del dipendente | UNIQUE |
| telefono | VARCHAR(20) | Numero di telefono del dipendente | - |
| data_assunzione | DATE | Data di assunzione del dipendente | NOT NULL |
| stipendio | DECIMAL(10,2) | Stipendio mensile del dipendente | - |
| id_ruolo | INT | Identificativo del ruolo assegnato | NOT NULL, FOREIGN KEY |
| id_ufficio | INT | Identificativo dell'ufficio di appartenenza | NOT NULL, FOREIGN KEY |

<br>

### Tabella: ruoli
**Descrizione:** Definisce i diversi ruoli professionali presenti in azienda.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_ruolo | INT | Identificativo univoco del ruolo | PRIMARY KEY, AUTO_INCREMENT |
| nome_ruolo | VARCHAR(100) | Nome del ruolo lavorativo | NOT NULL |
| descrizione | TEXT | Descrizione dettagliata del ruolo | - |


<br>

### Tabella: titoli
**Descrizione:** Elenca i titoli di studio o le certificazioni possedute dai dipendenti.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_titolo | INT | Identificativo univoco del titolo di studio | PRIMARY KEY, AUTO_INCREMENT |
| nome_titolo | VARCHAR(100) | Nome del titolo di studio o certificazione | NOT NULL |
| ente_emittente | VARCHAR(100) | Ente che ha rilasciato il titolo | - |
| data_conseguimento | DATE | Data di conseguimento del titolo | - |
| data_scadenza | DATE | Data di scadenza del titolo | - |
| eqf | INT | Livello EQF (European Qualifications Framework) | - |

<br>

### Tabella: uffici
**Descrizione:** Contiene informazioni sugli uffici presenti nei vari edifici del supermercato.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_ufficio | INT | Identificativo univoco dell'ufficio | PRIMARY KEY, AUTO_INCREMENT |
| nome_ufficio | VARCHAR(100) | Nome dell'ufficio | NOT NULL |
| piano | INT | Piano dell'edificio dove si trova l'ufficio | - |
| id_edificio | INT | Identificativo dell'edificio di appartenenza | NOT NULL, FOREIGN KEY |

<br>

### Tabella: dipendenti_titoli
**Descrizione:** Tabella di collegamento che associa i dipendenti ai titoli che possiedono (relazione N:M).

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_dipendente | INT | Identificativo del dipendente | PRIMARY KEY, FOREIGN KEY |
| id_titolo | INT | Identificativo del titolo posseduto | PRIMARY KEY, FOREIGN KEY |

<br>

### Tabella: ruoli_titoli
**Descrizione:** Tabella di collegamento che definisce quali titoli sono richiesti o preferenziali per un determinato ruolo (relazione N:M).

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_ruolo | INT | Identificativo del ruolo | PRIMARY KEY, FOREIGN KEY |
| id_titolo | INT | Identificativo del titolo richiesto | PRIMARY KEY, FOREIGN KEY |

---

## Infrastruttura e Localizzazione

### Tabella: edifici
**Descrizione:** Anagrafica degli edifici di proprietà o in uso al supermercato.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_edificio | INT | Identificativo univoco dell'edificio | PRIMARY KEY, AUTO_INCREMENT |
| nome_edificio | VARCHAR(100) | Nome dell'edificio | NOT NULL |
| indirizzo | VARCHAR(255) | Indirizzo dell'edificio | - |
| superficie_mq | INT | Superficie dell'edificio in metri quadrati | - |
| funzione_principale | ENUM('Punto Vendita', 'Magazzino', 'Sede') | Funzione principale dell'edificio | NOT NULL |

<br>

### Tabella: reparti
**Descrizione:** Definisce i vari reparti presenti all'interno dei punti vendita o dei magazzini.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_reparto | INT | Identificativo univoco del reparto | PRIMARY KEY, AUTO_INCREMENT |
| nome_reparto | VARCHAR(100) | Nome del reparto | NOT NULL |
| descrizione | TEXT | Descrizione del reparto | - |

<br>

### Tabella: scaffali
**Descrizione:** Anagrafica degli scaffali, con dettagli su tipo, capacità e collocazione.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_scaffale | INT | Identificativo univoco dello scaffale | PRIMARY KEY, AUTO_INCREMENT |
| tipo | ENUM('Normale', 'Frigorifero', 'Congelatore') | Tipo di scaffale | NOT NULL |
| capacita_peso | DECIMAL(10,2) | Capacità massima di peso dello scaffale | NOT NULL |
| capacita_volume | DECIMAL(10,2) | Capacità massima di volume dello scaffale | NOT NULL |
| id_reparto | INT | Identificativo del reparto di appartenenza | NOT NULL, FOREIGN KEY |

<br>

### Tabella: reparto_edificio
**Descrizione:** Tabella di collegamento che indica in quali edifici si trova un determinato reparto (relazione N:M).

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_reparto | INT | Identificativo del reparto | PRIMARY KEY, FOREIGN KEY |
| id_edificio | INT | Identificativo dell'edificio | PRIMARY KEY, FOREIGN KEY |

<br>

### Tabella: prodotti_scaffali
**Descrizione:** Tabella di collegamento che traccia la posizione e la quantità di ogni prodotto su uno specifico scaffale.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_prodotto | INT | Identificativo del prodotto | PRIMARY KEY, FOREIGN KEY |
| id_scaffale | INT | Identificativo dello scaffale | PRIMARY KEY, FOREIGN KEY |
| quantita | INT | Quantità del prodotto presente sullo scaffale | NOT NULL |
| data_collocazione | DATE | Data di collocazione del prodotto sullo scaffale | NOT NULL |

---
