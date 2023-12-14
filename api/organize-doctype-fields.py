import requests
import csv
from datetime import datetime
from config import API_KEY, api_url
from config_documenttypes import document_type_config

# Liste der zu verarbeitenden Dokumenttypen
# Aktualisieren Sie diese Liste je nach Bedarf
#document_types_to_process = ["Demo", "Anderes", "Angebot", "Gehaltsabrechnung", "Information", "Kassenzettel", "Rechnung", "Kontoauszug", "Mitgliedsausweis", "Vertrag"]
document_types_to_process = ["Demo"]#, "Anderes", "Angebot", "Gehaltsabrechnung", "Information", "Kassenzettel", "Rechnung", "Kontoauszug", "Mitgliedsausweis", "Vertrag"]

# Erstellen eines eindeutigen Dateinamens mit Zeitstempel
csv_filename = f'removed_fields_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

headers = {'Authorization': f'Token {API_KEY}'}

def get_custom_fields_mapping():
    response = requests.get(f'{api_url}/custom_fields/', headers=headers)
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der benutzerdefinierten Felder: {response.status_code}, {response.text}")
        return {}
    return {field['id']: field['name'] for field in response.json()['results']}

custom_fields_mapping = get_custom_fields_mapping()

def get_documents_of_type(doc_type):
    documents = []
    page_url = f'{api_url}/documents/'
    while page_url:
        params = {'query': f"type:{doc_type}"}
        response = requests.get(page_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Fehler bei der Abfrage von Dokumenten des Typs '{doc_type}': {response.status_code}, {response.text}")
            break
        data = response.json()
        documents.extend(data['results'])
        page_url = data.get('next')
    return documents

def save_removed_field(document_id, field_id, field_name, field_value, default_value):
    # Nur schreiben, wenn der Wert vom Default abweicht
    if field_value != default_value:
        with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([document_id, field_id, field_name, field_value])
        
def update_custom_fields(document_id, field_configs):
    """
    Aktualisiert benutzerdefinierte Felder eines Dokuments basierend auf den angegebenen Konfigurationen.
    :param document_id: Die ID des zu aktualisierenden Dokuments.
    :param field_configs: Eine Liste von Feldkonfigurationen für den Dokumenttyp.
    """
    response = requests.get(f'{api_url}/documents/{document_id}/', headers=headers)
    if response.status_code != 200:
        print(f"Fehler beim Abrufen des Dokuments {document_id}: {response.status_code}")
        return

    document = response.json()
    custom_fields = document.get('custom_fields', [])
    updated_fields = []

    for config in field_configs:
        field_id = config['id']
        field_name = config['name']
        default_value = config['default']
        remove = config['remove']

        existing_field = next((f for f in custom_fields if f['field'] == field_id), None)

        if remove:
            if existing_field and existing_field['value'] != default_value:
                save_removed_field(document_id, field_id, field_name, existing_field['value'], default_value)
            continue

        if existing_field:
            updated_fields.append(existing_field)
        else:
            updated_fields.append({'field': field_id, 'value': default_value})

    if updated_fields != custom_fields:
        response = requests.patch(f'{api_url}/documents/{document_id}/', headers=headers, json={'custom_fields': updated_fields})
        if response.status_code == 200:
            print(f"Benutzerdefinierte Felder für Dokument {document_id} aktualisiert.")
        else:
            print(f"Fehler beim Aktualisieren des Dokuments {document_id}: {response.status_code}, {response.text}")

def process_document_types():
    # Durchlaufen der definierten Dokumenttypen zur Verarbeitung
    for doc_type in document_types_to_process:
        if doc_type in document_type_config:
            fields = document_type_config[doc_type]
            documents = get_documents_of_type(doc_type)
            # Kontrollausgabe für den Dokumenttyp und die Anzahl der Dokumente
            print(f"Verarbeite Dokumenttyp {doc_type}, {len(documents)} Dokumente.")
            for doc in documents:
                update_custom_fields(doc['id'], fields)

process_document_types()

