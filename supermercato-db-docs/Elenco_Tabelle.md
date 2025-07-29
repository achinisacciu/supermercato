# Elenco Tabelle

##  Gestione Personale

| Nome Tabella         | Descrizione                                                                 |
|----------------------|------------------------------------------------------------------------------|
| dipendenti           | Anagrafica e dati contrattuali dei dipendenti.                              |
| ruoli                | Definizione dei ruoli aziendali (es. cassiere, magazziniere, direttore).     |
| titoli               | Certificazioni e qualifiche (es. HACCP, carrellista).                        |
| uffici               | Uffici amministrativi e operativi aziendali.                                |
| dipendenti_titoli    | **Associazione N:M** tra dipendenti e titoli posseduti.                      |
| ruoli_titoli         | **Associazione N:M** tra ruoli e titoli richiesti per svolgerli.             |

---

## Infrastruttura e Localizzazione

| Nome Tabella         | Descrizione                                                                 |
|----------------------|------------------------------------------------------------------------------|
| edifici              | Elenco edifici fisici (A, B, C) del supermercato.                           |
| reparti              | Reparti commerciali (es. ortofrutta, enoteca, drogheria...).                |
| scaffali             | Scaffali fisici e refrigerati per la collocazione dei prodotti.             |
| reparto_edificio     | **Associazione N:M** tra reparti ed edifici (es. un reparto in più edifici).|
| prodotti_scaffali    | **Associazione N:M** tra prodotti e scaffali su cui sono collocati.         |

---

## Clienti e Fidelizzazione

| Nome Tabella         | Descrizione                                                                 |
|----------------------|------------------------------------------------------------------------------|
| clienti              | Anagrafica clienti.                                                          |
| carte_fidelity       | Dati carte fedeltà associate ai clienti.                                    |
| clienti_preferenze   | **Associazione N:M** tra clienti e categorie/sottocategorie preferite.       |

---

## Gestione Prodotti

| Nome Tabella         | Descrizione                                                                 |
|----------------------|------------------------------------------------------------------------------|
| categorie            | Categorie merceologiche principali.                                          |
| sottocategorie       | Sottocategorie specifiche (es. pasta, birra, biscotti...).                   |
| prodotti             | Anagrafica prodotti (nome, codice, volume, prezzo...).                      |
| marche               | Brand commerciali dei prodotti.                                              |
| produttori           | Produttori delle marche.                                                     |

---

## Vendite e Scontrini

| Nome Tabella         | Descrizione                                                                 |
|----------------------|------------------------------------------------------------------------------|
| scontrini            | Dati principali di ogni scontrino (data, ora, cliente, dipendente, cassa...).|
| dettagli_scontrino   | **Associazione 1:N** tra scontrino e prodotti acquistati.                    |
| casse                | Postazioni fisiche di pagamento.                                             |
| pagamenti            | Dettaglio dei metodi e importi di pagamento associati agli scontrini.        |

---

##  Fornitori e Approvvigionamenti

| Nome Tabella         | Descrizione                                                                 |
|----------------------|------------------------------------------------------------------------------|
| fornitori            | Anagrafica dei fornitori.                                                    |
| ordini_fornitore     | Ordini effettuati verso i fornitori.                                         |
| dettagli_ordine      | Dettagli dei prodotti ordinati (quantità, prezzo, sconti...).                |
| offerte_fornitore    | **Associazione N:M** tra fornitori e prodotti con prezzo e validità.         |

---

## Promozioni e Marketing

| Nome Tabella         | Descrizione                                                                 |
|----------------------|------------------------------------------------------------------------------|
| promozioni           | Campagne promozionali attive con data inizio/fine e percentuale sconto.     |
| promozioni_prodotti  | **Associazione N:M** tra promozioni e prodotti coinvolti.                    |

---

## Inventario e Magazzino

| Nome Tabella         | Descrizione                                                                 |
|----------------------|------------------------------------------------------------------------------|
| inventario           | Giacenze di magazzino per prodotto, scaffale, reparto ed edificio.           |

---

## Tabelle Associazioni N:M – Riepilogo

| Nome Tabella             | Relazione                                       |
|--------------------------|-------------------------------------------------|
| dipendenti_titoli        | Dipendente ⬌ Titolo                            |
| ruoli_titoli             | Ruolo ⬌ Titolo                                 |
| reparto_edificio         | Reparto ⬌ Edificio                             |
| offerte_fornitore        | Fornitore ⬌ Prodotto (offerta con prezzo)      |
| promozioni_prodotti      | Promozione ⬌ Prodotto                          |
| prodotti_scaffali        | Prodotto ⬌ Scaffale                            |
| clienti_preferenze       | Cliente ⬌ Categoria/Sottocategoria preferita   |

> Le associazioni N:M sono normalizzate tramite tabelle ponte, spesso con attributi propri (es. data preferenza, quantità esposta, validità titolo, ecc.).

