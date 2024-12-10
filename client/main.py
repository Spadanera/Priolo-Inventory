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
OLLAMA_MODEL = 'qwen2.5-coder:latest'


def get_db_structure():
    """
    Restituisce la struttura del database in formato JSON.
    """
    db_structure = {
        "database": "PrioloInventory",
        "tables": {
            "bolle_uscita": {
                "columns": {
                    "PK_id_bolla": "bigint",
                    "data_uscita": "date",
                    "stato": "varchar(50)",
                    "note": "text",
                    "FK_id_cantiere_destinazione": "bigint",
                    "conducente": "varchar(255)",
                    "FK_targaMezzo": "varchar(255)"
                },
                "relations": {
                    "FK_id_cantiere_destinazione": "cantieri.PK_id_cantiere",
                    "FK_targaMezzo": "veicoli.PK_targa"
                }
            },
            "cantieri": {
                "columns": {
                    "PK_id_cantiere": "bigint",
                    "nome": "varchar(255)",
                    "nome2": "varchar(255)",
                    "indirizzo": "varchar(255)",
                    "ingegnere": "varchar(255)",
                    "supervisore": "varchar(255)",
                    "dataInizio": "date",
                    "dataFine": "date",
                    "numeroPiani": "int",
                    "numeroServizi": "int",
                    "capacitaPesoMassima": "bigint"
                },
                "relations": {}
            },
            "dettagli_bolle_uscita": {
                "columns": {
                    "PK_id_dettaglio": "bigint",
                    "FK_id_bolla": "bigint",
                    "FK_id_prodotto": "bigint",
                    "quantita_uscita": "bigint",
                    "prezzo_totale": "decimal(10,2)"
                },
                "relations": {
                    "FK_id_bolla": "bolle_uscita.PK_id_bolla",
                    "FK_id_prodotto": "prodotti.PK_id_prodotto"
                }
            },
            "prodotti": {
                "columns": {
                    "PK_id_prodotto": "bigint",
                    "nome": "varchar(100)",
                    "modello": "varchar(255)",
                    "marca": "varchar(255)",
                    "prezzo": "decimal(10,2)",
                    "quantita_disponibile": "bigint",
                    "codice_ean": "varchar(255)",
                    "codice_altro": "varchar(255)",
                    "sellerOrderNumber": "varchar(255)",
                    "CustomerOrderNumber": "varchar(255)",
                    "EquipmentNumber": "varchar(255)",
                    "ProjectNumber": "varchar(255)",
                    "ExternalIdentification": "varchar(255)"
                },
                "relations": {}
            },
            "veicoli": {
                "columns": {
                    "PK_targa": "varchar(20)",
                    "nome": "varchar(100)",
                    "modello": "varchar(100)",
                    "marca": "varchar(100)",
                    "anno_immatricolazione": "year",
                    "colore": "varchar(50)",
                    "alimentazione": "varchar(50)",
                    "cilindrata": "int",
                    "inManutenzione": "boolean",
                    "note": "text"
                },
                "relations": {}
            },
            "ordini_fornitori": {
                "columns": {
                    "PK_id_ordine": "bigint",
                    "FK_id_fornitore": "bigint",
                    "data_ordine": "date",
                    "stato": "varchar(50)",
                    "conducenteNome": "varchar(255)"
                },
                "relations": {
                    "FK_id_fornitore": "fornitori.PK_id_fornitore"
                }
            },
            "fornitori": {
                "columns": {
                    "PK_id_fornitore": "bigint",
                    "nome": "varchar(100)",
                    "contatti": "varchar(255)",
                    "indirizzo": "varchar(255)",
                    "codiceSDI": "varchar(255)",
                    "partitaIVA": "varchar(255)",
                    "iban": "varchar(255)",
                    "numeroTelefono": "varchar(255)",
                    "annotazioni": "text"
                },
                "relations": {}
            },
            "dettagli_ordini_fornitori": {
                "columns": {
                    "PK_id_dettaglio": "bigint",
                    "FK_id_ordine": "bigint",
                    "FK_id_prodotto": "bigint",
                    "quantità_ordinata": "bigint",
                    "prezzo_totale": "decimal(10,2)",
                    "FK_id_cantiere": "bigint"
                },
                "relations": {
                    "FK_id_ordine": "ordini_fornitori.PK_id_ordine",
                    "FK_id_prodotto": "prodotti.PK_id_prodotto",
                    "FK_id_cantiere": "cantieri.PK_id_cantiere"
                }
            },
            "ordini_clienti": {
                "columns": {
                    "PK_id_ordini": "bigint",
                    "numeroFattura": "varchar(255)",
                    "valore": "decimal(10,2)",
                    "orderNumber": "varchar(255)",
                    "item": "bigint",
                    "soNumber": "varchar(255)",
                    "ordineDescrizione": "varchar(255)",
                    "FK_id_cantiere": "bigint",
                    "stato": "varchar(255)",
                    "scadenza": "date",
                    "annotazioni": "text",
                    "extraDalPreventivoBool": "bit(1)"
                },
                "relations": {
                    "FK_id_cantiere": "cantieri.PK_id_cantiere"
                }
            },
            "preventivi": {
                "columns": {
                    "PK_id_preventivo": "bigint",
                    "numeroPreventivo": "varchar(255)",
                    "valorePreventivo": "decimal(10,2)",
                    "valoreExtraOpzionale": "decimal(10,2)",
                    "scontoEffettuato": "decimal(10,2)",
                    "FK_id_cantiere": "bigint",
                    "stato": "varchar(255)"
                },
                "relations": {
                    "FK_id_cantiere": "cantieri.PK_id_cantiere"
                }
            }
        }
    }
    return json.dumps(db_structure, indent=4)


def translate_to_sql(user_request, db_structure):
    """
    Trasforma una richiesta in linguaggio naturale in una query SQL usando Ollama.
    """
    prompt = (
        f"Trasforma la seguente richiesta in una query SQL: "
        f"'{user_request}'"
    )

    # Aggiungi il formato corretto per Ollama
    messages = [
        {"role": "system",
         "content": f"Sei un assistente AI che traduce richieste in linguaggio naturale in query mySQL. Questa è la struttura del Database mySQL con il quale comunicare: {db_structure}"},
        {"role": "user", "content": prompt}
    ]


    print(messages)

    # Richiesta di risposta dal modello
    response = chat(OLLAMA_MODEL, messages=messages)
    content = response.get('message', {}).get('content', '')

    print(response)
    print(messages)

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
