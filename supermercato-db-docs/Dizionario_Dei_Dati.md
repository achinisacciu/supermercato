# Dizionario dei Dati – Database Supermercato

Questo documento fornisce una descrizione dettagliata di ogni tabella e attributo presente nel database del supermercato, basandosi sul modello logico relazionale.

---

## Gestione Personale

### Tabella: `dipendenti`

**Descrizione:** Memorizza i dati anagrafici e professionali di tutti i dipendenti del supermercato.

| Nome Attributo   | Tipo di Dato  | Descrizione                                       | Constraint              | Esempio                      |
| ---------------- | ------------- | ------------------------------------------------- | ----------------------- | ---------------------------- |
| `id_dipendente`  | INT           | Identificativo univoco del dipendente.            | Primary Key, NOT NULL   | 101                          |
| `nome`           | VARCHAR(50)   | Nome di battesimo del dipendente.                 | NOT NULL                | 'Mario'                      |
| `cognome`        | VARCHAR(50)   | Cognome del dipendente.                           | NOT NULL                | 'Rossi'                      |
| `data_nascita`   | DATE          | Data di nascita del dipendente.                   | NOT NULL                | '1990-05-15'                 |
| `email`          | VARCHAR(100)  | Indirizzo email univoco del dipendente.           | UNIQUE, NOT NULL        | 'mario.rossi@email.com'      |
| `telefono`       | VARCHAR(20)   | Numero di telefono del dipendente.                |                         | '3331234567'                 |
| `data_assunzione`| DATE          | Data in cui il dipendente è stato assunto.        | NOT NULL                | '2020-01-10'                 |
| `stipendio`      | DECIMAL(10, 2)| Retribuzione mensile lorda del dipendente.        |                         | 1600.00                      |
| `id_ruolo`       | INT           | Chiave esterna che collega al ruolo del dipendente.| Foreign Key (`ruoli`)   | 2                            |
| `id_ufficio`     | INT           | Chiave esterna che collega all'ufficio di lavoro. | Foreign Key (`uffici`)  | 5                            |

<br>

### Tabella: `ruoli`

**Descrizione:** Definisce i diversi ruoli professionali presenti in azienda, con i relativi livelli di autorizzazione.

| Nome Attributo          | Tipo di Dato  | Descrizione                                       | Constraint            | Esempio                      |
| ----------------------- | ------------- | ------------------------------------------------- | --------------------- | ---------------------------- |
| `id_ruolo`              | INT           | Identificativo univoco del ruolo.                 | Primary Key, NOT NULL | 1                            |
| `nome_ruolo`            | VARCHAR(50)   | Nome del ruolo (es. Cassiere, Magazziniere).      | UNIQUE, NOT NULL      | 'Cassiere'                   |
| `descrizione`           | TEXT          | Descrizione dettagliata delle mansioni del ruolo. |                       | 'Gestione delle transazioni' |
| `livello_autorizzazione`| INT           | Livello numerico per i permessi nel sistema.      | NOT NULL              | 3                            |

<br>

### Tabella: `titoli`

**Descrizione:** Elenca i titoli di studio o le certificazioni possedute dai dipendenti.

| Nome Attributo       | Tipo di Dato  | Descrizione                                       | Constraint            | Esempio                      |
| -------------------- | ------------- | ------------------------------------------------- | --------------------- | ---------------------------- |
| `id_titolo`          | INT           | Identificativo univoco del titolo/certificazione. | Primary Key, NOT NULL | 1                            |
| `nome_titolo`        | VARCHAR(100)  | Nome del titolo di studio o della certificazione. | NOT NULL              | 'HACCP'                      |
| `ente_emittente`     | VARCHAR(100)  | Ente che ha rilasciato il titolo.                 |                       | 'Regione Sicilia'            |
| `data_conseguimento` | DATE          | Data di ottenimento del titolo.                   | NOT NULL              | '2019-06-20'                 |
| `data_scadenza`      | DATE          | Eventuale data di scadenza della certificazione.  |                       | '2024-06-20'                 |

<br>

### Tabella: `uffici`

**Descrizione:** Contiene informazioni sugli uffici presenti nei vari edifici del supermercato.

| Nome Attributo  | Tipo di Dato | Descrizione                                     | Constraint              | Esempio               |
| --------------- | ------------ | ----------------------------------------------- | ----------------------- | --------------------- |
| `id_ufficio`    | INT          | Identificativo univoco dell'ufficio.            | Primary Key, NOT NULL   | 1                     |
| `nome_ufficio`  | VARCHAR(50)  | Nome dell'ufficio (es. Ufficio Acquisti).       | UNIQUE, NOT NULL        | 'Ufficio Risorse Umane'|
| `piano`         | INT          | Numero del piano in cui si trova l'ufficio.     |                         | 2                     |
| `id_edificio`   | INT          | Chiave esterna che collega all'edificio.        | Foreign Key (`edifici`) | 1                     |

<br>

### Tabella: `dipendenti_titoli`

**Descrizione:** Tabella di collegamento che associa i dipendenti ai titoli che possiedono (relazione N:M).

| Nome Attributo  | Tipo di Dato | Descrizione                                       | Constraint                                | Esempio |
| --------------- | ------------ | ------------------------------------------------- | ----------------------------------------- | ------- |
| `id_dipendente` | INT          | Chiave esterna che si riferisce al dipendente.    | Primary Key, Foreign Key (`dipendenti`)   | 101     |
| `id_titolo`     | INT          | Chiave esterna che si riferisce al titolo.        | Primary Key, Foreign Key (`titoli`)       | 1       |

<br>

### Tabella: `ruoli_titoli`

**Descrizione:** Tabella di collegamento che definisce quali titoli sono richiesti o preferenziali per un determinato ruolo (relazione N:M).

| Nome Attributo  | Tipo di Dato | Descrizione                                       | Constraint                              | Esempio |
| --------------- | ------------ | ------------------------------------------------- | --------------------------------------- | ------- |
| `id_ruolo`      | INT          | Chiave esterna che si riferisce al ruolo.         | Primary Key, Foreign Key (`ruoli`)      | 5       |
| `id_titolo`     | INT          | Chiave esterna che si riferisce al titolo.        | Primary Key, Foreign Key (`titoli`)     | 3       |

---

## Infrastruttura e Localizzazione

### Tabella: `edifici`

**Descrizione:** Anagrafica degli edifici di proprietà o in uso al supermercato.

| Nome Attributo        | Tipo di Dato  | Descrizione                                       | Constraint            | Esempio                           |
| --------------------- | ------------- | ------------------------------------------------- | --------------------- | --------------------------------- |
| `id_edificio`         | INT           | Identificativo univoco dell'edificio.             | Primary Key, NOT NULL | 1                                 |
| `nome_edificio`       | VARCHAR(100)  | Nome identificativo dell'edificio.                | UNIQUE, NOT NULL      | 'Supermercato Centrale'           |
| `indirizzo`           | VARCHAR(255)  | Indirizzo completo dell'edificio.                 | NOT NULL              | 'Via Roma 1, 95047 Paternò CT'    |
| `superficie_mq`       | INT           | Superficie totale in metri quadri.                |                       | 2500                              |
| `funzione_principale` | VARCHAR(100)  | Uso primario dell'edificio (es. Vendita, Magazzino).|                       | 'Punto Vendita'                   |

<br>

### Tabella: `reparti`

**Descrizione:** Definisce i vari reparti presenti all'interno dei punti vendita o dei magazzini.

| Nome Attributo  | Tipo di Dato | Descrizione                                       | Constraint            | Esempio               |
| --------------- | ------------ | ------------------------------------------------- | --------------------- | --------------------- |
| `id_reparto`    | INT          | Identificativo univoco del reparto.               | Primary Key, NOT NULL | 1                     |
| `nome_reparto`  | VARCHAR(50)  | Nome del reparto (es. Ortofrutta, Macelleria).    | UNIQUE, NOT NULL      | 'Ortofrutta'          |
| `descrizione`   | TEXT         | Breve descrizione del reparto.                    |                       | 'Frutta e verdura fresca'|

<br>

### Tabella: `scaffali`

**Descrizione:** Anagrafica degli scaffali, con dettagli su tipo, capacità e collocazione.

| Nome Attributo    | Tipo di Dato  | Descrizione                                       | Constraint              | Esempio          |
| ----------------- | ------------- | ------------------------------------------------- | ----------------------- | ---------------- |
| `id_scaffale`     | INT           | Identificativo univoco dello scaffale.            | Primary Key, NOT NULL   | 1                |
| `tipo`            | VARCHAR(50)   | Tipologia di scaffale (es. Standard, Refrigerato).| NOT NULL                | 'Refrigerato'    |
| `capacita_peso`   | DECIMAL(10, 2)| Carico massimo in kg che lo scaffale può sostenere.|                       | 500.00           |
| `capacita_volume` | DECIMAL(10, 2)| Volume massimo in m³ che lo scaffale può contenere.|                       | 2.50             |
| `id_reparto`      | INT           | Chiave esterna che collega al reparto di pertinenza.| Foreign Key (`reparti`)| 1                |

<br>

### Tabella: `reparto_edificio`

**Descrizione:** Tabella di collegamento che indica in quali edifici si trova un determinato reparto (relazione N:M).

| Nome Attributo  | Tipo di Dato | Descrizione                                       | Constraint                              | Esempio |
| --------------- | ------------ | ------------------------------------------------- | --------------------------------------- | ------- |
| `id_reparto`    | INT          | Chiave esterna che si riferisce al reparto.       | Primary Key, Foreign Key (`reparti`)    | 1       |
| `id_edificio`   | INT          | Chiave esterna che si riferisce all'edificio.     | Primary Key, Foreign Key (`edifici`)    | 1       |

<br>

### Tabella: `prodotti_scaffali`

**Descrizione:** Tabella di collegamento che traccia la posizione e la quantità di ogni prodotto su uno specifico scaffale.

| Nome Attributo       | Tipo di Dato | Descrizione                                       | Constraint                                | Esempio      |
| -------------------- | ------------ | ------------------------------------------------- | ----------------------------------------- | ------------ |
| `id_prodotto`        | INT          | Chiave esterna che si riferisce al prodotto.      | Primary Key, Foreign Key (`prodotti`)     | 101          |
| `id_scaffale`        | INT          | Chiave esterna che si riferisce allo scaffale.    | Primary Key, Foreign Key (`scaffali`)     | 1            |
| `quantita`           | INT          | Numero di unità del prodotto su questo scaffale.  | NOT NULL                                  | 50           |
| `data_collocazione`  | DATE         | Data in cui il prodotto è stato posizionato.      |                                           | '2025-07-28' |

---

## Clienti e Fidelizzazione

### Tabella: `clienti`

**Descrizione:** Anagrafica dei clienti del supermercato.

| Nome Attributo  | Tipo di Dato  | Descrizione                                       | Constraint            | Esempio                      |
| --------------- | ------------- | ------------------------------------------------- | --------------------- | ---------------------------- |
| `id_cliente`    | INT           | Identificativo univoco del cliente.               | Primary Key, NOT NULL | 1                            |
| `nome`          | VARCHAR(50)   | Nome del cliente.                                 | NOT NULL              | 'Laura'                      |
| `cognome`       | VARCHAR(50)   | Cognome del cliente.                              | NOT NULL              | 'Bianchi'                    |
| `data_nascita`  | DATE          | Data di nascita del cliente.                      |                       | '1985-11-22'                 |
| `sesso`         | ENUM('M','F','Altro')  | classificazione del sesso del cliente    |                       | F                            |
| `lavoro`        | VARCHAR(150)  | titolo lavorativo del cliente.                    |                       | Ingegniere                   |
| `email`         | VARCHAR(100)  | Indirizzo email univoco del cliente.              | UNIQUE, NOT NULL      | 'laura.bianchi@email.com'    |
| `telefono`      | VARCHAR(20)   | Numero di telefono del cliente.                   |                       | '3471122334'                 |
| `residenza`     | VARCHAR(255)  | Indirizzo di residenza del cliente.               |                       | 'Via Verdi 5, 95100 Catania' |
| `newsletter`    | BOOLEAN       | Flag che indica se il cliente è iscritto alla newsletter.| DEFAULT FALSE  | TRUE                         |

<br>

### Tabella: `carte_fidelity`

**Descrizione:** Gestisce le carte fedeltà associate ai clienti, includendo livello e punti accumulati.

| Nome Attributo     | Tipo di Dato | Descrizione                                       | Constraint              | Esempio      |
| ------------------ | ------------ | ------------------------------------------------- | ----------------------- | ------------ |
| `id_carta`         | INT          | Identificativo univoco della carta fedeltà.       | Primary Key, NOT NULL   | 1            |
| `id_cliente`       | INT          | Chiave esterna che collega al cliente possessore. | Foreign Key (`clienti`) | 1            |
| `data_iscrizione`  | DATE         | Data di emissione della carta.                    | NOT NULL                | '2022-03-15' |
| `livello`          | VARCHAR(20)  | Livello della carta (es. Silver, Gold).           |                         | 'Gold'       |
| `punti`            | INT          | Punti fedeltà accumulati sulla carta.             | DEFAULT 0               | 1250         |

<br>

### Tabella: `clienti_preferenze`

**Descrizione:** Memorizza le preferenze dei clienti riguardo a specifiche sottocategorie di prodotti, per marketing mirato.

| Nome Attributo      | Tipo di Dato | Descrizione                                       | Constraint                                    | Esempio      |
| ------------------- | ------------ | ------------------------------------------------- | --------------------------------------------- | ------------ |
| `id_cliente`        | INT          | Chiave esterna che si riferisce al cliente.       | Primary Key, Foreign Key (`clienti`)          | 1            |
| `id_sottocategoria` | INT          | Chiave esterna che si riferisce alla sottocategoria.| Primary Key, Foreign Key (`sottocategorie`) | 5            |
| `data_inserimento`  | DATE         | Data in cui la preferenza è stata registrata.     |                                               | '2023-01-20' |

<br>

### Tabella: `clienti_titoli`

**Descrizione:** Tiene traccia dei titoli che i clienti hanno conseguito viene usato per indagare sui comportamenti dei clienti.

| Nome Attributo      | Tipo di Dato | Descrizione                                       | Constraint                                    | Esempio      |
| ------------------- | ------------ | ------------------------------------------------- | --------------------------------------------- | ------------ |
| `id_cliente_titolo` | INT          | Identificativo univoco del titolo del cliente.    | Primary Key, NOT NULL                         | 1            |
| `id_cliente`        | INT          | Chiave esterna che si riferisce al cliente.       | Foreign Key (`clienti`)                       | 5            |
| `id_titolo`         | INT          | Chiave esterna che si riferisce al titolo.        | Foreign Key (`titoli`)                        | 6            |

---

## Gestione Prodotti

### Tabella: `categorie`

**Descrizione:** Definisce le macro-categorie merceologiche dei prodotti.

| Nome Attributo   | Tipo di Dato | Descrizione                                       | Constraint            | Esempio               |
| ---------------- | ------------ | ------------------------------------------------- | --------------------- | --------------------- |
| `id_categoria`   | INT          | Identificativo univoco della categoria.           | Primary Key, NOT NULL | 1                     |
| `nome_categoria` | VARCHAR(50)  | Nome della categoria (es. Alimentari, Bevande).   | UNIQUE, NOT NULL      | 'Alimentari Freschi'  |
| `descrizione`    | TEXT         | Descrizione estesa della categoria.               |                       | 'Prodotti da banco frigo'|

<br>

### Tabella: `sottocategorie`

**Descrizione:** Dettaglia le categorie in sottogruppi più specifici.

| Nome Attributo        | Tipo di Dato | Descrizione                                       | Constraint                | Esempio          |
| --------------------- | ------------ | ------------------------------------------------- | ------------------------- | ---------------- |
| `id_sottocategoria`   | INT          | Identificativo univoco della sottocategoria.      | Primary Key, NOT NULL     | 1                |
| `nome_sottocategoria` | VARCHAR(50)  | Nome della sottocategoria (es. Latticini, Pasta). | UNIQUE, NOT NULL          | 'Latticini'      |
| `id_categoria`        | INT          | Chiave esterna che collega alla categoria madre.  | Foreign Key (`categorie`)| 1                |

<br>

### Tabella: `prodotti`

**Descrizione:** Anagrafica di tutti i prodotti venduti nel supermercato.

| Nome Attributo      | Tipo di Dato    | Descrizione                                       | Constraint                      | Esempio           |
| ------------------- | --------------- | ------------------------------------------------- | ------------------------------- | ----------------- |
| `id_prodotto`       | INT             | Identificativo univoco del prodotto.              | Primary Key, NOT NULL           | 1001              |
| `nome_prodotto`     | VARCHAR(100)    | Nome commerciale del prodotto.                    | NOT NULL                        | 'Latte Intero UHT'|
| `prezzo_vendita`    | DECIMAL(10, 2)  | Prezzo di vendita al pubblico.                    | NOT NULL                        | 1.20              |
| `peso_kg`           | DECIMAL(7, 3)   | Peso del prodotto in chilogrammi.                 |                                 | 1.000             |
| `volume_cm3`        | DECIMAL(10, 2)  | Volume del prodotto in centimetri cubi.           |                                 | 1000.00           |
| `id_marca`          | INT             | Chiave esterna che collega alla marca.            | Foreign Key (`marche`)          | 1                 |
| `id_sottocategoria` | INT             | Chiave esterna che collega alla sottocategoria.   | Foreign Key (`sottocategorie`)| 1                 |
| `scadenza`          | BOOLEAN         | Flag che indica se il prodotto è soggetto a scadenza.| DEFAULT TRUE                  | TRUE              |
| `is_alimentare`     | BOOLEAN         | Flag che indica se il prodotto è di tipo alimentare.| DEFAULT TRUE                  | TRUE              |

<br>

### Tabella: `marche`

**Descrizione:** Elenca le marche dei prodotti.

| Nome Attributo  | Tipo di Dato | Descrizione                                       | Constraint                 | Esempio          |
| --------------- | ------------ | ------------------------------------------------- | -------------------------- | ---------------- |
| `id_marca`      | INT          | Identificativo univoco della marca.               | Primary Key, NOT NULL      | 1                |
| `nome_marca`    | VARCHAR(50)  | Nome della marca.                                 | UNIQUE, NOT NULL           | 'Granarolo'      |
| `id_produttore` | INT          | Chiave esterna che collega al produttore.         | Foreign Key (`produttori`)| 1                |

<br>

### Tabella: `produttori`

**Descrizione:** Anagrafica dei produttori dei beni venduti.

| Nome Attributo     | Tipo di Dato | Descrizione                                       | Constraint            | Esempio                     |
| ------------------ | ------------ | ------------------------------------------------- | --------------------- | --------------------------- |
| `id_produttore`    | INT          | Identificativo univoco del produttore.            | Primary Key, NOT NULL | 1                           |
| `nome_produttore`  | VARCHAR(100) | Ragione sociale del produttore.                   | UNIQUE, NOT NULL      | 'Granarolo S.p.A.'          |
| `nazione`          | VARCHAR(50)  | Nazione di origine del produttore.                |                       | 'Italia'                    |
| `sito_web`         | VARCHAR(255) | Sito web ufficiale del produttore.                |                       | 'https://www.granarolo.it'  |
| `telefono`         | VARCHAR(20)  | Numero di telefono del produttore.                |                       | '0514162311'                |

---

## Vendite e Scontrini

### Tabella: `scontrini`

**Descrizione:** Registra le informazioni di testata di ogni scontrino fiscale emesso.

| Nome Attributo  | Tipo di Dato | Descrizione                                       | Constraint                                  | Esempio      |
| --------------- | ------------ | ------------------------------------------------- | ------------------------------------------- | ------------ |
| `id_scontrino`  | INT          | Identificativo univoco dello scontrino.           | Primary Key, NOT NULL                       | 1            |
| `data_scontrino`| DATE         | Data di emissione dello scontrino.                | NOT NULL                                    | '2025-07-29' |
| `ora_scontrino` | TIME         | Ora di emissione dello scontrino.                 | NOT NULL                                    | '18:30:00'   |
| `id_cassa`      | INT          | Chiave esterna che collega alla cassa emittente.  | Foreign Key (`casse`), NOT NULL             | 1            |
| `id_dipendente` | INT          | Chiave esterna che collega al dipendente cassiere.| Foreign Key (`dipendenti`), NOT NULL        | 101          |
| `id_cliente`    | INT          | Chiave esterna che collega al cliente (opzionale).| Foreign Key (`clienti`)                     | 1            |

<br>

### Tabella: `dettagli_scontrino`

**Descrizione:** Contiene le singole righe di dettaglio per ogni scontrino, con i prodotti acquistati.

| Nome Attributo       | Tipo di Dato   | Descrizione                                       | Constraint                                | Esempio |
| -------------------- | -------------- | ------------------------------------------------- | ----------------------------------------- | ------- |
| `id_dettaglio`       | INT            | Identificativo univoco della riga di dettaglio.   | Primary Key, NOT NULL                     | 1       |
| `id_scontrino`       | INT            | Chiave esterna che collega alla testata scontrino.| Foreign Key (`scontrini`), NOT NULL       | 1       |
| `id_prodotto`        | INT            | Chiave esterna che collega al prodotto venduto.   | Foreign Key (`prodotti`), NOT NULL        | 1001    |
| `quantita`           | INT            | Numero di unità del prodotto acquistate.          | NOT NULL                                  | 2       |
| `prezzo_unitario`    | DECIMAL(10, 2) | Prezzo del prodotto al momento della vendita.     | NOT NULL                                  | 1.20    |
| `sconto_percentuale` | DECIMAL(5, 2)  | Sconto applicato alla singola riga.               | DEFAULT 0.00                              | 10.00   |

<br>

### Tabella: `casse`

**Descrizione:** Anagrafica delle casse presenti nei punti vendita.

| Nome Attributo  | Tipo di Dato | Descrizione                                       | Constraint              | Esempio           |
| --------------- | ------------ | ------------------------------------------------- | ----------------------- | ----------------- |
| `id_cassa`      | INT          | Identificativo univoco della cassa.               | Primary Key, NOT NULL   | 1                 |
| `numero_cassa`  | INT          | Numero identificativo della cassa nel punto vendita.| NOT NULL                | 1                 |
| `tipo`          | VARCHAR(50)  | Tipologia di cassa (es. Standard, Self-service).  | NOT NULL                | 'Standard'        |
| `stato`         | VARCHAR(20)  | Stato operativo della cassa (es. Attiva, Inattiva).| NOT NULL                | 'Attiva'          |
| `id_edificio`   | INT          | Chiave esterna che collega all'edificio.          | Foreign Key (`edifici`)| 1                 |

<br>

### Tabella: `pagamenti`

**Descrizione:** Registra i dettagli delle transazioni di pagamento associate a ogni scontrino.

| Nome Attributo   | Tipo di Dato   | Descrizione                                       | Constraint                  | Esempio      |
| ---------------- | -------------- | ------------------------------------------------- | --------------------------- | ------------ |
| `id_pagamento`   | INT            | Identificativo univoco del pagamento.             | Primary Key, NOT NULL       | 1            |
| `id_scontrino`   | INT            | Chiave esterna che collega allo scontrino.        | Foreign Key (`scontrini`)   | 1            |
| `metodo`         | VARCHAR(50)    | Metodo di pagamento (es. Contanti, Carta Credito).| NOT NULL                    | 'Carta Credito'|
| `importo`        | DECIMAL(10, 2) | Importo pagato con questo metodo.                 | NOT NULL                    | 25.50        |
| `data_pagamento` | DATETIME       | Data e ora esatta della transazione.              | NOT NULL                    | '2025-07-29 18:31:00'|

---

## Fornitori e Approvvigionamenti

### Tabella: `fornitori`

**Descrizione:** Anagrafica dei fornitori di prodotti e servizi.

| Nome Attributo     | Tipo di Dato | Descrizione                                       | Constraint            | Esempio                     |
| ------------------ | ------------ | ------------------------------------------------- | --------------------- | --------------------------- |
| `id_fornitore`     | INT          | Identificativo univoco del fornitore.             | Primary Key, NOT NULL | 1                           |
| `nome_fornitore`   | VARCHAR(100) | Ragione sociale del fornitore.                    | UNIQUE, NOT NULL      | 'Frutta & Co. Srl'          |
| `partita_iva`      | VARCHAR(11)  | Partita IVA del fornitore.                        | UNIQUE, NOT NULL      | '01234567890'               |
| `email`            | VARCHAR(100) | Indirizzo email di contatto del fornitore.        | UNIQUE, NOT NULL      | 'info@fruttaco.it'          |
| `telefono`         | VARCHAR(20)  | Numero di telefono del fornitore.                 |                       | '029876543'                 |
| `affidabilita`     | INT          | Punteggio di affidabilità del fornitore (1-5).    |                       | 5                           |

<br>

### Tabella: `ordini_fornitore`

**Descrizione:** Registra gli ordini di acquisto inviati ai fornitori.

| Nome Attributo            | Tipo di Dato | Descrizione                                       | Constraint                 | Esempio      |
| ------------------------- | ------------ | ------------------------------------------------- | -------------------------- | ------------ |
| `id_ordine`               | INT          | Identificativo univoco dell'ordine.               | Primary Key, NOT NULL      | 1            |
| `id_fornitore`            | INT          | Chiave esterna che collega al fornitore.          | Foreign Key (`fornitori`)  | 1            |
| `data_ordine`             | DATE         | Data di emissione dell'ordine.                    | NOT NULL                   | '2025-07-20' |
| `data_prevista_consegna`  | DATE         | Data in cui è prevista la consegna della merce.   |                            | '2025-07-27' |
| `stato`                   | VARCHAR(20)  | Stato dell'ordine (es. Inviato, Consegnato).      | NOT NULL                   | 'Consegnato' |

<br>

### Tabella: `dettagli_ordine`

**Descrizione:** Contiene le righe di dettaglio di ogni ordine fornitore, con i prodotti e le quantità ordinate.

| Nome Attributo   | Tipo di Dato   | Descrizione                                       | Constraint                                  | Esempio |
| ---------------- | -------------- | ------------------------------------------------- | ------------------------------------------- | ------- |
| `id_dettaglio`   | INT            | Identificativo univoco della riga di dettaglio.   | Primary Key, NOT NULL                       | 1       |
| `id_ordine`      | INT            | Chiave esterna che collega all'ordine fornitore.  | Foreign Key (`ordini_fornitore`), NOT NULL  | 1       |
| `id_prodotto`    | INT            | Chiave esterna che collega al prodotto ordinato.  | Foreign Key (`prodotti`), NOT NULL          | 1001    |
| `quantita`       | INT            | Quantità di prodotto ordinata.                    | NOT NULL                                    | 200     |
| `prezzo_unitario`| DECIMAL(10, 2) | Prezzo d'acquisto unitario pattuito.              | NOT NULL                                    | 0.80    |

<br>

### Tabella: `offerte_fornitore`

**Descrizione:** Memorizza le offerte speciali sui prezzi d'acquisto proposte dai fornitori per determinati prodotti e periodi.

| Nome Attributo    | Tipo di Dato   | Descrizione                                       | Constraint                                | Esempio      |
| ----------------- | -------------- | ------------------------------------------------- | ----------------------------------------- | ------------ |
| `id_fornitore`    | INT            | Chiave esterna che si riferisce al fornitore.     | Primary Key, Foreign Key (`fornitori`)    | 1            |
| `id_prodotto`     | INT            | Chiave esterna che si riferisce al prodotto.      | Primary Key, Foreign Key (`prodotti`)     | 1001         |
| `prezzo_offerta`  | DECIMAL(10, 2) | Prezzo speciale offerto dal fornitore.            | NOT NULL                                  | 0.75         |
| `data_inizio`     | DATE           | Data di inizio validità dell'offerta.             | Primary Key, NOT NULL                     | '2025-08-01' |
| `data_fine`       | DATE           | Data di fine validità dell'offerta.               |                                           | '2025-08-31' |

---

## Promozioni e Marketing

### Tabella: `promozioni`

**Descrizione:** Definisce le campagne promozionali applicate ai prodotti in vendita.

| Nome Attributo       | Tipo di Dato   | Descrizione                                       | Constraint            | Esempio               |
| -------------------- | -------------- | ------------------------------------------------- | --------------------- | --------------------- |
| `id_promozione`      | INT            | Identificativo univoco della promozione.          | Primary Key, NOT NULL | 1                     |
| `nome`               | VARCHAR(100)   | Nome della promozione (es. "Sconto Estivo").      | UNIQUE, NOT NULL      | 'Offerta Latticini'   |
| `descrizione`        | TEXT           | Descrizione dettagliata della promozione.         |                       | 'Sconto del 20% su...' |
| `sconto_percentuale` | DECIMAL(5, 2)  | Sconto percentuale applicato (se unico).          |                       | 20.00                 |
| `data_inizio`        | DATE           | Data di inizio della promozione.                  | NOT NULL              | '2025-08-01'          |
| `data_fine`          | DATE           | Data di fine della promozione.                    | NOT NULL              | '2025-08-15'          |

<br>

### Tabella: `promozioni_prodotti`

**Descrizione:** Tabella di collegamento che associa i prodotti specifici a una campagna promozionale (relazione N:M).

| Nome Attributo  | Tipo di Dato | Descrizione                                       | Constraint                                  | Esempio |
| --------------- | ------------ | ------------------------------------------------- | ------------------------------------------- | ------- |
| `id_promozione` | INT          | Chiave esterna che si riferisce alla promozione.   | Primary Key, Foreign Key (`promozioni`)     | 1       |
| `id_prodotto`   | INT          | Chiave esterna che si riferisce al prodotto.      | Primary Key, Foreign Key (`prodotti`)       | 1001    |

---

## Inventario e Magazzino

### Tabella: `inventario`

**Descrizione:** Riepiloga la quantità totale di ogni prodotto per ogni scaffale, reparto ed edificio, fungendo da vista materializzata per rapide interrogazioni sulla giacenza.

| Nome Attributo              | Tipo di Dato | Descrizione                                       | Constraint                                                              | Esempio      |
| --------------------------- | ------------ | ------------------------------------------------- | ----------------------------------------------------------------------- | ------------ |
| `id_inventario`             | INT          | Identificativo univoco della riga di inventario.  | Primary Key, NOT NULL                                                   | 1            |
| `id_prodotto`               | INT          | Chiave esterna che collega al prodotto.           | Foreign Key (`prodotti`), NOT NULL                                      | 1001         |
| `id_scaffale`               | INT          | Chiave esterna che collega allo scaffale.         | Foreign Key (`scaffali`), NOT NULL                                      | 15           |
| `id_reparto`                | INT          | Chiave esterna che collega al reparto.            | Foreign Key (`reparti`), NOT NULL                                       | 3            |
| `id_edificio`               | INT          | Chiave esterna che collega all'edificio.          | Foreign Key (`edifici`), NOT NULL                                       | 1            |
| `quantita`                  | INT          | Quantità di prodotto in questa locazione.         | NOT NULL                                                                | 150          |
| `data_ultimo_aggiornamento` | DATETIME     | Data e ora dell'ultimo aggiornamento della giacenza.| NOT NULL                                                                | '2025-07-29 10:00:00'|
