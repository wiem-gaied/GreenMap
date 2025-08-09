import os
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenmap.settings")
django.setup()

from .models import CodePostale

def importer_codes_postaux():
    chemin_script = os.path.dirname(os.path.abspath(__file__))
    chemin_fichier = os.path.join(chemin_script, "zip-postcodes.json")

    with open(chemin_fichier, encoding='utf-8') as f:
        donnees = json.load(f)

    compteur = 0
    for item in donnees:
        zip_code = item.get('zip')
        if zip_code:
            obj, created = CodePostale.objects.get_or_create(
                zip=zip_code,
                defaults={
                    'gov': item.get('Gov', ''),
                    'deleg': item.get('Deleg', ''),
                    'cite': item.get('Cite', ''),
                }
            )
            if created:
                compteur += 1
    print(f"{compteur} codes postaux importés.")

if __name__ == "__main__":
    importer_codes_postaux()
