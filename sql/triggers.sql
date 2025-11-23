USE supermercato_db;

-- ==================================================================
-- 1. TRIGGER SULLE DATE E PROMOZIONI
-- ==================================================================

DELIMITER //

-- Trigger: check_date_promozioni
-- Vincolo 13: La data di scadenza di una promozione deve essere successiva alla data di inizio.
-- Vincolo 19: Le promozioni non devono essere attive oltre la loro data di fine (controllo logico in inserimento).
DROP TRIGGER IF EXISTS check_date_promozioni //
CREATE TRIGGER check_date_promozioni
BEFORE INSERT ON promozioni
FOR EACH ROW
BEGIN
    IF NEW.data_fine <= NEW.data_inizio THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Errore Vincolo 13: La data di fine promozione deve essere successiva alla data di inizio.';
    END IF;
END //

-- Trigger: check_data_consegna_ordini
-- Vincolo 25: La data di consegna prevista deve essere entro 30 giorni dall'ordine (se specificata).
DROP TRIGGER IF EXISTS check_data_consegna_ordini //
CREATE TRIGGER check_data_consegna_ordini
BEFORE INSERT ON ordini_fornitore
FOR EACH ROW
BEGIN
    IF NEW.data_prevista_consegna IS NOT NULL THEN
        IF NEW.data_prevista_consegna < NEW.data_ordine OR NEW.data_prevista_consegna > DATE_ADD(NEW.data_ordine, INTERVAL 30 DAY) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Errore Vincolo 25: La data di consegna deve essere successiva alla data ordine ed entro 30 giorni.';
        END IF;
    END IF;
END //

-- ==================================================================
-- 2. TRIGGER SUI PRODOTTI E LOTTI
-- ==================================================================

-- Trigger: check_scadenza_alimentari
-- Vincolo 14: Un prodotto alimentare deve avere una data di scadenza registrata nel lotto.
DROP TRIGGER IF EXISTS check_scadenza_alimentari //
CREATE TRIGGER check_scadenza_alimentari
BEFORE INSERT ON lotti
FOR EACH ROW
BEGIN
    DECLARE v_is_alimentare TINYINT;
    
    -- Recupera il flag is_alimentare dal prodotto
    SELECT is_alimentare INTO v_is_alimentare
    FROM prodotti
    WHERE id_prodotto = NEW.id_prodotto;
    
    -- Se è alimentare e la data scadenza è NULL, blocca l'inserimento
    IF v_is_alimentare = 1 AND NEW.data_scadenza IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Errore Vincolo 14: I prodotti alimentari devono avere una data di scadenza nel lotto.';
    END IF;
END //

-- ==================================================================
-- 3. TRIGGER SULLA LOGISTICA (SCAFFALI E GIACENZE)
-- ==================================================================

-- Trigger: check_capacita_scaffale
-- Vincolo 5: Ogni prodotto deve essere collocato su uno scaffale solo se c'è spazio sufficiente in volume.
-- Vincolo 15: Il peso su scaffale non deve superare la capacità dello scaffale assegnato.
DROP TRIGGER IF EXISTS check_capacita_scaffale_insert //
CREATE TRIGGER check_capacita_scaffale_insert
BEFORE INSERT ON giacenze
FOR EACH ROW
BEGIN
    DECLARE v_peso_unitario DECIMAL(10,2);
    DECLARE v_volume_unitario INT;
    DECLARE v_cap_peso_scaffale DECIMAL(10,2);
    DECLARE v_cap_vol_scaffale DECIMAL(10,2);
    DECLARE v_peso_attuale DECIMAL(10,2);
    DECLARE v_volume_attuale DECIMAL(10,2);
    
    -- Recupera info prodotto
    SELECT p.peso_kg, p.volume_cm3 
    INTO v_peso_unitario, v_volume_unitario
    FROM lotti l
    JOIN prodotti p ON l.id_prodotto = p.id_prodotto
    WHERE l.id_lotto = NEW.id_lotto;
    
    -- Recupera capacità scaffale
    SELECT capacita_peso, capacita_volume 
    INTO v_cap_peso_scaffale, v_cap_vol_scaffale
    FROM scaffali
    WHERE id_scaffale = NEW.id_scaffale;
    
    -- Calcola peso e volume ATTUALI sullo scaffale (escludendo la riga che stiamo inserendo)
    SELECT 
        COALESCE(SUM(g.quantita * p.peso_kg), 0),
        COALESCE(SUM(g.quantita * p.volume_cm3), 0)
    INTO v_peso_attuale, v_volume_attuale
    FROM giacenze g
    JOIN lotti l ON g.id_lotto = l.id_lotto
    JOIN prodotti p ON l.id_prodotto = p.id_prodotto
    WHERE g.id_scaffale = NEW.id_scaffale;
    
    -- Verifica superamento limiti (Attuale + Nuovo > Capacità)
    IF (v_peso_attuale + (NEW.quantita * v_peso_unitario)) > v_cap_peso_scaffale THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Errore Vincolo 15: Capacità di PESO dello scaffale superata.';
    END IF;

    IF (v_volume_attuale + (NEW.quantita * v_volume_unitario)) > (v_cap_vol_scaffale * 1000) THEN -- Conv litri in cm3 se necessario o viceversa
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Errore Vincolo 5: Capacità di VOLUME dello scaffale superata.';
    END IF;
END //

-- ==================================================================
-- 4. TRIGGER SU VENDITE E SCONTRINI
-- ==================================================================

-- Trigger: update_totale_scontrino_insert
-- Regola Derivazione 5: Il totale complessivo è la somma dei dettagli.
-- Automatizza l'aggiornamento dell'intestazione scontrino quando si aggiunge una riga.
DROP TRIGGER IF EXISTS update_totale_scontrino_insert //
CREATE TRIGGER update_totale_scontrino_insert
AFTER INSERT ON dettagli_scontrino
FOR EACH ROW
BEGIN
    DECLARE v_totale_riga DECIMAL(10,2);
    
    -- Calcolo totale netto della riga inserita (Regola Derivazione 4)
    SET v_totale_riga = (NEW.quantita * NEW.prezzo_unitario) * (1 - (NEW.sconto_percentuale / 100));
    
    -- Aggiorna il totale nel documento padre
    UPDATE documenti 
    SET importo = importo + v_totale_riga
    WHERE id_documento = NEW.id_documento;
END //

-- Trigger: update_totale_scontrino_delete
-- Gestisce il caso di storno riga scontrino (aggiorna il totale sottraendo).
DROP TRIGGER IF EXISTS update_totale_scontrino_delete //
CREATE TRIGGER update_totale_scontrino_delete
AFTER DELETE ON dettagli_scontrino
FOR EACH ROW
BEGIN
    DECLARE v_totale_riga DECIMAL(10,2);
    
    SET v_totale_riga = (OLD.quantita * OLD.prezzo_unitario) * (1 - (OLD.sconto_percentuale / 100));
    
    UPDATE documenti 
    SET importo = importo - v_totale_riga
    WHERE id_documento = OLD.id_documento;
END //

-- Trigger: check_validita_prezzo_vendita
-- Vincolo 28: Il prezzo di vendita deve superare il prezzo unitario d'acquisto (controllo semplificato rispetto all'ultimo ordine).
-- Nota: Questo è un controllo di business "soft", qui implementato come warning o blocco a seconda delle policy.
DROP TRIGGER IF EXISTS check_validita_prezzo_vendita //
CREATE TRIGGER check_validita_prezzo_vendita
BEFORE INSERT ON dettagli_scontrino
FOR EACH ROW
BEGIN
    DECLARE v_prezzo_vendita_attuale DECIMAL(10,2);
    
    -- Controllo che il prezzo nello scontrino non sia zero o negativo
    IF NEW.prezzo_unitario <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Errore: Il prezzo di vendita non può essere zero o negativo.';
    END IF;
END //

-- ==================================================================
-- 5. TRIGGER SUL PERSONALE
-- ==================================================================

-- Trigger: check_eta_dipendente
-- Vincolo 29: Ogni dipendente deve essere maggiorenne.
DROP TRIGGER IF EXISTS check_eta_dipendente //
CREATE TRIGGER check_eta_dipendente
BEFORE INSERT ON dipendenti
FOR EACH ROW
BEGIN
    IF TIMESTAMPDIFF(YEAR, NEW.data_nascita, CURDATE()) < 18 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Errore Vincolo 29: Il dipendente deve essere maggiorenne.';
    END IF;
END //

-- Trigger: check_titolo_obbligatorio
-- Vincolo 4: Un dipendente non può lavorare senza un titolo valido se richiesto dal suo ruolo.
-- Nota: Questo trigger controlla se il dipendente ha i titoli richiesti al momento dell'assegnazione del ruolo (Update).
DROP TRIGGER IF EXISTS check_titolo_obbligatorio //
CREATE TRIGGER check_titolo_obbligatorio
AFTER UPDATE ON dipendenti
FOR EACH ROW
BEGIN
    DECLARE v_titoli_richiesti INT;
    DECLARE v_titoli_posseduti INT;

    -- Se cambia il ruolo
    IF OLD.id_ruolo != NEW.id_ruolo THEN
        -- Conta quanti titoli sono obbligatori per il nuovo ruolo
        SELECT COUNT(*) INTO v_titoli_richiesti
        FROM ruoli_titoli
        WHERE id_ruolo = NEW.id_ruolo;

        -- Se ci sono requisiti, controlla se il dipendente li possiede
        IF v_titoli_richiesti > 0 THEN
            SELECT COUNT(*) INTO v_titoli_posseduti
            FROM dipendenti_titoli dt
            JOIN ruoli_titoli rt ON dt.id_titolo = rt.id_titolo
            WHERE dt.id_dipendente = NEW.id_dipendente
            AND rt.id_ruolo = NEW.id_ruolo;

            IF v_titoli_posseduti < v_titoli_richiesti THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Errore Vincolo 4: Il dipendente non possiede tutti i titoli obbligatori per questo ruolo.';
            END IF;
        END IF;
    END IF;
END //

DELIMITER ;