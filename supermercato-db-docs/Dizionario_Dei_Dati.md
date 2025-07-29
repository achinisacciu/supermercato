# Dizionario dei Dati - Database Supermercato

## Entità

| Entità           | Attributo                   | Descrizione Business                                                                 | Tipo        | Obbligatorietà | Dominio                          |
|------------------|----------------------------|-------------------------------------------------------------------------------------|-------------|----------------|----------------------------------|
| clienti          | id_cliente                 | Identificatore unico del cliente                                                    | INT         | PK             | Valore unico                     |
|                  | nome                       | Nome del cliente                                                                    | VARCHAR(50) | Sì             | Testo                            |
|                  | cognome                    | Cognome del cliente                                                                 | VARCHAR(50) | Sì             | Testo                            |
|                  | dob                        | Data di nascita del cliente                                                         | DATE        | Sì             | Formato data (YYYY-MM-DD)        |
|                  | sesso                      | Sesso del cliente                                                                   | CHAR(1)     | No             | M/F                              |
|                  | residenza                  | Indirizzo di residenza del cliente                                                  | VARCHAR(100)| Sì             | Testo                            |
|                  | CF                         | Codice Fiscale del cliente                                                          | VARCHAR(16) | Sì             | Alfanumerico (16 caratteri)      |
|                  | lavoro                     | Occupazione del cliente                                                             | VARCHAR(50) | No             | Testo                            |
|                  | id_titolo                  | Riferimento al titolo del cliente                                                   | INT         | No             | FK (titoli.id_titolo)            |
| titoli           | id_titolo                  | Identificatore unico del titolo                                                     | INT         | PK             | Valore unico                     |
|                  | nome                       | Nome del titolo                                                                     | VARCHAR(50) | Sì             | Testo                            |
|                  | descrizione                | Descrizione del titolo                                                              | TEXT        | No             | Testo                            |
|                  | scadenza                   | Data di scadenza del titolo                                                         | DATE        | No             | Formato data (YYYY-MM-DD)        |
|                  | eqf                        | Livello EQF del titolo                                                              | INT         | No             | Valore numerico (1-8)            |
| produttori       | id_produttore              | Identificatore unico del produttore                                                 | INT         | PK             | Valore unico                     |
|                  | ragione_sociale            | Nome legale del produttore                                                          | VARCHAR(100)| Sì             | Testo                            |
|                  | p_iva                      | Partita IVA del produttore                                                          | VARCHAR(11) | Sì             | Numerico (11 cifre)              |
|                  | indirizzo                  | Indirizzo del produttore                                                            | VARCHAR(100)| Sì             | Testo                            |
|                  | telefono                   | Numero di telefono del produttore                                                   | VARCHAR(15) | No             | Numerico                         |
|                  | e-mail                     | Indirizzo email del produttore                                                      | VARCHAR(50) | No             | Formato email                    |
| marche           | id_marca                   | Identificatore unico della marca                                                    | INT         | PK             | Valore unico                     |
|                  | id_produttore              | Riferimento al produttore della marca                                               | INT         | Sì             | FK (produttori.id_produttore)    |
|                  | id_categoria               | Riferimento alla categoria associata alla marca                                     | INT         | No             | FK (categorie.id_categoria)      |
|                  | nome                       | Nome della marca                                                                    | VARCHAR(50) | Sì             | Testo                            |
| categorie        | id_categoria               | Identificatore unico della categoria                                                | INT         | PK             | Valore unico                     |
|                  | nome_categoria             | Nome della categoria                                                                | VARCHAR(50) | Sì             | Testo                            |
| sottocategorie   | id_sottocategoria          | Identificatore unico della sottocategoria                                           | INT         | PK             | Valore unico                     |
|                  | nome_sottocategoria        | Nome della sottocategoria                                                           | VARCHAR(50) | Sì             | Testo                            |
|                  | id_categoria               | Riferimento alla categoria di appartenenza                                          | INT         | Sì             | FK (categorie.id_categoria)      |
| prodotti         | id_prodotto                | Identificatore unico del prodotto                                                   | INT         | PK             | Valore unico                     |
|                  | nome                       | Nome del prodotto                                                                   | VARCHAR(50) | Sì             | Testo                            |
|                  | descrizione                | Descrizione del prodotto                                                            | TEXT        | No             | Testo                            |
|                  | prezzo_unitario_vendita    | Prezzo di vendita unitario del prodotto                                             | DECIMAL(10,2)| Sì             | Valore positivo                  |
|                  | peso_su_scaffale           | Peso del prodotto sullo scaffale                                                    | DECIMAL(10,2)| No             | Valore positivo                  |
|                  | volume_su_scaffale         | Volume occupato dal prodotto sullo scaffale                                          | DECIMAL(10,2)| No             | Valore positivo                  |
|                  | id_sottocategoria          | Riferimento alla sottocategoria del prodotto                                        | INT         | Sì             | FK (sottocategorie.id_sottocategoria) |
|                  | id_marca                   | Riferimento alla marca del prodotto                                                 | INT         | Sì             | FK (marche.id_marca)             |
| fornitori        | id_fornitore               | Identificatore unico del fornitore                                                  | INT         | PK             | Valore unico                     |
|                  | ragione_sociale            | Nome legale del fornitore                                                           | VARCHAR(100)| Sì             | Testo                            |
|                  | p_iva                      | Partita IVA del fornitore                                                           | VARCHAR(11) | Sì             | Numerico (11 cifre)              |
|                  | indirizzo                  | Indirizzo del fornitore                                                             | VARCHAR(100)| Sì             | Testo                            |
|                  | telefono                   | Numero di telefono del fornitore                                                    | VARCHAR(15) | No             | Numerico                         |
|                  | e-mail                     | Indirizzo email del fornitore                                                       | VARCHAR(50) | No             | Formato email                    |
| ordini_fornitori | id_ordine                  | Identificatore unico dell'ordine                                                    | INT         | PK             | Valore unico                     |
|                  | data_ordine                | Data in cui è stato effettuato l'ordine                                             | DATE        | Sì             | Formato data (YYYY-MM-DD)        |
|                  | data_consegna_prevista     | Data prevista per la consegna dell'ordine                                           | DATE        | Sì             | Formato data (YYYY-MM-DD)        |
|                  | stato                      | Stato corrente dell'ordine                                                          | VARCHAR(20) | Sì             | "In attesa", "Spedito", "Consegnato" |
|                  | id_fornitore               | Riferimento al fornitore dell'ordine                                                | INT         | Sì             | FK (fornitori.id_fornitore)      |
| dipendenti       | id_dipendente              | Identificatore unico del dipendente                                                 | INT         | PK             | Valore unico                     |
|                  | nome                       | Nome del dipendente                                                                 | VARCHAR(50) | Sì             | Testo                            |
|                  | cognome                    | Cognome del dipendente                                                              | VARCHAR(50) | Sì             | Testo                            |
|                  | dob                        | Data di nascita del dipendente                                                      | DATE        | Sì             | Formato data (YYYY-MM-DD)        |
|                  | CF                         | Codice Fiscale del dipendente                                                       | VARCHAR(16) | Sì             | Alfanumerico (16 caratteri)      |
|                  | residenza                  | Indirizzo di residenza del dipendente                                               | VARCHAR(100)| Sì             | Testo                            |
|                  | telefono                   | Numero di telefono del dipendente                                                   | VARCHAR(15) | No             | Numerico                         |
|                  | e-mail                     | Indirizzo email del dipendente                                                      | VARCHAR(50) | No             | Formato email                    |
| ruoli            | id_ruoli                   | Identificatore unico del ruolo                                                      | INT         | PK             | Valore unico                     |
|                  | nome                       | Nome del ruolo                                                                      | VARCHAR(50) | Sì             | Testo                            |
| scontrini        | id_scontrino               | Identificatore unico dello scontrino                                                | INT         | PK             | Valore unico                     |
|                  | data_scontrino             | Data di emissione dello scontrino                                                   | DATE        | Sì             | Formato data (YYYY-MM-DD)        |
|                  | ora_scontrino              | Ora di emissione dello scontrino                                                    | TIME        | Sì             | Formato ora (HH:MM:SS)           |
|                  | id_personale               | Riferimento al dipendente che ha emesso lo scontrino                                 | INT         | Sì             | FK (dipendenti.id_dipendente)    |
|                  | id_cliente                 | Riferimento al cliente associato allo scontrino                                     | INT         | No             | FK (clienti.id_cliente)          |
| edifici          | id_edificio                | Identificatore unico dell'edificio                                                  | INT         | PK             | Valore unico                     |
|                  | tipo_edificio              | Tipo di edificio (punto vendita, magazzino)                                         | VARCHAR(20) | Sì             | "Punto vendita", "Magazzino"     |
|                  | città                      | Città in cui si trova l'edificio                                                    | VARCHAR(50) | Sì             | Testo                            |
|                  | indirizzo                  | Indirizzo dell'edificio                                                             | VARCHAR(100)| Sì             | Testo                            |
|                  | cap                        | Codice di avviamento postale dell'edificio                                          | VARCHAR(5)  | Sì             | Numerico (5 cifre)               |
| reparti          | id_reparto                 | Identificatore unico del reparto                                                    | INT         | PK             | Valore unico                     |
|                  | nome                       | Nome del reparto                                                                    | VARCHAR(50) | Sì             | Testo                            |
|                  | id_edificio                | Riferimento all'edificio in cui si trova il reparto                                 | INT         | Sì             | FK (edifici.id_edificio)         |
| uffici           | id_ufficio                 | Identificatore unico dell'ufficio                                                   | INT         | PK             | Valore unico                     |
|                  | nome                       | Nome dell'ufficio                                                                   | VARCHAR(50) | Sì             | Testo                            |
|                  | descrizione                | Descrizione dell'ufficio                                                            | TEXT        | No             | Testo                            |
|                  | id_edificio                | Riferimento all'edificio in cui si trova l'ufficio                                  | INT         | Sì             | FK (edifici.id_edificio)         |

## Tabelle di Associazione

| Tabella            | Attributo                   | Descrizione Business                                                                 | Tipo        | Obbligatorietà | Dominio                          |
|--------------------|----------------------------|-------------------------------------------------------------------------------------|-------------|----------------|----------------------------------|
| dipendenti_ruoli   | id_dipendenti_ruoli        | Identificatore unico dell'associazione                                              | INT         | PK             | Valore unico                     |
|                    | id_dipendente              | Riferimento al dipendente                                                           | INT         | Sì             | FK (dipendenti.id_dipendente)    |
|                    | id_ruolo                   | Riferimento al ruolo                                                                | INT         | Sì             | FK (ruoli.id_ruoli)              |
| dipendenti_titoli  | id_dipendenti_titoli       | Identificatore unico dell'associazione                                              | INT         | PK             | Valore unico                     |
|                    | id_dipendente              | Riferimento al dipendente                                                           | INT         | Sì             | FK (dipendenti.id_dipendente)    |
|                    | id_titolo                  | Riferimento al titolo                                                               | INT         | Sì             | FK (titoli.id_titolo)            |
| carte_fedelity     | id_carta                   | Identificatore unico della carta fedeltà                                            | INT         | PK             | Valore unico                     |
|                    | punteggio                 | Punteggio accumulato sulla carta fedeltà                                            | INT         | Sì             | Valore positivo                  |
|                    | data_iscrizione           | Data di iscrizione alla carta fedeltà                                               | DATE        | Sì             | Formato data (YYYY-MM-DD)        |
|                    | id_cliente                 | Riferimento al cliente proprietario della carta                                     | INT         | Sì             | FK (clienti.id_cliente)          |
| detaglio_scontrino | id_scontrino               | Riferimento allo scontrino                                                          | INT         | PK/FK          | FK (scontrini.id_scontrino)      |
|                    | id_prodotto                | Riferimento al prodotto                                                             | INT         | PK/FK          | FK (prodotti.id_prodotto)        |
|                    | quantita                   | Quantità del prodotto nello scontrino                                               | INT         | Sì             | Valore positivo                  |
|                    | prezzo_unitario_vendita    | Prezzo unitario di vendita del prodotto                                             | DECIMAL(10,2)| Sì             | Valore positivo                  |
|                    | sconto_applicato           | Sconto applicato al prodotto                                                        | DECIMAL(5,2)| No             | Valore percentuale (0-100)       |
| dettaglio_ordine   | id_ordine                  | Riferimento all'ordine                                                              | INT         | PK/FK          | FK (ordini_fornitori.id_ordine)  |
|                    | id_prodotto                | Riferimento al prodotto                                                             | INT         | PK/FK          | FK (prodotti.id_prodotto)        |
|                    | quantita_ordinata          | Quantità ordinata del prodotto                                                      | INT         | Sì             | Valore positivo                  |
|                    | prezzo_unitario_acquisto   | Prezzo unitario di acquisto del prodotto                                            | DECIMAL(10,2)| Sì             | Valore positivo                  |
| pagamenti          | id_pagamento               | Identificatore unico del pagamento                                                  | INT         | PK             | Valore unico                     |
|                    | id_scontrino               | Riferimento allo scontrino pagato                                                   | INT         | Sì             | FK (scontrini.id_scontrino)      |
|                    | metodo                     | Metodo di pagamento utilizzato                                                      | VARCHAR(20) | Sì             | "Contanti", "Carta", "Bonifico"  |
|                    | importo                    | Importo pagato                                                                      | DECIMAL(10,2)| Sì             | Valore positivo                  |
|                    | data_pagamento             | Data del pagamento                                                                  | DATE        | Sì             | Formato data (YYYY-MM-DD)        |
|                    | ora_pagamento              | Ora del pagamento                                                                   | TIME        | Sì             | Formato ora (HH:MM:SS)           |
|                    | id_cassa                   | Riferimento alla cassa utilizzata                                                   | INT         | Sì             | FK (postazioni_cassa.id_cassa)   |
