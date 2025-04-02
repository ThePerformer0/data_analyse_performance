import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configuration du style des graphiques
plt.style.use('seaborn-v0_8')
sns.set_theme()
sns.set_palette("husl")

def charger_donnees():
    """
    Charge les données depuis le fichier CSV
    """
    try:
        df = pd.read_csv('data/HRDataset_v14.xls', encoding='utf-8-sig')
        print("Données chargées avec succès!")
        print("\nAperçu des données:")
        print(df.head())
        print("\nInformations sur le dataset:")
        print(df.info())
        return df
    except FileNotFoundError:
        print("Erreur: Le fichier de données n'a pas été trouvé.")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {str(e)}")
        return None

def analyser_statistiques_descriptives(df):
    """
    Calcule les statistiques descriptives de base
    """
    print("\nStatistiques descriptives:")
    print(df.describe())

def main():
    # Chargement des données
    df = charger_donnees()
    
    if df is not None:
        # Analyse des statistiques descriptives
        analyser_statistiques_descriptives(df)
        
        # TODO: Ajouter les visualisations
        # TODO: Implémenter la détection des outliers

if __name__ == "__main__":
    main()
