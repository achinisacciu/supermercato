-- Creazione del Database
CREATE DATABASE IF NOT EXISTS supermercato_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE supermercato_db;

-- Disabilita temporaneamente i controlli sulle chiavi esterne per evitare errori durante la creazione in blocco
SET FOREIGN_KEY_CHECKS = 0;

-- ==================================================================
-- SEZIONE 1: INFRASTRUTTURA E LOCALIZZAZIONE
-- ==================================================================

-- Tabella: edifici
CREATE TABLE IF NOT EXISTS edifici (
    id_edificio INT AUTO_INCREMENT PRIMARY KEY,
    nome_edificio VARCHAR(100) NOT NULL,
    indirizzo VARCHAR(255),
    superficie_mq INT,
    funzione_principale ENUM('Punto Vendita', 'Magazzino', 'Sede') NOT NULL
);

-- Tabella: uffici
CREATE TABLE IF NOT EXISTS uffici (
    id_ufficio INT AUTO_INCREMENT PRIMARY KEY,
    nome_ufficio VARCHAR(100) NOT NULL,
    piano INT,
    id_edificio INT NOT NULL,
    FOREIGN KEY (id_edificio) REFERENCES edifici(id_edificio) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Tabella: reparti
CREATE TABLE IF NOT EXISTS reparti (
    id_reparto INT AUTO_INCREMENT PRIMARY KEY,
    nome_reparto VARCHAR(100) NOT NULL,
    descrizione TEXT
);

-- Tabella: reparto_edificio (Relazione N:M)
CREATE TABLE IF NOT EXISTS reparto_edificio (
    id_reparto INT NOT NULL,
    id_edificio INT NOT NULL,
    PRIMARY KEY (id_reparto, id_edificio),
    FOREIGN KEY (id_reparto) REFERENCES reparti(id_reparto) ON DELETE CASCADE,
    FOREIGN KEY (id_edificio) REFERENCES edifici(id_edificio) ON DELETE CASCADE
);

-- Tabella: scaffali
CREATE TABLE IF NOT EXISTS scaffali (
    id_scaffale INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('Normale', 'Frigorifero', 'Congelatore') NOT NULL,
    capacita_peso DECIMAL(10,2) NOT NULL COMMENT 'Capacità in Kg',
    capacita_volume DECIMAL(10,2) NOT NULL COMMENT 'Capacità in Litri/m3',
    id_reparto INT NOT NULL,
    FOREIGN KEY (id_reparto) REFERENCES reparti(id_reparto) ON DELETE RESTRICT
);

-- Tabella: casse
CREATE TABLE IF NOT EXISTS casse (
    id_cassa INT AUTO_INCREMENT PRIMARY KEY,
    numero_cassa INT NOT NULL,
    tipo ENUM('Manuale', 'Automatica') NOT NULL,
    stato ENUM('Attiva', 'In manutenzione', 'Disattivata') DEFAULT 'Attiva',
    id_edificio INT NOT NULL,
    FOREIGN KEY (id_edificio) REFERENCES edifici(id_edificio) ON DELETE RESTRICT
);

-- ==================================================================
-- SEZIONE 2: GESTIONE PERSONALE
-- ==================================================================

-- Tabella: ruoli
CREATE TABLE IF NOT EXISTS ruoli (
    id_ruolo INT AUTO_INCREMENT PRIMARY KEY,
    nome_ruolo VARCHAR(100) NOT NULL,
    descrizione TEXT,
    livello_autorizzazione INT DEFAULT 1
);

-- Tabella: titoli (Qualifiche e studi)
CREATE TABLE IF NOT EXISTS titoli (
    id_titolo INT AUTO_INCREMENT PRIMARY KEY,
    nome_titolo VARCHAR(100) NOT NULL,
    ente_emittente VARCHAR(100),
    data_conseguimento DATE,
    data_scadenza DATE,
    eqf INT COMMENT 'Livello European Qualifications Framework'
);

-- Tabella: dipendenti
CREATE TABLE IF NOT EXISTS dipendenti (
    id_dipendente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cognome VARCHAR(100) NOT NULL,
    data_nascita DATE NOT NULL,
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(20),
    data_assunzione DATE NOT NULL,
    stipendio DECIMAL(10,2),
    id_ruolo INT NOT NULL,
    id_ufficio INT NOT NULL,
    FOREIGN KEY (id_ruolo) REFERENCES ruoli(id_ruolo) ON DELETE RESTRICT,
    FOREIGN KEY (id_ufficio) REFERENCES uffici(id_ufficio) ON DELETE RESTRICT
);

-- Tabella: dipendenti_titoli (Relazione N:M)
CREATE TABLE IF NOT EXISTS dipendenti_titoli (
    id_dipendente INT NOT NULL,
    id_titolo INT NOT NULL,
    PRIMARY KEY (id_dipendente, id_titolo),
    FOREIGN KEY (id_dipendente) REFERENCES dipendenti(id_dipendente) ON DELETE CASCADE,
    FOREIGN KEY (id_titolo) REFERENCES titoli(id_titolo) ON DELETE CASCADE
);

-- Tabella: ruoli_titoli (Relazione N:M - Requisiti per ruolo)
CREATE TABLE IF NOT EXISTS ruoli_titoli (
    id_ruolo INT NOT NULL,
    id_titolo INT NOT NULL,
    PRIMARY KEY (id_ruolo, id_titolo),
    FOREIGN KEY (id_ruolo) REFERENCES ruoli(id_ruolo) ON DELETE CASCADE,
    FOREIGN KEY (id_titolo) REFERENCES titoli(id_titolo) ON DELETE CASCADE
);

-- ==================================================================
-- SEZIONE 3: CLIENTI
-- ==================================================================

-- Tabella: clienti
CREATE TABLE IF NOT EXISTS clienti (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cognome VARCHAR(100) NOT NULL,
    data_nascita DATE NOT NULL,
    sesso ENUM('M', 'F', 'Altro') DEFAULT NULL,
    lavoro VARCHAR(150),
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(20) UNIQUE,
    residenza VARCHAR(255),
    newsletter TINYINT(1) DEFAULT 0
);

-- Tabella: clienti_titoli (Relazione N:M)
CREATE TABLE IF NOT EXISTS clienti_titoli (
    id_cliente INT NOT NULL,
    id_titolo INT NOT NULL,
    PRIMARY KEY (id_cliente, id_titolo),
    FOREIGN KEY (id_cliente) REFERENCES clienti(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_titolo) REFERENCES titoli(id_titolo) ON DELETE CASCADE
);

-- ==================================================================
-- SEZIONE 4: GESTIONE PRODOTTI
-- ==================================================================

-- Tabella: categorie
CREATE TABLE IF NOT EXISTS categorie (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome_categoria VARCHAR(100) NOT NULL,
    descrizione TEXT
);

-- Tabella: sottocategorie
CREATE TABLE IF NOT EXISTS sottocategorie (
    id_sottocategoria INT AUTO_INCREMENT PRIMARY KEY,
    nome_sottocategoria VARCHAR(100) NOT NULL,
    id_categoria INT NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorie(id_categoria) ON DELETE CASCADE
);

-- Tabella: produttori
CREATE TABLE IF NOT EXISTS produttori (
    id_produttore INT AUTO_INCREMENT PRIMARY KEY,
    nome_produttore VARCHAR(100) NOT NULL,
    nazione VARCHAR(50),
    sito_web VARCHAR(150),
    telefono VARCHAR(20)
);

-- Tabella: marche
CREATE TABLE IF NOT EXISTS marche (
    id_marca INT AUTO_INCREMENT PRIMARY KEY,
    nome_marca VARCHAR(100) NOT NULL,
    id_produttore INT NOT NULL,
    FOREIGN KEY (id_produttore) REFERENCES produttori(id_produttore) ON DELETE RESTRICT
);

-- Tabella: prodotti
CREATE TABLE IF NOT EXISTS prodotti (
    id_prodotto INT AUTO_INCREMENT PRIMARY KEY,
    nome_prodotto VARCHAR(150) NOT NULL,
    prezzo_vendita DECIMAL(10,2) NOT NULL,
    peso_kg DECIMAL(6,3),
    volume_cm3 INT,
    id_marca INT NOT NULL,
    id_sottocategoria INT NOT NULL,
    scadenza DATE,
    is_alimentare TINYINT(1) DEFAULT 1,
    FOREIGN KEY (id_marca) REFERENCES marche(id_marca) ON DELETE RESTRICT,
    FOREIGN KEY (id_sottocategoria) REFERENCES sottocategorie(id_sottocategoria) ON DELETE RESTRICT
);

-- Tabella: lotti
CREATE TABLE IF NOT EXISTS lotti (
    id_lotto INT AUTO_INCREMENT PRIMARY KEY,
    codice_lotto VARCHAR(50) NOT NULL,
    id_prodotto INT NOT NULL,
    data_produzione DATE,
    data_scadenza DATE,
    UNIQUE (codice_lotto, id_prodotto), -- Un codice lotto è univoco per prodotto
    FOREIGN KEY (id_prodotto) REFERENCES prodotti(id_prodotto) ON DELETE RESTRICT
);

-- Tabella: giacenze (Prodotti sugli scaffali)
CREATE TABLE IF NOT EXISTS giacenze (
    id_giacenza INT AUTO_INCREMENT PRIMARY KEY,
    id_lotto INT NOT NULL,
    id_scaffale INT NOT NULL,
    quantita INT NOT NULL,
    data_collocazione DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_lotto) REFERENCES lotti(id_lotto) ON DELETE RESTRICT,
    FOREIGN KEY (id_scaffale) REFERENCES scaffali(id_scaffale) ON DELETE RESTRICT
);

-- ==================================================================
-- SEZIONE 5: FORNITORI E APPROVVIGIONAMENTI
-- ==================================================================

-- Tabella: fornitori
CREATE TABLE IF NOT EXISTS fornitori (
    id_fornitore INT AUTO_INCREMENT PRIMARY KEY,
    nome_fornitore VARCHAR(100) NOT NULL,
    partita_iva VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(150),
    telefono VARCHAR(20),
    affidabilita TINYINT COMMENT 'Scala 1-10 o 1-5'
);

-- Tabella: ordini_fornitore
CREATE TABLE IF NOT EXISTS ordini_fornitore (
    id_ordine INT AUTO_INCREMENT PRIMARY KEY,
    id_fornitore INT NOT NULL,
    data_ordine DATE NOT NULL,
    data_prevista_consegna DATE,
    stato ENUM('In attesa', 'Consegnato', 'Annullato') DEFAULT 'In attesa',
    FOREIGN KEY (id_fornitore) REFERENCES fornitori(id_fornitore) ON DELETE RESTRICT
);

-- Tabella: dettagli_ordine
CREATE TABLE IF NOT EXISTS dettagli_ordine (
    id_dettaglio INT AUTO_INCREMENT PRIMARY KEY,
    id_ordine INT NOT NULL,
    id_prodotto INT NOT NULL,
    quantita INT NOT NULL CHECK (quantita > 0),
    prezzo_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_ordine) REFERENCES ordini_fornitore(id_ordine) ON DELETE CASCADE,
    FOREIGN KEY (id_prodotto) REFERENCES prodotti(id_prodotto) ON DELETE RESTRICT
);

-- Tabella: catalogo_fornitori (Offerte)
CREATE TABLE IF NOT EXISTS catalogo_fornitori (
    id_fornitore INT NOT NULL,
    id_prodotto INT NOT NULL,
    prezzo_offerta DECIMAL(10,2) NOT NULL,
    data_inizio DATE NOT NULL,
    data_fine DATE NOT NULL,
    PRIMARY KEY (id_fornitore, id_prodotto),
    FOREIGN KEY (id_fornitore) REFERENCES fornitori(id_fornitore) ON DELETE CASCADE,
    FOREIGN KEY (id_prodotto) REFERENCES prodotti(id_prodotto) ON DELETE CASCADE,
    CHECK (data_fine >= data_inizio)
);

-- ==================================================================
-- SEZIONE 6: PROMOZIONI E MARKETING
-- ==================================================================

-- Tabella: promozioni
CREATE TABLE IF NOT EXISTS promozioni (
    id_promozione INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descrizione TEXT,
    sconto_percentuale DECIMAL(5,2),
    data_inizio DATE NOT NULL,
    data_fine DATE NOT NULL,
    CHECK (data_fine >= data_inizio)
);

-- Tabella: promozioni_prodotti (Relazione N:M)
CREATE TABLE IF NOT EXISTS promozioni_prodotti (
    id_promozione INT NOT NULL,
    id_prodotto INT NOT NULL,
    PRIMARY KEY (id_promozione, id_prodotto),
    FOREIGN KEY (id_promozione) REFERENCES promozioni(id_promozione) ON DELETE CASCADE,
    FOREIGN KEY (id_prodotto) REFERENCES prodotti(id_prodotto) ON DELETE CASCADE
);

-- ==================================================================
-- SEZIONE 7: VENDITE (DOCUMENTI)
-- ==================================================================

-- Tabella: documenti (Scontrini e Fatture)
CREATE TABLE IF NOT EXISTS documenti (
    id_documento INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento ENUM('Scontrino', 'Fattura') NOT NULL,
    data_documento DATE NOT NULL,
    ora_documento TIME NOT NULL,
    modalità_pagamento ENUM('Contanti', 'Carta di Credito', 'Carta di Debito', 'Digital Wallet') NOT NULL,
    importo DECIMAL(10,2) NOT NULL,
    id_cassa INT NOT NULL,
    id_dipendente INT NOT NULL,
    id_cliente INT DEFAULT NULL, -- Opzionale (cliente anonimo)
    FOREIGN KEY (id_cassa) REFERENCES casse(id_cassa) ON DELETE RESTRICT,
    FOREIGN KEY (id_dipendente) REFERENCES dipendenti(id_dipendente) ON DELETE RESTRICT,
    FOREIGN KEY (id_cliente) REFERENCES clienti(id_cliente) ON DELETE SET NULL
);

-- Tabella: dettagli_scontrino
CREATE TABLE IF NOT EXISTS dettagli_scontrino (
    id_dettaglio INT AUTO_INCREMENT PRIMARY KEY,
    id_documento INT NOT NULL,
    id_prodotto INT NOT NULL,
    quantita INT NOT NULL CHECK (quantita > 0),
    prezzo_unitario DECIMAL(10,2) NOT NULL,
    sconto_percentuale DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (id_documento) REFERENCES documenti(id_documento) ON DELETE CASCADE,
    FOREIGN KEY (id_prodotto) REFERENCES prodotti(id_prodotto) ON DELETE RESTRICT
);

-- Riabilita i controlli sulle chiavi esterne
SET FOREIGN_KEY_CHECKS = 1;