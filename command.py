import os 
import shutil
import subprocess
import requests
from tqdm import tqdm
import json

def export_backup():
   chemin_export="/home/orphee/orphee/backend_bizapp/bizbackup.sql"
   command_dump=[
      'mysqldump',
      "-h", "127.0.0.1",
      "-u","root",
      "-p" + "",
      "bugany"
   ]
   try: 
      print("\n\n Démarrage processus exportation de la base de donnée..........")
      with open(chemin_export, "w+") as fichier_export:
         subprocess.run(command_dump, stdout=fichier_export)
   except Exception as e:
      print("\nErreur lors de l'exportation du fichier :  ", e)


def delete_pycache_dir(directory):
   for root, dirs, files in os.walk(directory):
      if '__pycache__' in dirs:
         chemin_dossier_pycache = os.path.join(root, '__pycache__')
         print("\n\nSuppression du dossier : ", chemin_dossier_pycache)
         try:
            shutil.rmtree(chemin_dossier_pycache)
            print("\nDossier supprimer avec succès \n\n")
         except Exception as e:
            print("\nErreur lors de la suppression du dossier : ", e)



def main():
   while True:
      print("Menu : ")
      print("\n1-Exportation de la base de donnée")
      print("\n2-Supression des dossier __pycache__")
      print("\n3-Terminé")

      choix = input("\nChoisissez (1/2/3) : ")

      if choix == "1":
         print("..................................................")
         print("....... Exportation de la base de donnée .........")
         print("..................................................")
         export_backup()
         break
      elif choix =="2":
         print("...................................................")
         print("....... Supression des dossier __pycache__ ........")
         print("...................................................")
         delete_pycache_dir(os.getcwd())
         break
    
      elif choix =="3":
         print("...................................")
         print("....... Programme Terminé .........")
         print("...................................")
         break
      else:
         print("Option non valide")

if __name__ == "__main__":
   main()



#  total_size = int(response.headers.get('content-length', 0))
#       with tqdm(total=total_size, unit='B', unit_scale=True, desc="Téléchargement") as pbar:
#          contenu_json = 'b'
#          for chunk in response.iter_content(chunk_size=1024):
#             if chunk:
#                contenu_json += chunk
#                pbar.update(len(chunk))