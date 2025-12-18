#!/bin/bash

# Arrêt du script en cas d'erreur
set -e

echo "--- [1/4] INITIALISATION DE L'INFRASTRUCTURE AZURE ---"
terraform init
terraform apply -auto-approve

# Récupération de l'IP publique générée par Terraform
IP_VM=$(terraform output -raw public_ip_address)
echo "L'infrastructure est prête. IP de la VM : $IP_VM"

echo "--- [2/4] TRANSFERT DES FICHIERS VERS LE CLOUD ---"
# On envoie tout le dossier (Modèle h5, Dockerfile, Nginx, Compose)
scp -o StrictHostKeyChecking=no -r ./* azureuser@$IP_VM:/home/azureuser/

echo "--- [3/4] CONFIGURATION DU SERVEUR DISTANT ---"
ssh -o StrictHostKeyChecking=no azureuser@$IP_VM << EOF
    # Installation de Docker
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo systemctl start docker
    sudo usermod -aG docker azureuser
   
    # Lancement de la stack Pneumonie (Niveau 2 & 3)
    cd /home/azureuser
    sudo docker-compose up --build -d
EOF

echo "--- [4/4] VÉRIFICATION FINALE ---"
echo "Attente du démarrage des conteneurs..."
sleep 15
curl -s http://$IP_VM/health

echo ""
echo "PROJET TERMINÉ AVEC SUCCÈS !"
echo "Votre modèle CNN est déployé sur : http://$IP_VM"
