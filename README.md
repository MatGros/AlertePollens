# 🌸 AlertePollens

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MQTT](https://img.shields.io/badge/MQTT-enabled-orange.svg)](https://mqtt.org/)

> Système de surveillance automatisé des niveaux d'alerte pollinique en France avec publication MQTT pour domotique

## 📋 Description

**AlertePollens** est un script Python qui télécharge et analyse automatiquement les cartes de vigilance pollinique depuis [pollens.fr](https://www.pollens.fr). Il détecte les niveaux d'alerte par reconnaissance de couleur et publie les données via MQTT pour une intégration facile avec des systèmes domotiques (Home Assistant, Jeedom, etc.).

### Cartes analysées

| Type | Source |
|------|--------|
| 🗺️ Carte de vigilance générale | ![Vigilance Map](https://www.pollens.fr/generated/vigilance_map.png) |
| 🌲 Cyprès (Cupressacées) | ![Cypres](https://www.pollens.fr/uploads/historic/2022/cypres.png) |

## ✨ Fonctionnalités

- 📥 **Téléchargement automatique** des cartes de vigilance pollinique
- 🎨 **Reconnaissance de couleur** pour déterminer les niveaux d'alerte
  - 🟢 Vert = Risque **FAIBLE**
  - 🟡 Jaune = Risque **MOYEN**
  - 🔴 Rouge = Risque **ÉLEVÉ**
- 📡 **Publication MQTT** des données pour intégration domotique
- ⏰ **Mise à jour périodique** configurable
- 🐛 **Mode debug** pour visualisation et diagnostic
- 📍 **Position géographique personnalisable** (coordonnées pixel)

## 🚀 Installation

### Prérequis

- Python 3.6 ou supérieur
- Un broker MQTT (Mosquitto, Eclipse Mosquitto, etc.)

### Dépendances

```bash
pip install pillow paho-mqtt
```

Ou installez toutes les dépendances :

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Paramètres à personnaliser

#### 1. Configuration MQTT

**⚠️ IMPORTANT - Sécurité**: Ne jamais mettre de mots de passe ou identifiants directement dans le code !

Utilisez des variables d'environnement pour configurer le broker MQTT :

**Option A - Variables d'environnement directes** :

```bash
export MQTT_BROKER="your.broker.ip"     # Adresse IP de votre broker MQTT
export MQTT_PORT="1883"                  # Port MQTT (1883 par défaut)
export MQTT_USERNAME="your_username"     # Nom d'utilisateur MQTT
export MQTT_PASSWORD="your_password"     # Mot de passe MQTT
```

**Option B - Fichier .env (recommandé)** :

1. Copiez le fichier d'exemple :
```bash
cp .env.example .env
```

2. Éditez `.env` avec vos identifiants réels :
```bash
MQTT_BROKER=your.broker.ip
MQTT_PORT=1883
MQTT_USERNAME=your_username
MQTT_PASSWORD=your_secure_password
```

3. Chargez les variables et lancez le script :
```bash
# Option sécurisée avec set
set -a
source .env
set +a
python AlertePollens_Img_v1.5-MQTT.py

# Ou utilisez python-dotenv (recommandé pour la production)
# pip install python-dotenv
```

**Note**: Le fichier `.env` est automatiquement ignoré par Git pour protéger vos identifiants.

#### 2. Position géographique

Ajustez les coordonnées pixel pour votre département en éditant le fichier `AlertePollens_Img_v1.5-MQTT.py` :

```python
ReadPix_X = 300  # Coordonnée X du pixel à analyser
ReadPix_Y = 330  # Coordonnée Y du pixel à analyser
```

#### 3. Intervalle de rafraîchissement

Éditez le fichier `AlertePollens_Img_v1.5-MQTT.py` pour ajuster l'intervalle :

```python
sleepTime = 10  # Temps en secondes entre chaque vérification
```

#### 4. Mode debug

Éditez le fichier `AlertePollens_Img_v1.5-MQTT.py` pour activer/désactiver le mode debug :

```python
debugMode = 1  # 1 = activé, 0 = désactivé
```

## 📊 Topics MQTT

Le script publie les données suivantes :

| Topic | Description | Valeurs possibles |
|-------|-------------|-------------------|
| `AP/VPC` | Vigilance Pollens - Couleur | `Vert`, `Jaune`, `Rouge`, `?` |
| `AP/VPN` | Vigilance Pollens - Niveau | `FAIBLE`, `MOYEN`, `ELEVE`, `NUL` |
| `AP/VPCrgb` | Vigilance Pollens - RGB | `[R, G, B]` |
| `AP/CGC` | Cyprès - Couleur | `Vert`, `Jaune`, `Rouge`, `?` |
| `AP/CGN` | Cyprès - Niveau | `FAIBLE`, `MOYEN`, `ELEVE`, `NUL` |
| `AP/CGCrgb` | Cyprès - RGB | `[R, G, B]` |
| `AP/datetime` | Date et heure de la dernière mise à jour | ISO 8601 |
| `AP/math` | Signal de test (sinusoïdal) | Valeur numérique |

## 🎯 Utilisation

### Lancement du script

```bash
python AlertePollens_Img_v1.5-MQTT.py
```

### Mode debug

En mode debug (debugMode = 1), le script :
- Affiche les images téléchargées avec une croix sur le pixel analysé
- Imprime des informations détaillées dans la console
- Garde les fenêtres d'aperçu ouvertes quelques secondes

### Exécution en arrière-plan

#### Linux/macOS

```bash
nohup python AlertePollens_Img_v1.5-MQTT.py &
```

#### Windows (avec pythonw)

```bash
pythonw AlertePollens_Img_v1.5-MQTT.py
```

#### Avec systemd (Linux)

Créez `/etc/systemd/system/alertepollens.service` :

```ini
[Unit]
Description=Alerte Pollens Monitor
After=network.target

[Service]
Type=simple
User=votre_utilisateur
WorkingDirectory=/chemin/vers/AlertePollens
Environment="MQTT_BROKER=your.broker.ip"
Environment="MQTT_PORT=1883"
Environment="MQTT_USERNAME=your_username"
Environment="MQTT_PASSWORD=your_secure_password"
ExecStart=/usr/bin/python3 AlertePollens_Img_v1.5-MQTT.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Ou pour charger depuis un fichier `.env` :

```ini
[Unit]
Description=Alerte Pollens Monitor
After=network.target

[Service]
Type=simple
User=votre_utilisateur
WorkingDirectory=/chemin/vers/AlertePollens
EnvironmentFile=/chemin/vers/AlertePollens/.env
ExecStart=/usr/bin/python3 AlertePollens_Img_v1.5-MQTT.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Activez le service :

```bash
sudo systemctl enable alertepollens
sudo systemctl start alertepollens
```

## 🏠 Intégration domotique

### Home Assistant

Ajoutez dans `configuration.yaml` :

```yaml
mqtt:
  sensor:
    - name: "Vigilance Pollens Niveau"
      state_topic: "AP/VPN"
      icon: mdi:flower-pollen
      
    - name: "Vigilance Pollens Couleur"
      state_topic: "AP/VPC"
      
    - name: "Cyprès Niveau"
      state_topic: "AP/CGN"
      icon: mdi:tree
      
    - name: "Cyprès Couleur"
      state_topic: "AP/CGC"
      
    - name: "Dernière MAJ Pollens"
      state_topic: "AP/datetime"
      icon: mdi:clock-outline
```

### Jeedom

Utilisez le plugin MQTT pour créer des équipements avec les topics ci-dessus.

## 🔧 Fonctionnement technique

1. **Téléchargement** : Récupération des images PNG depuis pollens.fr
2. **Redimensionnement** : Réduction à 470x470 pixels pour optimisation
3. **Analyse** : Lecture de la couleur RGB du pixel aux coordonnées configurées
4. **Classification** :
   - RGB(0-60, 128+, 0-60) → Vert/FAIBLE
   - RGB(200+, 200+, 0-60) → Jaune/MOYEN
   - RGB(200+, 0-60, 0-60) → Rouge/ÉLEVÉ
5. **Publication** : Envoi des données vers le broker MQTT

## 🔒 Sécurité

### Bonnes pratiques

- ⚠️ **Ne jamais commiter de mots de passe ou clés API** dans le dépôt Git
- ✅ Utilisez des variables d'environnement pour toutes les informations sensibles
- ✅ Ajoutez `.env` dans `.gitignore` pour éviter les commits accidentels
- ✅ Utilisez des mots de passe forts pour votre broker MQTT
- ✅ Limitez l'accès réseau au broker MQTT (firewall, VPN, etc.)
- ✅ Changez les mots de passe par défaut de tous les services

### Configuration sécurisée

Créez un fichier `.env` (non commité) contenant vos identifiants :

```bash
MQTT_BROKER=votre_broker_ip
MQTT_PORT=1883
MQTT_USERNAME=votre_username
MQTT_PASSWORD=votre_password_securise
```

Le script chargera automatiquement ces variables d'environnement.

## 📝 Notes

- Les images sont sauvegardées localement (`vigilance_map.png`, `cypres.png`)
- Le script tourne en boucle infinie
- Les messages MQTT avec `retain=True` sont conservés par le broker
- Le signal mathématique sinusoïdal (`AP/math`) peut servir de test de connectivité

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- 🐛 Signaler des bugs
- 💡 Proposer de nouvelles fonctionnalités
- 🔧 Soumettre des pull requests

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- [pollens.fr](https://www.pollens.fr) pour les données polliniques
- RNSA (Réseau National de Surveillance Aérobiologique)

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

**⚠️ Avertissement** : Ce projet est à but éducatif et personnel. Assurez-vous de respecter les conditions d'utilisation de pollens.fr lors de l'utilisation de leurs données.