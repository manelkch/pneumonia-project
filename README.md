# pneumonia-project

# PneumoScan - Système de Détection de Pneumonie (CNN)

## Présentation du Projet

Ce projet industrialise un modèle de Deep Learning pour l'imagerie médicale. Il s'agit d'une architecture micro-services déployée sur Microsoft Azure, orchestrée via Docker Compose et provisionnée automatiquement par Terraform.

Points clés :

- IA : Classification binaire (PNEUMONIA / NORMAL) via CNN.

- Haute Disponibilité : 3 réplicas du modèle pour répartir la charge.

- Load Balancing : Serveur Nginx en tant que reverse-proxy.

- Automatisation : Script de déploiement "one-click" (deploy.sh).

## Liens de Référence

- Documentation du Modèle (Hugging Face) : [https://huggingface.co/sukhmani1303/pneumonia-cnn-model]

- Jeu de données de test (Kaggle) : [https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia]

## Architecture Technique

- Backend : Flask (Python 3.9), TensorFlow-CPU.

- Interface Web : HTML5/JS. 

- Conteneurisation : Docker & Docker Compose.

- Infrastructure : Azure VM (Standard_D2s_v3), Terraform.

## Structure du Projet
Plaintext

├── app.py              # Logique d'inférence Flask
├── pneumonia_cnn.h5    # Modèle Keras entraîné (150x150)
├── templates/          # Interface utilisateur (Frontend)
├── nginx.conf          # Configuration du Load Balancer
├── Dockerfile          # Image Docker de l'application
├── docker-compose.yml  # Orchestration des micro-services
├── main.tf             # Infrastructure as Code (Azure)
└── deploy.sh           # Script d'automatisation globale

## Déploiement et Utilisation

### Lancer le déploiement

Depuis votre terminal local, assurez-vous d'être connecté à Azure, puis lancez :
Bash

`
az login
chmod +x deploy.sh
./deploy.sh
`

## Tester le système

- Interface Web : Ouvrez http://<VOTRE_IP_AZURE>/ dans votre navigateur.

  - Test API (CURL) :

Bash

`curl -X POST -F "file=@radio.jpg" http://<VOTRE_IP_AZURE>/predict`

## Maintenance (Troubleshooting)

- Dimensions : Le modèle exige des images de $150 \times 150$ pixels en niveaux de gris.

- Nettoyage : Pour détruire l'infrastructure et éviter les frais Azure :

Bash

`terraform destroy -auto-approve`

Projet réalisé dans le cadre du module DevOps.
