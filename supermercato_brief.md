# 📘 Scheda del progetto – Database Supermercato

> Documento di contesto generale – versione 1.0  
> Ultimo aggiornamento: 29 luglio 2025

---

## 1. Premessa
Il presente progetto è **puramente didattico**.  
Il supermercato **“Supermercato León” non esiste** nella realtà; è stato ideato per consentire l’applicazione pratica di tecniche di **progettazione concettuale, logica e fisica di basi di dati relazionali** con **MySQL e MySQL Workbench**, nonché per l’analisi dei dati mediante query SQL e strumenti di BI.  
Tutti i nomi, i marchi e i dati contenuti sono fittizi.

---

## 2. Obiettivi formativi
- Modellare un dominio complesso con vincoli di integrità realistici.  
- Esercitarsi nella stesura di **DDL**, **DML**, **viste**, **stored procedure** e **trigger** in **MySQL 8.x**.  
- Popolare il database con dataset realistici per effettuare analisi di vendita, fidelizzazione, rotazione stock, ecc.  
- Produrre report di business (es. “Top-10 prodotti per margine”, “Clienti a rischio abbandono”).  

---

## 3. Contesto aziendale immaginario
| Voce | Valore |
|------|--------|
| Ragione sociale | **Supermercato S.r.l.** |
| Formato | Catena di **ipermercati di vicinato** |
| Sede legale | Via delle Magnolie 42, Batarnù (IT) |
| Anno di apertura | 2020 |
| Orari | 08:00 – 21:00, tutti i giorni |
| Proprietà | Famiglia León (100 %) |
| Mission | “Offrire freschezza, convenienza e servizio alle famiglie del quartiere” |

---

## 4. Infrastruttura fisica e ubicazioni

### 4.1 Complesso immobiliare
Il supermercato occupa **3 edifici** collegati da un’area pedonale e da un tunnel di servizio riservato al personale:



| Edificio | Ruolo | Superficie | Reparti / Uffici principali |
|--------|------|------------|------------------------------|
| **Edificio A** | Punto vendita secondario (specializzato) | 2.000 m² | Ortofrutta, Panetteria, Gastronomia, Macelleria, Pescheria, Latticini, Drogheria, Enoteca, Prodotti senza glutine, Casa & Igiene, Area cassa (8 casse tradizionali + 1 self-checkout) |
| **Edificio B** | **Punto vendita principale e magazzino centrale** | 3.500 m² (totale) | <br>**Area vendita**: ampliata rispetto all'Edificio A, con reparti omogenei ma più estesi<br>**Magazzino**: Ricezione merci, stoccaggio temperatura ambiente, celle frigorifere (+4 °C), celle congelate (−18 °C), area preparazione ordini online, logistica interna |
| **Edificio C** | **Sede centrale amministrativa e direzionale** | 1.200 m² | Direzione Generale, Direzione Operativa, Ufficio Commerciale, Marketing, HR, Amministrazione e Finanza, IT, Acquisti, Logistica, Qualità, Sicurezza, E-commerce, Progetti, Legale, Comunicazione |

> **Nota**: L’Edificio B è il più grande ed è il fulcro operativo dell’intero complesso, combinando **punto vendita principale** e **funzioni logistiche centrali**. L’Edificio C funge da **headquarter aziendale**, ospitando tutti gli uffici direzionali e di staff.

---

## 4.2 Distribuzione reparti e uffici

| Reparto / Ufficio | Ubicazione | Note |
|-------------------|------------|------|
| **Ortofrutta** | Edificio A, lato sud | 6 scaffali refrigerati, 2 isole display |
| **Panetteria** | Edificio A, fronte ingresso | Forno interno, 3 addetti produzione |
| **Gastronomia** | Edificio A, centro | Banco self-service + vetrine calde |
| **Macelleria** | Edificio A, retro | 1 macellaio capo-reparto + 2 addetti |
| **Pescheria** | Edificio A, angolo nord | Vasche refrigeranti, 1 specialista |
| **Latticini** | Edificio A, corsia 3 | 10 banchi frigo verticali |
| **Drogheria** | Edificio A, corsia 4-5 | 22 scaffali verticali |
| **Enoteca** | Edificio A, lato est | 1 sommelier interno |
| **Prodotti senza glutine** | Edificio A, corsia 6 | 4 scaffali dedicati |
| **Prodotti per la casa** | Edificio A, fondo negozio | 12 scaffali |
| **Area cassa (A)** | Edificio A, fronte uscita | 8 postazioni cassa tradizionali + 1 self-checkout |
| **Area vendita principale** | Edificio B | Reparti omologhi a Edificio A, ma con superficie ampliata e assortimento esteso |
| **Ricezione merci** | Edificio B, retro | Turni 6:00–14:00, 3 addetti |
| **Stoccaggio ambiente** | Edificio B | Scaffalature metalliche, controllo umidità |
| **Celle frigorifere (+4 °C)** | Edificio B | Per latticini, carne fresca, prodotti deperibili |
| **Celle congelate (−18 °C)** | Edificio B | Per surgelati e pesce congelato |
| **Preparazione ordini online** | Edificio B | Zona dedicata con picking list digitale, 2 addetti full-time |
| **Logistica interna** | Edificio B | Coordinamento trasporti e riassortimento reparti |
| **Carrelli e attrezzature** | Edificio B | Deposito attrezzi, manutenzione carrelli elevatori |
| **Direzione Generale** | Edificio C, piano 1 | CEO e staff direzionale |
| **Direzione Operativa** | Edificio C, piano 1 | Gestione attività quotidiane del punto vendita e logistica |
| **Ufficio Commerciale** | Edificio C, piano 1 | Negoziazione con fornitori, gestione contratti |
| **Ufficio Marketing** | Edificio C, piano 1 | Campagne promozionali, digital marketing, fidelizzazione |
| **Ufficio Risorse Umane (HR)** | Edificio C, piano 2 | Reclutamento, contratti, formazione, relazioni sindacali |
| **Ufficio Amministrazione e Finanza** | Edificio C, piano 2 | Bilanci, fatturazione, paghe, rapporti con commercialista |
| **Ufficio IT** | Edificio C, piano 2 | Gestione sistemi POS, rete interna, e-commerce, sicurezza informatica |
| **Ufficio Acquisti** | Edificio C, piano 2 | Selezione fornitori, ordini, controllo qualità in ingresso |
| **Ufficio Logistica** | Edificio C, piano 2 | Pianificazione trasporti, gestione magazzino centrale, ottimizzazione flussi |
| **Ufficio Qualità** | Edificio C, piano 2 | Controllo HACCP, audit interni, conformità normative |
| **Ufficio Sicurezza** | Edificio C, piano 2 | Sicurezza sui luoghi di lavoro, formazione antincendio, videosorveglianza |
| **Ufficio E-commerce** | Edificio C, piano 2 | Gestione piattaforma online, consegne a domicilio, customer care digitale |
| **Ufficio Progetti** | Edificio C, piano 2 | Innovazione, digitalizzazione, espansioni future |
| **Ufficio Legale** | Edificio C, piano 2 | Contratti, contenziosi, compliance normativa |
| **Ufficio Comunicazione** | Edificio C, piano 2 | Relazioni con i media, comunicati stampa, social media |
| **Centro-analisi dati** | Edificio C, piano 2 | 1 data analyst (stage universitario), supporto a marketing e logistica con reportistica |

---

## Note aggiuntive

- Il **tunnel di servizio** consente al personale di spostarsi tra i tre edifici senza interferire con il flusso dei clienti.
- Gli **Edifici A e B** sono aperti al pubblico, ma con una **gerarchia di servizio**: l’Edificio B è il principale, l’Edificio A funge da punto vendita satellite con offerta specializzata.
- L’**Edificio C** è **non aperto al pubblico**, accessibile solo a dipendenti e fornitori autorizzati.
- La concentrazione degli uffici direzionali in un unico edificio favorisce l’efficienza operativa e la sinergia tra le funzioni aziendali.

> Questo assetto riflette un modello organizzativo moderno, in cui **operatività, logistica e direzione** sono fisicamente separate ma strettamente integrate.

---

## 5. Organico personale (snapshot 2025)

| Area | N° dipendenti | Dettaglio ruoli |
|---|---|---|
| **Direzione** | 5 | CEO, Direttore Operativo, Direttore Commerciale, Direttore Marketing, Direttore HR |
| **Amministrazione e Finanza** | 4 | Responsabile Amministrazione e Finanza, Addetto Contabilità Fornitori, Addetto Contabilità Clienti, Addetto Paghe |
| **IT** | 3 | Responsabile IT, Sistemista, Data Analyst (stagista universitario) |
| **Acquisti** | 2 | Responsabile Acquisti, Buyer |
| **Logistica** | 4 | Responsabile Logistica, 3 Addetti Magazzino (Ricezione Merci, Stoccaggio, Preparazione Ordini Online) |
| **Qualità e Sicurezza** | 2 | Responsabile Qualità, Responsabile Sicurezza |
| **E-commerce** | 2 | Responsabile E-commerce, Addetto Customer Care Digitale |
| **Progetti** | 1 | Responsabile Progetti |
| **Legale** | 1 | Responsabile Legale |
| **Comunicazione** | 1 | Responsabile Comunicazione |
| **Personale di Vendita (Edificio A & B)** | 35 | Responsabile di Punto Vendita, 2 Capi Reparto (Ortofrutta, Panetteria/Gastronomia), 2 Macellai, 1 Specialista Pescheria, 1 Sommelier, 20 Addetti Reparto (Ortofrutta, Panetteria, Gastronomia, Latticini, Drogheria, Enoteca, Senza Glutine, Casa & Igiene), 6 Cassieri Tradizionali, 1 Addetto Self-Checkout |
| **Servizi Generali** | 3 | Addetti Pulizia, Addetti Manutenzione |
| **Totale Stimato** | **63** | |

---
---

## 6. Sistema informativo
- **DBMS**: **MySQL 8.0.x**  
- **IDE grafico**: **MySQL Workbench**   
- **Sorgenti dati**:  
  - TPV casse → inserimento real-time  
  - File CSV fornitori → import batch notturno con `LOAD DATA INFILE`

---

## 7. Note legali e privacy
- Progetto didattico: **nessun dato reale**.  
- Dataset clienti e dipendenti sono sintetici.  
- Licenza: **MIT** per uso didattico e open-source.

---

> *“Il supermercato non esiste, ma i problemi di gestione dei dati che ci alleniamo a risolvere sono reali.”*  
> — Andrea Palazzo
