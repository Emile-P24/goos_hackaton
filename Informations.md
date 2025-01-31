# goos_hackaton

Dans ce hackathon, nous nous sommes intéressés au jeu World of Goo.
Nous créons des classes pour les Goos et les Plateformes, pour répondre aux spécifications de l'énoncé.
Puis nous tentons de faire le pont entre les classes, qui utilisent numpy, et les modules pygame et pymunk pour créer l'interface graphique de jeu.

Dans un premier temps il faut placer les goos sur l'interface, ceux ci s'accrochent au deux autres goos les plus proches avec un resort.
(Les resorts, la gravite, les rebonds, et toute autre force est définie avec pymunk directement).
Avec pygame, on peut représenter la simulation en temps réel, et intéragir avec celle ci en ajoutant des goos.

Pour faciliter le jeu pour l'utilisateur, il a fallu ajouter un curseur qui indique à quels goos il va s'accrocher. 
Nous avons également fait en sorte qu'il soit impossible de poser un goo qui ne s'accroche pas à un autre, dans le cas où ils seraient trop éloignés.