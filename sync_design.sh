#!/bin/bash

echo "🔁 Synchronisation des fichiers design vers l'app Flask..."

rsync -av ~/Documents/Phoenix\ Code/design/templates/ ./app/templates/
rsync -av ~/Documents/Phoenix\ Code/design/static/css/ ./app/static/css/

echo "✅ Fait."
