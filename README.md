# Hochnebelkarte Schweiz

High Fog Service Switzerland by HSR Geometa Lab.

Weblinks:

- "Hochnebelkarte Schweiz" (Prototype): http://geometalab.github.io/fog_app.webapp/
- General information about "Nebelkarte Schweiz": http://giswiki.hsr.ch/Hochnebelkarte

## Development

Normal docker-compose usage, copy `.env-file` file to `.env` and fill it
with the correct values.

### Running tests

```bash
docker-compose run --rm backend bash -c 'cd tests && python -m unittest'
```
