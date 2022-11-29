# boosted_technology_consent_api

Install dependencies:
`pip3 install -r requirements.txt`

To run:
`python3 init.py`

App will be running on localhost.
Example queries:

```
curl -X GET \
  -H "Content-type: application/json" \
  -H "Accept: application/json" \
  "http://127.0.0.1:5000/consent/target"


curl -X POST \
  -H "Content-type: application/json" \
  -H "Accept: application/json" \
  -d '{"name":"pharmacy.allow_marketing_emails", "consent_url":"http://example.com/marketing_terms"}' \
  "http://127.0.0.1:5000/consent/target"


curl -X PATCH \
  -H "Content-type: application/json" \
  -H "Accept: application/json" \
  -d '{"consent_url":"http://example.com/marketing_terms_updated2"}' \
  "http://127.0.0.1:5000/consent/target/<targetId>"
```
