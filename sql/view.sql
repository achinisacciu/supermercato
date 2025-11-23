USE supermercato_db;

-- ==================================================================
-- 1. VISTE VENDITE E FATTURATO
-- ==================================================================

-- Vista: v_analisi_vendite_prodotto
-- Descrizione: Mostra il fatturato generato e le quantità vendute per ogni prodotto,
-- raggruppato per categoria e sottocategoria.
CREATE OR REPLACE VIEW v_analisi_vendite_prodotto AS
SELECT 
    c.nome_categoria,
    s.nome_sottocategoria,
    p.nome_prodotto,
    m.nome_marca,
    SUM(ds.quantita) AS pezzi_venduti,
    ROUND(SUM(ds.quantita * ds.prezzo_unitario), 2) AS fatturato_lordo,
    ROUND(SUM((ds.quantita * ds.prezzo_unitario) * (ds.sconto_percentuale / 100)), 2) AS totale_sconti_applicati,
    ROUND(SUM((ds.quantita * ds.prezzo_unitario) * (1 - ds.sconto_percentuale / 100)), 2) AS fatturato_netto
FROM dettagli_scontrino ds
JOIN prodotti p ON ds.id_prodotto = p.id_prodotto
JOIN marche m ON p.id_marca = m.id_marca
JOIN sottocategorie s ON p.id_sottocategoria = s.id_sottocategoria
JOIN categorie c ON s.id_categoria = c.id_categoria
JOIN documenti doc ON ds.id_documento = doc.id_documento
GROUP BY c.id_categoria, s.id_sottocategoria, p.id_prodotto, m.nome_marca;

-- Vista: v_vendite_mensili
-- Descrizione: Aggregazione temporale del fatturato per mese e anno.
CREATE OR REPLACE VIEW v_vendite_mensili AS
SELECT 
    YEAR(data_documento) AS anno,
    MONTH(data_documento) AS mese,
    COUNT(id_documento) AS numero_scontrini,
    SUM(importo) AS incasso_totale,
    ROUND(AVG(importo), 2) AS scontrino_medio
FROM documenti
WHERE tipo_documento = 'Scontrino'
GROUP BY YEAR(data_documento), MONTH(data_documento)
ORDER BY anno DESC, mese DESC;

-- ==================================================================
-- 2. VISTE GESTIONE MAGAZZINO E LOGISTICA
-- ==================================================================

-- Vista: v_giacenza_prodotti
-- Descrizione: Calcola la quantità totale fisica presente in negozio per ogni prodotto,
-- sommando le quantità dei vari lotti distribuiti sui vari scaffali.
-- Gestisce anche i prodotti con giacenza zero (LEFT JOIN).
CREATE OR REPLACE VIEW v_giacenza_prodotti AS
SELECT 
    p.id_prodotto,
    p.nome_prodotto,
    m.nome_marca,
    COALESCE(SUM(g.quantita), 0) AS quantita_totale,
    CASE 
        WHEN COALESCE(SUM(g.quantita), 0) = 0 THEN 'STOCK-OUT'
        WHEN COALESCE(SUM(g.quantita), 0) < 10 THEN 'CRITICA'
        ELSE 'NORMALE'
    END AS stato_stock
FROM prodotti p
JOIN marche m ON p.id_marca = m.id_marca
LEFT JOIN lotti l ON p.id_prodotto = l.id_prodotto
LEFT JOIN giacenze g ON l.id_lotto = g.id_lotto
GROUP BY p.id_prodotto, m.nome_marca;

-- Vista: v_prodotti_in_scadenza
-- Descrizione: Elenca i lotti specifici che scadranno nei prossimi 30 giorni
-- e indica su quale scaffale si trovano per facilitare il ritiro o lo sconto.
CREATE OR REPLACE VIEW v_prodotti_in_scadenza AS
SELECT 
    p.nome_prodotto,
    l.codice_lotto,
    l.data_scadenza,
    DATEDIFF(l.data_scadenza, CURDATE()) AS giorni_alla_scadenza,
    g.quantita AS quantita_su_scaffale,
    s.id_scaffale,
    r.nome_reparto,
    e.nome_edificio
FROM lotti l
JOIN prodotti p ON l.id_prodotto = p.id_prodotto
JOIN giacenze g ON l.id_lotto = g.id_lotto
JOIN scaffali s ON g.id_scaffale = s.id_scaffale
JOIN reparti r ON s.id_reparto = r.id_reparto
JOIN reparto_edificio re ON r.id_reparto = re.id_reparto
JOIN edifici e ON re.id_edificio = e.id_edificio
WHERE l.data_scadenza BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
ORDER BY l.data_scadenza ASC;

-- ==================================================================
-- 3. VISTE CLIENTI E CRM
-- ==================================================================

-- Vista: v_analisi_clienti_fedelta
-- Descrizione: Calcola il "Life Time Value" dei clienti registrati, 
-- l'età (Regola di Derivazione 1) e i punti fedeltà stimati (Regola 7).
CREATE OR REPLACE VIEW v_analisi_clienti_fedelta AS
SELECT 
    c.id_cliente,
    CONCAT(c.nome, ' ', c.cognome) AS nominativo,
    TIMESTAMPDIFF(YEAR, c.data_nascita, CURDATE()) AS eta,
    c.email,
    COUNT(d.id_documento) AS numero_visite,
    SUM(d.importo) AS spesa_totale_storica,
    ROUND(AVG(d.importo), 2) AS scontrino_medio,
    FLOOR(SUM(d.importo) / 10) AS punti_fedelta_stimati
FROM clienti c
JOIN documenti d ON c.id_cliente = d.id_cliente
GROUP BY c.id_cliente;

-- ==================================================================
-- 4. VISTE PERSONALE E PERFORMANCE
-- ==================================================================

-- Vista: v_performance_cassieri
-- Descrizione: Analizza il volume di lavoro gestito da ogni dipendente alle casse.
CREATE OR REPLACE VIEW v_performance_cassieri AS
SELECT 
    dip.id_dipendente,
    CONCAT(dip.nome, ' ', dip.cognome) AS cassiere,
    COUNT(doc.id_documento) AS scontrini_emessi,
    SUM(doc.importo) AS totale_incassato,
    MAX(doc.data_documento) AS ultimo_turno
FROM dipendenti dip
JOIN documenti doc ON dip.id_dipendente = doc.id_dipendente
WHERE doc.tipo_documento = 'Scontrino'
GROUP BY dip.id_dipendente;

-- Vista: v_scadenza_titoli_dipendenti
-- Descrizione: Monitora le certificazioni (es. HACCP) dei dipendenti in scadenza o scadute.
CREATE OR REPLACE VIEW v_scadenza_titoli_dipendenti AS
SELECT 
    d.id_dipendente,
    CONCAT(d.nome, ' ', d.cognome) AS dipendente,
    r.nome_ruolo,
    t.nome_titolo,
    t.data_scadenza,
    CASE 
        WHEN t.data_scadenza < CURDATE() THEN 'SCADUTO'
        WHEN t.data_scadenza BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 60 DAY) THEN 'IN SCADENZA'
        ELSE 'VALIDO'
    END AS stato_titolo
FROM dipendenti d
JOIN dipendenti_titoli dt ON d.id_dipendente = dt.id_dipendente
JOIN titoli t ON dt.id_titolo = t.id_titolo
JOIN ruoli r ON d.id_ruolo = r.id_ruolo
WHERE t.data_scadenza IS NOT NULL
AND t.data_scadenza < DATE_ADD(CURDATE(), INTERVAL 60 DAY);

-- ==================================================================
-- 5. VISTE FORNITORI
-- ==================================================================

-- Vista: v_monitoraggio_ordini_fornitori
-- Descrizione: Riepilogo dello stato degli ordini verso i fornitori.
CREATE OR REPLACE VIEW v_monitoraggio_ordini_fornitori AS
SELECT 
    f.nome_fornitore,
    o.id_ordine,
    o.data_ordine,
    o.data_prevista_consegna,
    o.stato,
    COUNT(do_det.id_dettaglio) AS numero_articoli_ordinati,
    SUM(do_det.quantita * do_det.prezzo_unitario) AS valore_ordine
FROM ordini_fornitore o
JOIN fornitori f ON o.id_fornitore = f.id_fornitore
JOIN dettagli_ordine do_det ON o.id_ordine = do_det.id_ordine
GROUP BY o.id_ordine;