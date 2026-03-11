# API Choice

Étudiant : Pasidi COULIBALY
API choisie : Frankfurter (Taux de change)
URL base : https://api.frankfurter.app
Documentation officielle : frankfurter.app/docs
Auth : None
Endpoints testés :
GET /latest : Récupère les derniers taux de change depuis l'Euro.
GET /latest?from=USD : Récupère les taux depuis une devise spécifique.
Hypothèses de contrat :
Champs attendus : amount (float/int), base (string), date (string/ISO8601), rates (objet/dict).
Types : Les valeurs dans rates doivent être des nombres (floats).
Codes HTTP : 200 pour le succès, 404 pour une devise inexistante.
Limites : Pas de clé requise, mais respecter un usage raisonnable (le site indique que c'est ouvert, mais nous resterons sur 1 run / 5 min).
Risques : Instabilité potentielle de la source de données amont (banques centrales), latence réseau.
