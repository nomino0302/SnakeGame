# SnakeGame 🐍

Le jeu nécessite Python et Pygame pour être lancé depuis les sources :

```sh
python -m pip install -r requirements.txt
python snakeGame.py
```

Depuis les sources, les images et polices se trouvent dans `assets/` et les
scores et derniers réglages dans `scores.json`, à la racine du projet. Pour
macOS, ces fichiers sont dans `Snake.app/Contents/Resources/`. Sur Windows et
Linux, ils se trouvent à côté de l'exécutable.

## Créer les applications

Installer les dépendances et PyInstaller dans un environnement Python de la
plateforme cible :

```sh
python -m pip install -r requirements.txt pyinstaller
```

Sur macOS Apple Silicon, avec Python ARM64 :

```sh
python -m PyInstaller --noconfirm --onedir --windowed --name Snake --icon assets/img/icon/icon.icns --add-data "assets:assets" snakeGame.py
mkdir -p apps
ditto -c -k --keepParent dist/Snake.app apps/Snake-macos-arm64.zip
```

Distribuer `apps/Snake-macos-arm64.zip`. Le fichier
`scores.json` est créé dans le `.app` après une partie. `dist/Snake` est un
dossier intermédiaire qui n'est pas nécessaire.

Sur Windows x86_64, avec Python x86_64 :

```powershell
python -m PyInstaller --noconfirm --onedir --windowed --name Snake --distpath apps/windows-x86_64 --icon assets/img/icon/icon.ico snakeGame.py
Copy-Item -Recurse assets apps/windows-x86_64/Snake/assets
Compress-Archive -Path apps/windows-x86_64/Snake -DestinationPath apps/Snake-windows-x86_64.zip
```

Distribuer le ZIP créé : `Snake.exe` a besoin des autres fichiers du dossier.
L'archive `apps/Snake-windows-x86_64.zip` actuellement présente est une
ancienne version datant de 2022 : elle ne contient pas les derniers correctifs.

Sur Linux x86_64, avec Python x86_64 :

```sh
python -m PyInstaller --noconfirm --onedir --windowed --name Snake --distpath apps/linux-x86_64 snakeGame.py
cp -R assets apps/linux-x86_64/Snake/assets
cd apps/linux-x86_64 && zip -r ../Snake-linux-x86_64.zip Snake && cd ../..
```

Distribuer le ZIP créé, en conservant le droit d'exécution du fichier `Snake`.
Construire sous
une distribution Linux aussi ancienne que celles que l'on souhaite prendre en
charge. Les versions Windows et Linux doivent être construites sur leurs
plateformes respectives, par exemple avec un ordinateur ou une machine
virtuelle adaptée. Les joueurs n'ont pas besoin d'installer Python ou Pygame.

Le dossier du jeu doit être accessible en écriture pour enregistrer les scores.
Sur macOS, le contenu du `.app` doit lui aussi être accessible en écriture.
Avant de remplacer l'application par une nouvelle version, conserver son
`Contents/Resources/scores.json` pour ne pas perdre les scores. Modifier ce
fichier invalide la signature du bundle, y compris la signature ad hoc générée
par PyInstaller ; cette organisation n'est donc pas adaptée à une future
distribution signée et notarisée.

Ces builds ne sont pas signés : macOS et Windows peuvent afficher un
avertissement de sécurité au téléchargement ou au premier lancement.
