# Modello Logico Completo delle Tabelle – Database Supermercato

Questo documento contiene l'elenco completo delle tabelle da implementare nel database del supermercato, con attributi dettagliati per ciascuna tabella secondo il modello logico relazionale (3NF).


## Gestione del Personale

* **Dipendenti**(`id_dipendente` PK, nome, cognome, data\_nascita, email UNIQUE, telefono, data\_assunzione, stipendio, `id_ruolo` FK → Ruoli, `id_ufficio` FK → Uffici)
* **Ruoli**(`id_ruolo` PK, nome\_ruolo, descrizione)
* **Titoli**(`id_titolo` PK, nome\_titolo, ente\_emittente, data\_conseguimento, data\_scadenza, eqf)
* **Uffici**(`id_ufficio` PK, nome\_ufficio, piano, `id_edificio` FK → Edifici)
* **Dipendenti\_Titoli**(`id_dipendente` FK → Dipendenti, `id_titolo` FK → Titoli, PK composta)
* **Ruoli\_Titoli**(`id_ruolo` FK → Ruoli, `id_titolo` FK → Titoli, PK composta)

---

## Infrastruttura e Localizzazione

* **Edifici**(`id_edificio` PK, nome\_edificio, indirizzo, superficie\_mq, funzione\_principale)
* **Reparti**(`id_reparto` PK, nome\_reparto, descrizione)
* **Scaffali**(`id_scaffale` PK, tipo, capacita\_peso, capacita\_volume, `id_reparto` FK → Reparti)
* **Reparto\_Edificio**(`id_reparto` FK → Reparti, `id_edificio` FK → Edifici, PK composta)
* **Prodotti\_Scaffali**(`id_prodotto` FK → Prodotti, `id_scaffale` FK → Scaffali, quantita, data\_collocazione, PK composta)

---

## Clienti

* **Clienti**(`id_cliente` PK, nome, cognome, data\_nascita, sesso, lavoro, email UNIQUE, telefono UNIQUE, residenza, newsletter)
* **Clienti\_Titoli**(`id_cliente` FK → Clienti, `id_titolo` FK → Titoli, PK composta)

---

## Gestione Prodotti

* **Categorie**(`id_categoria` PK, nome\_categoria, descrizione)
* **Sottocategorie**(`id_sottocategoria` PK, nome\_sottocategoria, `id_categoria` FK → Categorie)
* **Prodotti**(`id_prodotto` PK, nome\_prodotto, prezzo\_vendita, peso\_kg, volume\_cm3, `id_marca` FK → Marche, `id_sottocategoria` FK → Sottocategorie, scadenza, is\_alimentare)
* **Marche**(`id_marca` PK, nome\_marca, `id_produttore` FK → Produttori)
* **Produttori**(`id_produttore` PK, nome\_produttore, nazione, sito\_web, telefono)

---

## Vendite

* **Documenti**(`id_documento` PK, tipo\_documento, data\_documento, ora\_documento, modalità\_pagamento, importo, `id_cassa` FK → Casse, `id_dipendente` FK → Dipendenti, `id_cliente` FK → Clienti)
* **Dettagli\_Scontrino**(`id_dettaglio` PK, `id_documento` FK → Documenti, `id_prodotto` FK → Prodotti, quantita, prezzo\_unitario, sconto\_percentuale)
* **Casse**(`id_cassa` PK, numero\_cassa, tipo, stato, `id_edificio` FK → Edifici)

---

## Fornitori e Approvvigionamenti

* **Fornitori**(`id_fornitore` PK, nome\_fornitore, partita\_iva UNIQUE, email, telefono, affidabilita)
* **Ordini\_Fornitore**(`id_ordine` PK, `id_fornitore` FK → Fornitori, data\_ordine, data\_prevista\_consegna, stato)
* **Dettagli\_Ordine**(`id_dettaglio` PK, `id_ordine` FK → Ordini\_Fornitore, `id_prodotto` FK → Prodotti, quantita, prezzo\_unitario)
* **Catalogo\_Fornitori**(`id_fornitore` FK → Fornitori, `id_prodotto` FK → Prodotti, prezzo\_offerta, data\_inizio, data\_fine, PK composta)

---

## Promozioni

* **Promozioni**(`id_promozione` PK, nome, descrizione, sconto\_percentuale, data\_inizio, data\_fine)
* **Promozioni\_Prodotti**(`id_promozione` FK → Promozioni, `id_prodotto` FK → Prodotti, PK composta)

---
