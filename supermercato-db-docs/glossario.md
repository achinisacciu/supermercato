# Glossario – Progetto Database «Supermercato»

> Elenco alfabetico dei termini tecnici, di dominio o aziendali usati nel progetto.  
> Ogni definizione è scritta in linguaggio chiaro per stakeholder sia business che tecnici.

---

| Termine | Descrizione |
|---------|-------------|
| **Back-office** | Area (fisica o logica) riservata al personale amministrativo per attività di gestione non visibili al cliente (contabilità, ordini fornitori, anagrafiche). |
| **Barcode / SKU** | Codice numerico o alfanumerico stampato sul prodotto; nel DB è l’identificatore univoco di ogni articolo a livello logico (SKU = Stock Keeping Unit). |
| **Capacità scaffale** | Massimo volume (litri) e peso (kg) che uno scaffale può contenere, usato nei vincoli di riempimento. |
| **Carta Fedeltà** | Tessera personale abbinata 1-to-1 al cliente; consente raccolta punti, sconti automatici e analisi CRM. |
| **Categoria (prodotto)** | Classificazione di primo livello dell’assortimento (es. Alimentari, Igiene Casa). |
| **Cliente** | Persona fisica o giuridica che acquista nel punto vendita; può essere titolare di Carta Fedeltà oppure “cliente anonimo”. |
| **Data di scadenza prodotto** | Data entro la quale un prodotto deperibile deve essere venduto o ritirato (vincolo obbligatorio solo per prodotti alimentari). |
| **Dettaglio Scontrino** | Riga di vendita interna a uno scontrino: identifica prodotto, quantità, prezzo unitario, sconto applicato e totale riga. |
| **Dettaglio Ordine Fornitore** | Riga di acquisto interna a un ordine fornitore: prodotto, quantità ordinata, prezzo unitario d’acquisto. |
| **Dipendente** | Lavoratore interno al supermercato, dotato di anagrafica, ruolo/i e titoli professionali. |
| **Edificio** | Struttura fisica (punto vendita o magazzino) che contiene reparti, uffici e scaffali. |
| **Fornitore** | Azienda terza che approvvigiona il supermercato di prodotti; emette offerte e riceve ordini. |
| **Giacenza** | Quantità fisica di un prodotto presente a scaffale o in magazzino al momento. |
| **Marca** | Nome commerciale registrato da un produttore; serve a collegare prodotti al produttore e alla categoria. |
| **Offerta Fornitore** | Prezzo e condizioni di fornitura di un prodotto proposte da un fornitore in un periodo di tempo. |
| **Ordine Fornitore** | Documento con cui il supermercato richiede merce a un fornitore; contiene almeno un Dettaglio Ordine. |
| **Pagamento** | Versamento (contante, POS, buoni, satispay, ecc.) collegato a uno scontrino; può essere multiplo. |
| **Peso lordo / peso netto** | Attributi del prodotto utilizzati per calcolare il peso totale su scaffale e nei trasporti. |
| **Prezzo di acquisto** | Prezzo unitario pagato al fornitore per un prodotto (registrato nell’ordine e nell’offerta). |
| **Prezzo di vendita** | Prezzo al pubblico attivo al momento della vendita (può essere sovrascritto da promozioni). |
| **Produttore** | Entità che produce fisicamente il bene; può registrare una o più marche. |
| **Promozione** | Regola di sconto o premio attiva su uno o più prodotti per un periodo definito. |
| **Punti Fedeltà** | Credito numerico accumulato sulla Carta Fedeltà: 1 punto ogni 10 € di spesa (regola derivata). |
| **Reparto** | Area logica e fisica del punto vendita dedicata a una famiglia di prodotti; contiene scaffali. |
| **Reso** | Restituzione di merce da parte del cliente; deve essere gestito entro 14 giorni dallo scontrino. |
| **Ruolo (dipendente)** | Funzione operativa (cassiere, magazziniere, responsabile reparto, amministrativo). |
| **Scaffale** | Mobile fisico (o porzione di esso) che ospita fisicamente i prodotti; ha capacità di peso/volume. |
| **Scontrino** | Documento fiscale di vendita al cliente; contiene almeno un Dettaglio Scontrino e almeno un Pagamento. |
| **Sottocategoria** | Classificazione di secondo livello (figlia di Categoria) usata per raffinare l’assortimento. |
| **Stock-out** | Condizione in cui la giacenza di un prodotto scende a zero. |
| **Titolo (qualifica)** | Certificazione posseduta dal dipendente (es. HACCP, patentino muletto, diploma). |
| **Ufficio** | Ambiente fisico all’interno di un Edificio destinato a mansioni amministrative. |
| **Unità di misura** | Ettari, litri, kg, pezzi, ecc. associati al prodotto per calcoli di volume e peso. |
| **Volume unitario** | Spazio fisico occupato da una singola unità di prodotto (litri o metri cubi). |
---
