

# Repo perso mais publique

Expérimentations pour un meilleur système à événements 100% python.


# Que faire comme ajouts?

-duplication de code pour ne plus rien aller chercher dans dossier parent (..)

-simplification/nettoyage
implem de NetworkLayer reste à unifier: client & serveur

- au niveau du modèle:
Peut-on encore mieux split code overhead/generic et code spécifique au jeu?

- faire en sorte que mediator devienne Singleton puisqu'on veut s'assurer qu'on en utilise un seul
par instance de programme

-verifier a nouveau que Mediator peut etre utile sans NetworkLayer pour etre sur qu'on
a gardé un total découplage

-la logique de jeu cote serveur devient isolee si possible sans héritage
(façon 'STRATEGY' pattern,
https://sourcemaking.com/design_patterns/strategy.
Contexte possède une stratégie)

- Du 'sucre syntaxique'
  - les events seraient automatiquement modelisés (str->class)
Cela evitera les bug et permettra davoir des tests plus robustes. Par exemple:
     - au lieu de tester le nom en chaine de caractères à plusieurs endroits, set attribut + ev.is_special() getter

     - utilisation de chaine de car. pour post mais si l'évent n'a jamais été déclaré ou que des attr sont manquants
 raise ValueError dès le post!
  
- les ev_listeners sont automatiquement 'register' sur le mediator, grace aux methodes on_*

- "FLAG" via les commentaires tt le code destiné une conversion JS.
On peut la faire une fois pour toute puis versionner le code JS en sortie pour notre app.
