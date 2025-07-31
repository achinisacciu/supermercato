# Modello Logico Completo delle Tabelle – Database Supermercato

Questo documento contiene l'elenco completo delle tabelle da implementare nel database del supermercato, con attributi dettagliati per ciascuna tabella secondo il modello logico relazionale (3NF).

---

## Gestione Personale

### dipendenti (`id_dipendente`, `nome`, `cognome`, `data_nascita`, `email`, `telefono`, `data_assunzione`, `stipendio`, `id_ruolo`, `id_ufficio`)

### ruoli (`id_ruolo`, `nome_ruolo`, `descrizione`, `livello_autorizzazione`)

### titoli (`id_titolo`, `nome_titolo`, `ente_emittente`, `data_conseguimento`, `data_scadenza`)

### uffici (`id_ufficio`, `nome_ufficio`, `piano`, `id_edificio`)

### dipendenti\_titoli (`id_dipendente`, `id_titolo`)

### ruoli\_titoli (`id_ruolo`, `id_titolo`)

---

## Infrastruttura e Localizzazione

### edifici (`id_edificio`, `nome_edificio`, `indirizzo`, `superficie_mq`, `funzione_principale`)

### reparti (`id_reparto`, `nome_reparto`, `descrizione`)

### scaffali (`id_scaffale`, `tipo`, `capacita_peso`, `capacita_volume`, `id_reparto`)

### reparto\_edificio (`id_reparto`, `id_edificio`)

### prodotti\_scaffali (`id_prodotto`, `id_scaffale`, `quantita`, `data_collocazione`)

---

## Clienti e Fidelizzazione

### clienti (`id_cliente`, `nome`, `cognome`, `data_nascita`, `email`, `telefono`, `residenza`, `newsletter`)

### carte\_fidelity (`id_carta`, `id_cliente`, `data_iscrizione`, `livello`, `punti`)

### clienti\_preferenze (`id_cliente`, `id_sottocategoria`, `data_inserimento`)

### clienti\_titoli (`id_clienti_titoli`, `id_cliente`, `id_titoli`)

---

## Gestione Prodotti

### categorie (`id_categoria`, `nome_categoria`, `descrizione`)

### sottocategorie (`id_sottocategoria`, `nome_sottocategoria`, `id_categoria`)

### prodotti (`id_prodotto`, `nome_prodotto`, `prezzo_vendita`, `peso_kg`, `volume_cm3`, `id_marca`, `id_sottocategoria`, `scadenza`, `is_alimentare`)

### marche (`id_marca`, `nome_marca`, `id_produttore`)

### produttori (`id_produttore`, `nome_produttore`, `nazione`, `sito_web`, `telefono`)

---

## Vendite e Scontrini

### scontrini (`id_scontrino`, `data_scontrino`, `ora_scontrino`, `id_cassa`, `id_dipendente`, `id_cliente`)

### dettagli\_scontrino (`id_dettaglio`, `id_scontrino`, `id_prodotto`, `quantita`, `prezzo_unitario`, `sconto_percentuale`)

### casse (`id_cassa`, `numero_cassa`, `tipo`, `stato`, `id_edificio`)

### pagamenti (`id_pagamento`, `id_scontrino`, `metodo`, `importo`, `data_pagamento`)

---

## Fornitori e Approvvigionamenti

### fornitori (`id_fornitore`, `nome_fornitore`, `partita_iva`, `email`, `telefono`, `affidabilita`)

### ordini\_fornitore (`id_ordine`, `id_fornitore`, `data_ordine`, `data_prevista_consegna`, `stato`)

### dettagli\_ordine (`id_dettaglio`, `id_ordine`, `id_prodotto`, `quantita`, `prezzo_unitario`)

### offerte\_fornitore (`id_fornitore`, `id_prodotto`, `prezzo_offerta`, `data_inizio`, `data_fine`)

---

## Promozioni e Marketing

### promozioni (`id_promozione`, `nome`, `descrizione`, `sconto_percentuale`, `data_inizio`, `data_fine`)

### promozioni\_prodotti (`id_promozione`, `id_prodotto`)

---

