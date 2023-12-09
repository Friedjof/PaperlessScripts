.PHONY: asn reset_asn

# Generate the next 140 ASN's
asn:
	python3 asn/generate.py

# Remove the config file so that it will be regenerated
# this config file stores the last ASN used
# it is used to generate the next ASN in the run
reset_asn:
	rm -rf asn/config.json
