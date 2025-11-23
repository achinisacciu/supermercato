# Classificazione delle Relazioni – Database Supermercato

## Tipologie di Relazione

* **1:1 (uno a uno)** → una tupla in A corrisponde a una sola tupla in B e viceversa.
* **1:N (uno a molti)** → una tupla in A può essere associata a più tuple in B.
* **N:M (molti a molti)** → molte tuple in A possono essere associate a molte in B. Richiede **tabella associativa**.

---

## Relazioni tra Entità

### Clienti

| Entità A | Entità B        | Tipo | Cardinalità | Chiave di Lettura | Tabella Associativa |
| -------- | --------------- | ---- | ----------- | ----------------- | ------------------- |
| clienti  | scontrini       | 1:N  | 1 ⟶ N       | Un cliente può avere molti scontrini | No |
| clienti  | preferenze      | N:M  | N ⟷ M       | Molti clienti possono condividere molte preferenze | clienti_preferenze |
| clienti  | titoli      | N:M  | N ⟷ M       | Molti clienti possono conseguire più titoli | clienti_titoli |

### Dipendenti

| Entità A   | Entità B | Tipo | Cardinalità | Chiave di Lettura | Tabella Associativa |
| ---------- | -------- | ---- | ----------- | ----------------- | ------------------- |
| ruoli      | dipendenti |1:N | 1 ⟶ N      | Un ruolo può essere assegnato a più dipendenti | No |
| dipendenti | ruoli    | N:1  | N ⟶ 1      | Molti dipendenti possono avere lo stesso ruolo | No |
| dipendenti | uffici   | N:1  | N ⟶ 1      | Molti dipendenti possono lavorare in un ufficio | No |
| uffici     | dipendenti   | 1:N  | 1 ⟶ N  | In un uffucio possono lavorare molti dipendenti | No |
| dipendenti | titoli   | N:M  | N ⟷ M      | Molti dipendenti possono avere molti titoli | dipendenti_titoli |

### Organizzazione Interna

| Entità A | Entità B | Tipo | Cardinalità | Chiave di Lettura | Tabella Associativa |
| -------- | -------- | ---- | ----------- | ----------------- | ------------------- |
| uffici   | edifici  | 1:N  | 1 ⟶ N      | Un ufficio può essere distribuito in più edifici | No |
| ruoli    | titoli   | N:M  | N ⟷ M      | Molti ruoli possono richiedere molti titoli | ruoli_titoli |
| reparti  | edifici  | N:M  | N ⟷ M      | Molti reparti possono essere in molti edifici | reparto_edificio |
| reparti  | scaffali | 1:N  | 1 ⟶ N      | Un reparto contiene molti scaffali | No |


### Vendite

| Entità A            | Entità B            | Tipo | Cardinalità | Chiave di Lettura | Tabella Associativa |
| ------------------- | ------------------- | ---- | ----------- | ----------------- | ------------------- |
| documenti           | dettagli_scontrino  | 1:N  | 1 ⟶ N       | Uno documento di tipo scontrino ha molti dettagli (righe) | No |
| dettagli_scontrino  | prodotti            | N:1  | N ⟶ 1       | Molti dettagli possono riferirsi allo stesso prodotto | No |
| documenti           | casse               | N:1  | N ⟶ 1       | Molti documenti di tipo scontrino vengono emessi dalla stessa cassa | No |

### Prodotti

| Entità A       | Entità B       | Tipo | Cardinalità | Chiave di Lettura | Tabella Associativa |
| -------------- | -------------- | ---- | ----------- | ----------------- | -------------------- |
| prodotti       | sottocategorie | N:1  | N ⟶ 1       | Molti prodotti appartengono alla stessa sottocategoria | No |
| sottocategorie | categorie      | N:1  | N ⟶ 1       | Molte sottocategorie appartengono alla stessa categoria | No |
| prodotti       | marche         | N:1  | N ⟶ 1       | Molti prodotti appartengono alla stessa marca | No |
| marche         | produttori     | N:1  | N ⟶ 1       | Molte marche appartengono allo stesso produttore | No |
| prodotti       | promozioni     | N:M  | N ⟷ M       | Molti prodotti possono avere molte promozioni | promozioni_prodotti |
| prodotti       | lotti          | 1:N  | 1 ⟶ N       | Un prodotto può avere diversi lotti di produzione | No |
| lotti          | scaffali       | N:M  | N ⟷ M       | Molti lotti possono essere distribuiti su molti scaffali | giacenze |

### Fornitori

| Entità A          | Entità B          | Tipo | Cardinalità | Chiave di Lettura | Tabella Associativa |
| ----------------- | ----------------- | ---- | ----------- | ----------------- | ------------------- |
| fornitori         | ordini_fornitore  | 1:N  | 1 ⟶ N       | Un fornitore può ricevere molti ordini | No |
| ordini_fornitore  | dettagli_ordine   | 1:N  | 1 ⟶ N       | Un ordine ha molti dettagli (righe) | No |
| dettagli_ordine   | prodotti          | N:1  | N ⟶ 1       | Molti dettagli possono riferirsi allo stesso prodotto | No |
| fornitori         | prodotti          | N:M  | N ⟷ M       | Molti fornitori possono fornire molti prodotti | catalogo_fornitore |

### Inventario

| Entità A   | Entità B | Tipo | Cardinalità | Chiave di Lettura | Tabella Associativa |
| ---------- | -------- | ---- | ----------- | ----------------- | ------------------- |
| inventario | prodotti | N:1  | N ⟶ 1       | Molte voci di inventario si riferiscono allo stesso prodotto | No |
| inventario | scaffali | N:1  | N ⟶ 1       | Molte voci di inventario si riferiscono allo stesso scaffale | No |
| inventario | reparti  | N:1  | N ⟶ 1       | Molte voci di inventario si riferiscono allo stesso reparto | No |
| inventario | edifici  | N:1  | N ⟶ 1       | Molte voci di inventario si riferiscono allo stesso edificio | No |

---
