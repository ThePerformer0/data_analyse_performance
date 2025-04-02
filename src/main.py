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

def analyser_performance_heures(df):
    """
    Analyse détaillée des scores de performance et des heures travaillées
    """
    print("\nAnalyse des scores de performance:")
    print(df['Performance Score'].describe())
    print("\nAnalyse des heures travaillées:")
    print(df['Hours Worked'].describe())
    
    # Calcul de la corrélation entre performance et heures travaillées
    correlation = df['Performance Score'].corr(df['Hours Worked'])
    print(f"\nCorrélation entre performance et heures travaillées: {correlation:.3f}")

def analyser_facteurs_performance(df):
    """
    Analyse des facteurs influençant la performance
    """
    # Variables catégorielles à analyser
    variables_categorielles = ['Department', 'Position', 'Employment Status', 'Gender']
    
    for var in variables_categorielles:
        if var in df.columns:
            print(f"\nAnalyse de la performance par {var}:")
            stats = df.groupby(var)['Performance Score'].agg(['mean', 'count', 'std'])
            print(stats)
            
            # Test ANOVA pour vérifier si les différences sont significatives
            groups = [group['Performance Score'].values for name, group in df.groupby(var)]
            f_statistic, p_value = stats.f_oneway(*groups)
            print(f"Test ANOVA - p-value: {p_value:.4f}")

def visualiser_performance_heures(df):
    """
    Crée des visualisations spécifiques pour la performance et les heures travaillées
    """
    # 1. Distribution des scores de performance
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Performance Score', kde=True)
    plt.title('Distribution des scores de performance')
    plt.savefig('visualisations/distribution_performance.png')
    plt.close()
    
    # 2. Distribution des heures travaillées
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Hours Worked', kde=True)
    plt.title('Distribution des heures travaillées')
    plt.savefig('visualisations/distribution_heures.png')
    plt.close()
    
    # 3. Scatter plot performance vs heures travaillées
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Hours Worked', y='Performance Score', alpha=0.5)
    plt.title('Relation entre heures travaillées et performance')
    plt.savefig('visualisations/performance_vs_heures.png')
    plt.close()
    
    # 4. Boxplots de performance par département
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='Department', y='Performance Score')
    plt.xticks(rotation=45)
    plt.title('Distribution des scores de performance par département')
    plt.tight_layout()
    plt.savefig('visualisations/performance_par_departement.png')
    plt.close()

def analyser_tendances_temporelles(df):
    """
    Analyse des tendances temporelles de la performance
    """
    if 'Date of Hire' in df.columns:
        df['Date of Hire'] = pd.to_datetime(df['Date of Hire'])
        df['Ancienneté'] = (pd.Timestamp.now() - df['Date of Hire']).dt.days / 365
        
        # Scatter plot performance vs ancienneté
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='Ancienneté', y='Performance Score', alpha=0.5)
        plt.title('Relation entre ancienneté et performance')
        plt.savefig('visualisations/performance_vs_anciennete.png')
        plt.close()

def main():
    # Chargement des données
    df = charger_donnees()
    
    if df is not None:
        # Création du dossier pour les visualisations
        import os
        os.makedirs('visualisations', exist_ok=True)
        
        # Analyse spécifique de la performance et des heures travaillées
        analyser_performance_heures(df)
        
        # Analyse des facteurs influençant la performance
        analyser_facteurs_performance(df)
        
        # Création des visualisations spécifiques
        visualiser_performance_heures(df)
        
        # Analyse des tendances temporelles
        analyser_tendances_temporelles(df)
        
        print("\nLes visualisations ont été sauvegardées dans le dossier 'visualisations'")

if __name__ == "__main__":
    main()
