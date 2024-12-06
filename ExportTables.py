import mysql.connector
import csv
from datetime import datetime
import os

# Credenziali di accesso al database
user = 'user'
password = 'password'

try:
    # Connessione al database MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user=user,
        password=password,
        database='PrioloInventory'
    )

    if conn.is_connected():
        print("Connessione riuscita.")

        # Creazione del cursore
        cursor = conn.cursor()

        # Esecuzione della query per ottenere tutte le tabelle nel database
        cursor.execute("SHOW TABLES")

        # Ottieni la lista di tutte le tabelle
        tables = cursor.fetchall()

        # Verifica se la cartella "backupTables" esiste, altrimenti creala
        backup_dir = 'backupTables'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            print(f"Cartella '{backup_dir}' creata.")

        # Ottieni la data corrente nel formato YYYY-MM-DD
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Crea una sottocartella con la data corrente all'interno di "backupTables"
        date_dir = os.path.join(backup_dir, current_date)
        if not os.path.exists(date_dir):
            os.makedirs(date_dir)
            print(f"Sottocartella '{date_dir}' creata.")

        for table in tables:
            table_name = table[0]
            print(f"Sto esportando {table_name}...")

            # Creazione di una query SELECT per ottenere tutti i dati dalla tabella
            select_query = f"SELECT * FROM {table_name}"

            cursor.execute(select_query)

            # Ottieni le descrizioni delle colonne
            columns = [desc[0] for desc in cursor.description]

            # Nome del file CSV per questa tabella (all'interno della sottocartella con la data corrente)
            csv_file_name = os.path.join(date_dir, f"{table_name}.csv")

            with open(csv_file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Scriviamo la riga di intestazione con i nomi delle colonne
                writer.writerow(columns)
                
                # Scriviamo le righe dei dati
                for row in cursor.fetchall():
                    writer.writerow(row)

            print(f"Dati di {table_name} esportati nel file {csv_file_name}")

except mysql.connector.Error as err:
    print(f"Errore di connessione al database: {err}")

finally:
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Connessione chiusa.")
