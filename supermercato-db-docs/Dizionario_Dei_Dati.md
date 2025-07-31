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
**Descrizione:** Definisce i diversi ruoli professionali presenti in azienda, con i relativi livelli di autorizzazione.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_ruolo | INT | Identificativo univoco del ruolo | PRIMARY KEY, AUTO_INCREMENT |
| nome_ruolo | VARCHAR(100) | Nome del ruolo lavorativo | NOT NULL |
| descrizione | TEXT | Descrizione dettagliata del ruolo | - |
| livello_autorizzazione | ENUM('Operativo', 'Supervisione', 'Manageriale') | Livello di autorizzazione del ruolo | NOT NULL |

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

## Clienti e Fidelizzazione

### Tabella: clienti
**Descrizione:** Anagrafica dei clienti del supermercato.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_cliente | INT | Identificativo univoco del cliente | PRIMARY KEY, AUTO_INCREMENT |
| nome | VARCHAR(100) | Nome del cliente | NOT NULL |
| cognome | VARCHAR(100) | Cognome del cliente | NOT NULL |
| data_nascita | DATE | Data di nascita del cliente | NOT NULL |
| sesso | ENUM('M', 'F', 'Altro') | Sesso del cliente | DEFAULT NULL |
| lavoro | VARCHAR(150) | Professione del cliente | - |
| email | VARCHAR(150) | Indirizzo email del cliente | UNIQUE |
| telefono | VARCHAR(20) | Numero di telefono del cliente | UNIQUE |
| residenza | VARCHAR(255) | Indirizzo di residenza del cliente | - |
| newsletter | TINYINT(1) | Consenso per ricevere newsletter | DEFAULT '0' |

<br>

### Tabella: carte_fidelity
**Descrizione:** Gestisce le carte fedeltà associate ai clienti, includendo livello e punti accumulati.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_carta | INT | Identificativo univoco della carta fidelity | PRIMARY KEY, AUTO_INCREMENT |
| id_cliente | INT | Identificativo del cliente proprietario | NOT NULL, UNIQUE, FOREIGN KEY |
| data_iscrizione | DATE | Data di iscrizione al programma fedeltà | NOT NULL |
| livello | ENUM('Bronze', 'Silver', 'Gold') | Livello della carta fedeltà | DEFAULT 'Bronze' |
| punti | INT | Punti fedeltà accumulati | DEFAULT '0' |

<br>

### Tabella: clienti_preferenze
**Descrizione:** Memorizza le preferenze dei clienti riguardo a specifiche sottocategorie di prodotti, per marketing mirato.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_cliente | INT | Identificativo del cliente | PRIMARY KEY, FOREIGN KEY |
| id_sottocategoria | INT | Identificativo della sottocategoria preferita | PRIMARY KEY, FOREIGN KEY |
| data_inserimento | DATE | Data di inserimento della preferenza | NOT NULL |

<br>

### Tabella: clienti_titoli
**Descrizione:** Tiene traccia dei titoli che i clienti hanno conseguito viene usato per indagare sui comportamenti dei clienti.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_clienti_titoli | INT | Identificativo univoco della relazione | PRIMARY KEY, AUTO_INCREMENT |
| id_cliente | INT | Identificativo del cliente | NOT NULL, FOREIGN KEY |
| id_titolo | INT | Identificativo del titolo posseduto | NOT NULL, FOREIGN KEY |

---

## Gestione Prodotti

### Tabella: categorie
**Descrizione:** Definisce le macro-categorie merceologiche dei prodotti.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_categoria | INT | Identificativo univoco della categoria | PRIMARY KEY, AUTO_INCREMENT |
| nome_categoria | VARCHAR(100) | Nome della categoria di prodotti | NOT NULL |
| descrizione | TEXT | Descrizione della categoria | - |

<br>

### Tabella: sottocategorie
**Descrizione:** Dettaglia le categorie in sottogruppi più specifici.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_sottocategoria | INT | Identificativo univoco della sottocategoria | PRIMARY KEY, AUTO_INCREMENT |
| nome_sottocategoria | VARCHAR(100) | Nome della sottocategoria | NOT NULL |
| id_categoria | INT | Identificativo della categoria padre | NOT NULL, FOREIGN KEY |

<br>

### Tabella: prodotti
**Descrizione:** Anagrafica di tutti i prodotti venduti nel supermercato.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_prodotto | INT | Identificativo univoco del prodotto | PRIMARY KEY, AUTO_INCREMENT |
| nome_prodotto | VARCHAR(150) | Nome del prodotto | NOT NULL |
| prezzo_vendita | DECIMAL(10,2) | Prezzo di vendita del prodotto | NOT NULL |
| peso_kg | DECIMAL(6,3) | Peso del prodotto in chilogrammi | - |
| volume_cm3 | INT | Volume del prodotto in centimetri cubi | - |
| id_marca | INT | Identificativo della marca del prodotto | NOT NULL, FOREIGN KEY |
| id_sottocategoria | INT | Identificativo della sottocategoria | NOT NULL, FOREIGN KEY |
| scadenza | DATE | Data di scadenza del prodotto | - |
| is_alimentare | TINYINT(1) | Indica se il prodotto è alimentare | DEFAULT '1' |

<br>

### Tabella: marche
**Descrizione:** Elenca le marche dei prodotti.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_marca | INT | Identificativo univoco della marca | PRIMARY KEY, AUTO_INCREMENT |
| nome_marca | VARCHAR(100) | Nome della marca | NOT NULL |
| id_produttore | INT | Identificativo del produttore della marca | NOT NULL, FOREIGN KEY |

<br>

### Tabella: produttori
**Descrizione:** Anagrafica dei produttori dei beni venduti.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_produttore | INT | Identificativo univoco del produttore | PRIMARY KEY, AUTO_INCREMENT |
| nome_produttore | VARCHAR(100) | Nome del produttore | NOT NULL |
| nazione | VARCHAR(50) | Nazione di origine del produttore | - |
| sito_web | VARCHAR(150) | Sito web del produttore | - |
| telefono | VARCHAR(20) | Numero di telefono del produttore | - |

---

## Vendite e Scontrini

### Tabella: scontrini
**Descrizione:** Registra le informazioni di testata di ogni scontrino fiscale emesso.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_scontrino | INT | Identificativo univoco dello scontrino | PRIMARY KEY, AUTO_INCREMENT |
| data_scontrino | DATE | Data di emissione dello scontrino | NOT NULL |
| ora_scontrino | TIME | Ora di emissione dello scontrino | NOT NULL |
| id_cassa | INT | Identificativo della cassa utilizzata | NOT NULL, FOREIGN KEY |
| id_dipendente | INT | Identificativo del dipendente che ha emesso lo scontrino | NOT NULL, FOREIGN KEY |
| id_cliente | INT | Identificativo del cliente (opzionale) | FOREIGN KEY |

<br>

### Tabella: dettagli_scontrino
**Descrizione:** Contiene le singole righe di dettaglio per ogni scontrino, con i prodotti acquistati.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_dettaglio | INT | Identificativo univoco del dettaglio | PRIMARY KEY, AUTO_INCREMENT |
| id_scontrino | INT | Identificativo dello scontrino di riferimento | NOT NULL, FOREIGN KEY |
| id_prodotto | INT | Identificativo del prodotto venduto | NOT NULL, FOREIGN KEY |
| quantita | INT | Quantità del prodotto venduta | NOT NULL |
| prezzo_unitario | DECIMAL(10,2) | Prezzo unitario del prodotto al momento della vendita | NOT NULL |
| sconto_percentuale | DECIMAL(5,2) | Percentuale di sconto applicata | DEFAULT '0.00' |

<br>

### Tabella: casse
**Descrizione:** Anagrafica delle casse presenti nei punti vendita.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_cassa | INT | Identificativo univoco della cassa | PRIMARY KEY, AUTO_INCREMENT |
| numero_cassa | INT | Numero identificativo della cassa | NOT NULL |
| tipo | ENUM('Manuale', 'Automatica') | Tipo di cassa | NOT NULL |
| stato | ENUM('Attiva', 'In manutenzione', 'Disattivata') | Stato operativo della cassa | DEFAULT 'Attiva' |
| id_edificio | INT | Identificativo dell'edificio dove si trova la cassa | NOT NULL, FOREIGN KEY |

<br>

### Tabella: pagamenti
**Descrizione:** Registra i dettagli delle transazioni di pagamento associate a ogni scontrino.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_pagamento | INT | Identificativo univoco del pagamento | PRIMARY KEY, AUTO_INCREMENT |
| id_scontrino | INT | Identificativo dello scontrino pagato | NOT NULL, FOREIGN KEY |
| metodo | ENUM('Contanti', 'Carta di Credito', 'Carta di Debito', 'Digital Wallet') | Metodo di pagamento utilizzato | NOT NULL |
| importo | DECIMAL(10,2) | Importo del pagamento | NOT NULL |
| data_pagamento | DATE | Data del pagamento | NOT NULL |

---

## Fornitori e Approvvigionamenti

### Tabella: fornitori
**Descrizione:** Anagrafica dei fornitori di prodotti e servizi.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_fornitore | INT | Identificativo univoco del fornitore | PRIMARY KEY, AUTO_INCREMENT |
| nome_fornitore | VARCHAR(100) | Nome del fornitore | NOT NULL |
| partita_iva | VARCHAR(20) | Partita IVA del fornitore | NOT NULL, UNIQUE |
| email | VARCHAR(150) | Indirizzo email del fornitore | - |
| telefono | VARCHAR(20) | Numero di telefono del fornitore | - |
| affidabilita | TINYINT | Indice di affidabilità del fornitore | - |

<br>

### Tabella: ordini_fornitore
**Descrizione:** Registra gli ordini di acquisto inviati ai fornitori.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_ordine | INT | Identificativo univoco dell'ordine | PRIMARY KEY, AUTO_INCREMENT |
| id_fornitore | INT | Identificativo del fornitore | NOT NULL, FOREIGN KEY |
| data_ordine | DATE | Data di emissione dell'ordine | NOT NULL |
| data_prevista_consegna | DATE | Data prevista per la consegna | - |
| stato | ENUM('In attesa', 'Consegnato', 'Annullato') | Stato dell'ordine | DEFAULT 'In attesa' |

<br>

### Tabella: dettagli_ordine
**Descrizione:** Contiene le righe di dettaglio di ogni ordine fornitore, con i prodotti e le quantità ordinate.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_dettaglio | INT | Identificativo univoco del dettaglio ordine | PRIMARY KEY, AUTO_INCREMENT |
| id_ordine | INT | Identificativo dell'ordine di riferimento | NOT NULL, FOREIGN KEY |
| id_prodotto | INT | Identificativo del prodotto ordinato | NOT NULL, FOREIGN KEY |
| quantita | INT | Quantità del prodotto ordinata | NOT NULL |
| prezzo_unitario | DECIMAL(10,2) | Prezzo unitario del prodotto nell'ordine | NOT NULL |

<br>

### Tabella: offerte_fornitore
**Descrizione:** Memorizza le offerte speciali sui prezzi d'acquisto proposte dai fornitori per determinati prodotti e periodi.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_fornitore | INT | Identificativo del fornitore che fa l'offerta | PRIMARY KEY, FOREIGN KEY |
| id_prodotto | INT | Identificativo del prodotto in offerta | PRIMARY KEY, FOREIGN KEY |
| prezzo_offerta | DECIMAL(10,2) | Prezzo scontato offerto dal fornitore | NOT NULL |
| data_inizio | DATE | Data di inizio validità dell'offerta | NOT NULL |
| data_fine | DATE | Data di fine validità dell'offerta | NOT NULL |

---

## Promozioni e Marketing

### Tabella: promozioni
**Descrizione:** Definisce le campagne promozionali applicate ai prodotti in vendita.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_promozione | INT | Identificativo univoco della promozione | PRIMARY KEY, AUTO_INCREMENT |
| nome | VARCHAR(100) | Nome della promozione | NOT NULL |
| descrizione | TEXT | Descrizione dettagliata della promozione | - |
| sconto_percentuale | DECIMAL(5,2) | Percentuale di sconto della promozione | - |
| data_inizio | DATE | Data di inizio validità della promozione | NOT NULL |
| data_fine | DATE | Data di fine validità della promozione | NOT NULL |

<br>

### Tabella: promozioni_prodotti
**Descrizione:** Tabella di collegamento che associa i prodotti specifici a una campagna promozionale (relazione N:M).

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_promozione | INT | Identificativo della promozione | PRIMARY KEY, FOREIGN KEY |
| id_prodotto | INT | Identificativo del prodotto in promozione | PRIMARY KEY, FOREIGN KEY |

---

## Inventario e Magazzino

### Tabella: inventario
**Descrizione:** Riepiloga la quantità totale di ogni prodotto per ogni scaffale, reparto ed edificio, fungendo da vista materializzata per rapide interrogazioni sulla giacenza.

| Nome Attributo | Tipo di Dato | Descrizione | Constraint/Extra |
|---|---|---|---|
| id_inventario | INT | Identificativo univoco del record di inventario | PRIMARY KEY, AUTO_INCREMENT |
| id_prodotto | INT | Identificativo del prodotto | NOT NULL, FOREIGN KEY |
| id_scaffale | INT | Identificativo dello scaffale dove è posizionato | NOT NULL, FOREIGN KEY |
| id_reparto | INT | Identificativo del reparto di appartenenza | NOT NULL, FOREIGN KEY |
| id_edificio | INT | Identificativo dell'edificio dove si trova | NOT NULL, FOREIGN KEY |
| quantita | INT | Quantità disponibile del prodotto | NOT NULL |
| data_ultimo_aggiornamento | DATE | Data dell'ultimo aggiornamento dell'inventario | NOT NULL |
