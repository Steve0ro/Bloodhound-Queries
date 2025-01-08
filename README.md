# Older Bloodhound queries to BloodhoundCE Script

## Author: https://medium.com/seercurity-spotlight/make-bloodhound-cool-again-migrating-custom-queries-from-legacy-bloodhound-to-bloodhound-ce-83cffcfe5b64

- Needed to work the json data and bash script.
The whole reason for this script was due to the original script and JQ command not working for me. 

- JQ command that worked for me:
```bash
jq '[.queries[] | {name: .name, query: .queryList[0].query}] | map(select(.name != null and .query != null))' customqueries.json > cleaned_customqueries.json

```

---

# How to use?
Make sure Bloodhound-CE is up and running, admin password is set.

# Run:

```bash
python3 bloodhound_upload.py -f JSON/cleaned_customqueries.json -u admin -p 'p@ssword123!!'

```

---
