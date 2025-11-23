USE supermercato_db;

-- ==================================================================
-- 1. VISTA BASE: RFM & DEMOGRAFIA
-- Recency (giorni dall'ultimo acquisto), Frequency (n. visite), Monetary (spesa totale)
-- ==================================================================
CREATE OR REPLACE VIEW v_ml_rfm_demografia AS
SELECT 
    c.id_cliente,
    -- Feature Demografiche
    TIMESTAMPDIFF(YEAR, c.data_nascita, CURDATE()) AS eta,
    CASE WHEN c.sesso = 'M' THEN 1 WHEN c.sesso = 'F' THEN 0 ELSE -1 END AS sesso_encoded, -- Encoding numerico
    COALESCE(c.lavoro, 'Non Specificato') AS professione,
    
    -- Feature RFM
    MAX(d.data_documento) AS ultima_visita,
    DATEDIFF(CURDATE(), MAX(d.data_documento)) AS recency_giorni,
    COUNT(DISTINCT d.id_documento) AS frequency_visite,
    SUM(d.importo) AS monetary_totale_spend,
    AVG(d.importo) AS scontrino_medio
FROM clienti c
LEFT JOIN documenti d ON c.id_cliente = d.id_cliente
WHERE d.tipo_documento = 'Scontrino'
GROUP BY c.id_cliente;

-- ==================================================================
-- 2. VISTA COMPORTAMENTALE: SENSIBILITÀ PREZZO E VARIETÀ
-- Quanto il cliente compra in offerta? Compra prodotti costosi o economici?
-- ==================================================================
CREATE OR REPLACE VIEW v_ml_comportamento_acquisto AS
SELECT 
    d.id_cliente,
    COUNT(ds.id_dettaglio) AS totale_articoli_acquistati,
    
    -- Sensibilità alle promozioni (Rapporto tra articoli scontati e totali)
    SUM(CASE WHEN ds.sconto_percentuale > 0 THEN 1 ELSE 0 END) / COUNT(ds.id_dettaglio) AS indice_cacciatore_offerte,
    
    -- Prezzo medio unitario (indica se compra prodotti "Premium" o "Budget")
    AVG(ds.prezzo_unitario) AS prezzo_medio_articolo,
    
    -- Varietà del carrello (Quanti prodotti unici compra rispetto al totale)
    COUNT(DISTINCT ds.id_prodotto) / COUNT(ds.id_dettaglio) AS indice_varieta,
    
    -- Fedeltà ai brand (Quante marche diverse compra)
    COUNT(DISTINCT p.id_marca) AS numero_brand_diversi
FROM documenti d
JOIN dettagli_scontrino ds ON d.id_documento = ds.id_documento
JOIN prodotti p ON ds.id_prodotto = p.id_prodotto
WHERE d.id_cliente IS NOT NULL
GROUP BY d.id_cliente;

-- ==================================================================
-- 3. VISTA ABITUDINI TEMPORALI
-- Quando preferisce comprare il cliente? (Weekend vs Settimana)
-- ==================================================================
CREATE OR REPLACE VIEW v_ml_abitudini_temporali AS
SELECT 
    id_cliente,
    -- Percentuale visite nel weekend (Sabato=7, Domenica=1 in ODBC standard, verifica settings DB)
    SUM(CASE WHEN DAYOFWEEK(data_documento) IN (1, 7) THEN 1 ELSE 0 END) / COUNT(id_documento) AS propensione_weekend,
    
    -- Fascia oraria preferita (Mattina, Pomeriggio, Sera)
    CASE 
        WHEN AVG(HOUR(ora_documento)) < 13 THEN 'Mattina'
        WHEN AVG(HOUR(ora_documento)) BETWEEN 13 AND 18 THEN 'Pomeriggio'
        ELSE 'Sera'
    END AS fascia_oraria_prevalente_label,
    AVG(HOUR(ora_documento)) AS ora_media_visita
FROM documenti
WHERE id_cliente IS NOT NULL
GROUP BY id_cliente;

-- ==================================================================
-- 4. VISTA PREFERENZE CATEGORIE (Cross-Selling)
-- Qual è la categoria merceologica preferita?
-- ==================================================================
CREATE OR REPLACE VIEW v_ml_preferenze_categoria AS
SELECT 
    d.id_cliente,
    -- Trova la categoria dove ha speso di più (Logica semplificata per vista)
    (
        SELECT cat.nome_categoria 
        FROM dettagli_scontrino ds2
        JOIN documenti d2 ON ds2.id_documento = d2.id_documento
        JOIN prodotti p2 ON ds2.id_prodotto = p2.id_prodotto
        JOIN sottocategorie s2 ON p2.id_sottocategoria = s2.id_sottocategoria
        JOIN categorie cat ON s2.id_categoria = cat.id_categoria
        WHERE d2.id_cliente = d.id_cliente
        GROUP BY cat.id_categoria
        ORDER BY SUM(ds2.quantita * ds2.prezzo_unitario) DESC
        LIMIT 1
    ) AS categoria_preferita,
    
    -- Percentuale di spesa in Alimentari (utile per distinguere famiglie da uffici/altro)
    SUM(CASE WHEN p.is_alimentare = 1 THEN (ds.quantita * ds.prezzo_unitario) ELSE 0 END) / SUM(ds.quantita * ds.prezzo_unitario) AS share_alimentare
FROM documenti d
JOIN dettagli_scontrino ds ON d.id_documento = ds.id_documento
JOIN prodotti p ON ds.id_prodotto = p.id_prodotto
WHERE d.id_cliente IS NOT NULL
GROUP BY d.id_cliente;

-- ==================================================================
-- 5. DATASET FINALE PER PYTHON (FLAT TABLE)
-- Unisce tutto in un'unica tabella pronta per pd.read_sql()
-- ==================================================================
CREATE OR REPLACE VIEW v_dataset_clustering_completo AS
SELECT 
    base.id_cliente,
    base.eta,
    base.sesso_encoded,
    base.professione,
    base.recency_giorni,
    base.frequency_visite,
    base.monetary_totale_spend,
    base.scontrino_medio,
    
    comp.indice_cacciatore_offerte,
    comp.prezzo_medio_articolo,
    comp.indice_varieta,
    
    temp.propensione_weekend,
    temp.ora_media_visita,
    
    pref.categoria_preferita,
    pref.share_alimentare

FROM v_ml_rfm_demografia base
JOIN v_ml_comportamento_acquisto comp ON base.id_cliente = comp.id_cliente
JOIN v_ml_abitudini_temporali temp ON base.id_cliente = temp.id_cliente
JOIN v_ml_preferenze_categoria pref ON base.id_cliente = pref.id_cliente;