# Scelte delle Entità per il progetto "Supermercato"

## Introduzione

La progettazione di un database per un sistema di supermercato rappresenta una sfida complessa che richiede un'analisi approfondita delle molteplici interazioni che caratterizzano l'ambiente commerciale moderno. Il presente documento illustra le motivazioni strategiche e tecniche che hanno guidato la definizione delle entità del database, con l'obiettivo di creare un sistema informativo completo, scalabile e in grado di supportare efficacemente tutte le operazioni aziendali.

L'approccio progettuale adottato si basa su un'analisi sistematica dei processi aziendali, dalla gestione del personale alla logistica, dalle vendite alla fidelizzazione clienti. Ogni entità è stata concepita non solo per rispondere alle esigenze operative immediate, ma anche per garantire l'integrità referenziale, la consistenza dei dati e la scalabilità futura del sistema attraverso una struttura relazionale ottimizzata.

La complessità di un'organizzazione commerciale moderna richiede infatti un sistema informativo che possa adattarsi rapidamente ai cambiamenti del mercato, supportare l'innovazione tecnologica e fornire le basi per l'implementazione di strategie data-driven sempre più sofisticate.

## Analisi delle Entità e Motivazioni Progettuali

### Sottosistema Gestione del Personale

Il sottosistema dedicato alla gestione del personale costituisce il fondamento operativo dell'intera organizzazione. La sua progettazione riflette la necessità di creare una struttura organizzativa chiara, efficiente e conforme alle normative vigenti.

L'entità **Dipendente** rappresenta il nucleo centrale di questo sottosistema, progettata per contenere tutte le informazioni anagrafiche, contrattuali e operative necessarie per una gestione completa delle risorse umane. La tracciabilità delle operazioni eseguite da ogni dipendente risulta fondamentale non solo per questioni di sicurezza e controllo, ma anche per l'ottimizzazione dei processi operativi e la valutazione delle performance individuali.

L'entità **Ruolo** definisce con precisione le mansioni e le responsabilità all'interno dell'organizzazione, creando una struttura gerarchica e funzionale che facilita la gestione operativa quotidiana.

L'entità **Titolo** gestisce le qualifiche professionali e le certificazioni richieste per specifici ruoli, garantendo la conformità alle normative professionali e di settore. Questa entità risulta particolarmente importante per la gestione delle competenze specialistiche, come le certificazioni per la manipolazione di alimenti o le qualifiche per la gestione di sostanze pericolose. La tracciabilità delle qualifiche supporta inoltre i processi di audit interni ed esterni e facilita la pianificazione della formazione continua del personale.

L'entità **Ufficio** rappresenta le unità organizzative funzionali, distinguendo tra strutture fisiche, come l'ufficio amministrazione con una postazione dedicata, e strutture virtuali, come l'ufficio logistica che opera trasversalmente su tutti gli edifici pur mantenendo un responsabile e un team dedicato. Questa distinzione permette una gestione flessibile dell'organizzazione funzionale, supporta l'allocazione efficace dei centri di costo e facilita il coordinamento delle attività inter-dipartimentali.

### Sottosistema Infrastruttura e Logistica

L'infrastruttura fisica e logistica rappresenta l'ossatura operativa dell'organizzazione, richiedendo una modellazione accurata che rifletta la complessità spaziale e funzionale di un'azienda commerciale distribuita.

L'entità **Edificio** rappresenta le strutture fisiche dell'organizzazione, classificate in base alla loro funzione principale: punti vendita orientati al cliente finale con alta rotazione e necessità di ottimizzazione dell'esperienza d'acquisto, magazzini focalizzati sull'efficienza logistica e l'ottimizzazione degli spazi di stoccaggio, e sedi amministrative dedicate agli uffici direzionali e ai servizi centrali. Questa classificazione supporta la gestione del patrimonio immobiliare aziendale, l'ottimizzazione della distribuzione geografica e la pianificazione strategica dell'espansione territoriale.

| Tipo Edificio | Funzione Principale | Caratteristiche Operative | Metriche Chiave |
|---------------|-------------------|--------------------------|----------------|
| Punto Vendita | Vendita al dettaglio | Customer-facing, alta rotazione | Fatturato/mq, traffico clienti |
| Magazzino | Stoccaggio e logistica | Ottimizzazione spazi, gestione flussi | Rotazione stock, efficienza picking |
| Sede | Amministrazione | Uffici direzionali, servizi centrali | Costi operativi, produttività |

L'entità **Reparto** organizza l'offerta commerciale per categorie merceologiche omogenee, facilitando sia l'esperienza del cliente che l'efficienza operativa. I reparti classici come ortofrutta, elettronica, abbigliamento e prodotti per la casa richiedono gestioni specializzate per quanto riguarda conservazione, esposizione e rotazione dei prodotti. Questa organizzazione supporta l'ottimizzazione del layout del punto vendita, permette analisi dettagliate delle performance per area merceologica e facilita la personalizzazione dell'esperienza cliente attraverso strategie di merchandising mirate.

L'entità **Scaffale** gestisce la micro-localizzazione dei prodotti all'interno dei reparti, includendo anche strutture specializzate come frigoriferi e celle climatizzate. Questa granularità nella localizzazione risulta fondamentale per l'ottimizzazione del picking durante le operazioni di rifornimento, la gestione efficiente degli spazi espositivi e l'implementazione di strategie avanzate di merchandising che considerano fattori come l'altezza degli occhi, la posizione rispetto ai percorsi di traffico e la vicinanza a prodotti complementari.

L'entità **Giacenza** introduce un livello di dettaglio superiore rispetto alla semplice quantità per prodotto. Collegando i lotti agli scaffali, permette di sapere esattamente *quale* lotto si trova in *quale* posizione. Questo è cruciale per la gestione FIFO (First-In, First-Out) e per la rimozione mirata di lotti specifici (es. in caso di richiami o scadenze imminenti).

### Sottosistema Gestione Clienti

La gestione dei clienti rappresenta un elemento strategico fondamentale per il successo commerciale, richiedendo un equilibrio tra raccolta di informazioni utili e rispetto della privacy dei consumatori.

L'entità **Cliente** centralizza le informazioni sui consumatori mantenendo una notevole flessibilità nei campi opzionali, riconoscendo che le informazioni disponibili possono variare significativamente in base al canale di acquisizione, alle politiche di privacy aziendali e alle preferenze individuali dei clienti. Questa flessibilità progettuale permette di gestire efficacemente sia clienti completamente profilati che clienti occasionali, supportando al contempo lo sviluppo di strategie di marketing personalizzate e l'analisi approfondita dei comportamenti d'acquisto.

### Sottosistema Gestione Prodotti

La gestione dei prodotti richiede una struttura di classificazione gerarchica che supporti sia le operazioni quotidiane che le analisi strategiche di lungo termine.

L'entità **Categoria** fornisce la classificazione primaria dell'assortimento merceologico, creando macro-segmenti che facilitano l'organizzazione logica dell'offerta e supportano le analisi di mercato ad alto livello. Questa classificazione risulta fondamentale per lo sviluppo di strategie commerciali differenziate per categoria, l'ottimizzazione dei processi di acquisto e la gestione del pricing strategico a livello di macro-segmento.

L'entità **Sottocategoria** affina ulteriormente la classificazione merceologica, permettendo una gestione più granulare che riflette le specificità dei diversi segmenti di mercato. Questa granularità supporta analisi precise delle performance, facilita la gestione mirata delle promozioni e ottimizza il posizionamento dei prodotti nei reparti considerando fattori come stagionalità, complementarità e strategie di cross-selling.

L'entità **Prodotto** rappresenta il cuore dell'offerta commerciale, contenendo tutte le informazioni tecniche, commerciali e logistiche necessarie per una gestione completa del ciclo di vita del prodotto. Ogni prodotto deve essere tracciabile per conformità normative, supportare strategie di pricing dinamico e integrarsi efficacemente con eventuali sistemi di e-commerce o mobile commerce.

L'entità **Lotto** è stata introdotta per garantire la tracciabilità completa dei prodotti, specialmente quelli alimentari. Ogni lotto porta con sé informazioni vitali come la data di produzione e la data di scadenza. Questo permette al sistema di gestire avvisi preventivi per le scadenze, ottimizzare la rotazione delle scorte e garantire la sicurezza alimentare conformemente alle normative vigenti.

L'entità **Marca** gestisce il brand dei prodotti, permettendo analisi dettagliate delle performance per marchio e supportando lo sviluppo di strategie commerciali differenziate. La gestione delle relazioni con i brand owner, l'ottimizzazione del mix di marca e lo sviluppo di eventuali linee private label beneficiano significativamente di questa strutturazione.

L'entità **Produttore** traccia l'origine manifatturiera dei prodotti, garantendo la conformità alle crescenti normative di tracciabilità e supportando la gestione della qualità e gli eventuali recall di prodotto. Questa informazione risulta inoltre fondamentale per l'ottimizzazione della supply chain e la valutazione delle performance dei fornitori indiretti.

### Sottosistema Approvvigionamento

La gestione dell'approvvigionamento richiede un controllo preciso dei flussi di merci e delle relazioni commerciali con i fornitori.

L'entità **Fornitore** centralizza la gestione dei partner commerciali, permettendo una valutazione completa delle performance, l'ottimizzazione dei termini contrattuali e la diversificazione del rischio di approvvigionamento. Ogni fornitore viene valutato secondo criteri di affidabilità, qualità, puntualità delle consegne e competitività dei prezzi, informazioni che risultano cruciali per le decisioni strategiche di sourcing.

L'entità **Ordine** gestisce il processo di richiesta merci, garantendo la tracciabilità completa del processo di acquisto e supportando la gestione ottimale dei tempi di consegna e della pianificazione degli stock. Ogni ordine documenta non solo i prodotti richiesti ma anche i termini commerciali, le condizioni di pagamento e le specifiche logistiche.

L'entità **Dettaglio_Ordine** specifica i singoli articoli richiesti per ogni ordine, garantendo la precisione nella gestione delle quantità, la tracciabilità dei prezzi di acquisto e il supporto ai processi di controllo qualità in ingresso. Questa granularità permette inoltre la gestione efficace delle variazioni d'ordine e il calcolo preciso dei costi di approvvigionamento per singolo prodotto.

### Sottosistema Vendite e Transazioni

Il sottosistema transazionale rappresenta il punto di convergenza di tutti i processi aziendali, richiedendo particolare attenzione alla precisione e alla conformità normativa.

l’entità **Documento** come base concettuale per la gestione degli atti fiscali e commerciali.
Ogni documento contiene le informazioni comuni: identificativo, data, totale, cliente (opzionale), cassa e dipendente associato.

Lo Scontrino viene considerato una specializzazione del Documento, essendo in questa fase l’unico tipo gestito. In futuro sarà possibile introdurre altre specializzazioni (fattura, nota di credito, ecc.) senza modificare radicalmente la struttura. Uno scontrino è emesso soltanto a seguito di un pagamento e ogni pagamento è legato a un solo scontrino, così come ogni scontrino ha un solo pagamento.

L'entità **Dettaglio_Scontrino** registra ogni singolo articolo venduto associato ad uno scontrino, mantenendo il prezzo effettivo al momento della vendita e garantendo l'integrità storica dei dati anche in presenza di variazioni di listino. Questa informazione risulta cruciale per l'analisi delle vendite per prodotto, la gestione dell'inventario in tempo reale e il calcolo accurato di margini e profittabilità.

L'entità **Cassa** gestisce i punti di incasso del punto vendita, permettendo il controllo dei flussi di cassa per postazione, la gestione delle responsabilità per operatore e l'ottimizzazione dei tempi di attesa attraverso analisi dei flussi di traffico. La tracciabilità per cassa risulta inoltre fondamentale per audit interni e controlli di conformità.


| Metodo Pagamento | Commissioni Tipiche | Tempo Elaborazione | Livello Rischio Frodi | Note Operative |
|------------------|--------------------|--------------------|----------------------|----------------|
| Contanti | 0% | Immediato | Basso | Gestione fisica, controllo contraffazione |
| Carte di Debito | 0.3-0.5% | Immediato | Medio | Verifica PIN, controlli antiriciclaggio |
| Carte di Credito | 1.5-3% | 24-48h | Alto | Autorizzazioni complesse, chargeback |
| Digital Wallet | 0.5-1% | Immediato | Basso | Integrazione tecnologica, user experience |

<br>

## Conclusioni

La struttura database proposta garantisce una gestione completa e integrata di tutti i processi aziendali del supermercato, dall'operatività quotidiana alla pianificazione strategica di lungo termine. Ogni entità è stata progettata considerando non solo le esigenze operative immediate, ma anche la scalabilità futura del sistema, l'integrazione con tecnologie emergenti nel retail moderno e la capacità di adattamento a mercati in continua evoluzione.

L'architettura risultante supporta efficacemente l'implementazione di sistemi avanzati di business intelligence, piattaforme di e-commerce integrate, soluzioni di mobile commerce e strategie omnichannel sofisticate. Questa base solida posiziona l'organizzazione per competere efficacemente nel mercato retail contemporaneo, caratterizzato da una crescente digitalizzazione, aspettative dei clienti sempre più elevate e la necessità di operare con margini ottimizzati in un contesto competitivo intenso.

La flessibilità intrinseca del design permette inoltre l'evoluzione graduale del sistema, supportando l'introduzione di nuove funzionalità, l'integrazione con partner esterni e l'adozione di tecnologie innovative senza richiedere ristrutturazioni radicali dell'architettura dati esistente.

---
