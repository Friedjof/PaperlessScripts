# Paperless Scripts
This repository contains scripts to help with some paperless workflows.

## Installation
1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install the requirements: `pip install -r requirements.txt`

## Usage
### Generate ASNs
Display the help message for more information:
```bash
python asn/generate.py -h
```
You will finde the generated PDFs in the `asn` folder.

You can visit also the [Makefile](Makefile) for more information about the usage.

#### Sources
1. [Paperless QR-Code ASN](https://margau.net/posts/2023-04-16-paperless-ngx-asn/)
2. [Generate ASN](https://pypi.org/project/paperless-asn-qr-codes/)
3. [Custom ASN script](https://gist.github.com/timrprobocom/3946aca8ab75df8267bbf892a427a1b7/)

### API - Scripts
Manage paperless user defined fields for documenttypes
1. configure config.py and config_documenttypes.py, use *.template if you want an example
2. Initially use organize-doctype-fields to change all existing documents in your paperless instance
3. Regulary use update-open-document-fields.py to update documents with tag "Offen" for defined type fields