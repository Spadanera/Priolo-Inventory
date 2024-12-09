import tkinter as tk
from tkinter import ttk
import json
import mysql.connector
from ollama import chat

# Configurazione del database
DB_CONFIG = {
    'user': 'user',  # Sostituisci con il tuo nome utente
    'password': 'password',  # Sostituisci con la tua password
    'host': 'localhost',
    'database': 'PrioloInventory',
    'port': 3306
}

# Modello di Ollama
OLLAMA_MODEL = 'qwen2.5-coder:7b'


def get_db_structure():
    """
    Restituisce la struttura del database in formato JSON.
    """
    db_structure = {
        "database": "PrioloInventory",
        "tables": {
        "bolle_uscita": [
            "PK_id_bolla",
            "data_uscita",
            "stato",
            "note",
            "FK_id_cantiere_destinazione",
            "conducente",
            "FK_targaMezzo"
        ],
        "cantieri": [
            "PK_id_cantiere",
            "nome",
            "nome2",
            "indirizzo",
            "ingegnere",
            "supervisore",
            "dataInizio",
            "dataFine",
            "numeroPiani",
            "numeroServizi",
            "capacitaPesoMassima"
        ],
        "dettagli_bolle_uscita": [
            "PK_id_dettaglio",
            "FK_id_bolla",
            "FK_id_prodotto",
            "quantita_uscita",
            "prezzo_totale"
        ],
        "dettagli_ordini_fornitori": [
            "PK_id_dettaglio",
            "FK_id_ordine",
            "FK_id_prodotto",
            "quantità_ordinata",
            "prezzo_totale",
            "FK_id_cantiere"
        ],
        "fornitori": [
            "PK_id_fornitore",
            "nome",
            "contatti",
            "indirizzo",
            "email",
            "codiceSDI",
            "partitaIva",
            "iban",
            "numeroTelefono",
            "annotazioni"
        ],
        "ordini_clienti": [
            "PK_id_ordini",
            "numeroFattura",
            "valore",
            "orderNumber",
            "item",
            "soNumber",
            "pos",
            "lavorazioneDescrizione",
            "FK_id_cantiere",
            "stato",
            "scadenza",
            "extra",
            "annotazioni",
            "extraDalPreventivoBool"
        ],
        "ordini_fornitori": [
            "PK_id_ordine",
            "FK_id_fornitore",
            "data_ordine",
            "stato",
            "conducenteNome"
        ],
        "preventivi": [
            "PK_id_preventivo",
            "numeroPreventivo",
            "valorePreventivo",
            "valoreExtraOpzionale",
            "scontoEffettuato",
            "FK_id_cantiere",
            "stato"
        ],
        "prodotti": [
            "PK_id_prodotto",
            "nome",
            "modello",
            "marca",
            "prezzo",
            "quantità_disponibile",
            "codice_ean",
            "codice_altro",
            "sellerOrderNumber",
            "networkNumber",
            "CustomerOrderNumber",
            "PurchaseOrderNumber",
            "EquipmentNumber",
            "ProjectNumber",
            "ExternalIdentification"
        ],
        "veicoli": [
            "PK_targa",
            "nome",
            "modello",
            "marca",
            "anno_immatricolazione",
            "colore",
            "tipo",
            "alimentazione",
            "chilometraggio",
            "nextManutenzione",
            "note"
        ]
    }
    }
    return json.dumps(db_structure, indent=4)


def translate_to_sql(user_request, db_structure):
    """
    Trasforma una richiesta in linguaggio naturale in una query SQL usando Ollama.
    """
    prompt = (
        f"in base a questa struttura:\n"
        f"{db_structure}\n\n"
        f"Trasforma la seguente richiesta in una query SQL: "
        f"'{user_request}'"
    )

    # Aggiungi il formato corretto per Ollama
    messages = [
        {"role": "system",
         "content": "Sei un assistente AI che traduce richieste in linguaggio naturale in query SQL."},
        {"role": "user", "content": prompt}
    ]

    # Richiesta di risposta dal modello
    response = chat(OLLAMA_MODEL, messages=messages)
    content = response.get('message', {}).get('content', '')

    # Estrai la query SQL dalla risposta
    start_index = content.find("```sql") + 7
    end_index = content.find("```", start_index)
    if start_index == -1 or end_index == -1:
        return "Errore: Nessuna query SQL trovata nella risposta."

    sql_query = content[start_index:end_index].strip()

    if not sql_query:
        return "Errore: Nessuna query generata. Controlla la tua richiesta o la struttura del database."

    return sql_query


def execute_query(query):
    """
    Esegue una query SQL sul database e restituisce il risultato.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(query)

        # Recupera tutti i risultati della query
        result = cursor.fetchall()

        # Chiude il cursore e la connessione
        cursor.close()
        connection.close()

        if not result:
            return "Nessun risultato trovato."

        return result
    except mysql.connector.Error as err:
        return f"Errore: {err}"


def display_results(results, frame):
    """
    Visualizza i risultati della query in una tabella Tkinter.
    """
    for widget in frame.winfo_children():
        widget.destroy()  # Pulisce la finestra dai risultati precedenti

    if isinstance(results, str):  # Gestisce eventuali errori
        result_label = tk.Label(frame, text=results)
        result_label.pack()
        return

    # Crea la tabella dinamicamente
    headers = [f"Colonna {i + 1}" for i in range(len(results[0]))]

    # Crea le intestazioni delle colonne
    for header in headers:
        header_label = tk.Label(frame, text=header, relief="solid", width=20)
        header_label.grid(row=0, column=headers.index(header))

    # Crea i dati nelle righe
    for row_index, row in enumerate(results, start=1):
        for col_index, cell in enumerate(row):
            cell_label = tk.Label(frame, text=str(cell), relief="solid", width=20)
            cell_label.grid(row=row_index, column=col_index)


def on_request_submit(user_request, db_structure, frame):
    """
    Funzione chiamata quando l'utente invia la richiesta.
    """
    sql_query = translate_to_sql(user_request, db_structure)

    if "Errore:" in sql_query:
        display_results(sql_query, frame)
    else:
        result = execute_query(sql_query)
        display_results(result, frame)


def main():
    # Inizializzazione della finestra principale Tkinter
    root = tk.Tk()
    root.title("Query SQL tramite Ollama")

    # Struttura del database (utilizzata per generare la query SQL)
    db_structure = get_db_structure()

    # Finestra per la richiesta dell'utente
    request_label = tk.Label(root, text="Scrivi la tua richiesta:")
    request_label.pack(pady=10)

    request_entry = tk.Entry(root, width=50)
    request_entry.pack(pady=10)

    # Bottone per inviare la richiesta
    submit_button = tk.Button(
        root, text="Invia richiesta",
        command=lambda: on_request_submit(request_entry.get(), db_structure, results_frame)
    )
    submit_button.pack(pady=10)

    # Finestra per i risultati della query
    results_frame = tk.Frame(root)
    results_frame.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
