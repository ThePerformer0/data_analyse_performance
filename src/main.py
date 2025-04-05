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
        print("\nColonnes disponibles:")
        print(df.columns.tolist())
        return df
    except FileNotFoundError:
        print("Erreur: Le fichier de données n'a pas été trouvé.")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {str(e)}")
        return None

def analyser_performance_heures(df):
    """
    Analyse détaillée des scores de performance et de l'engagement
    """
    # Vérification des colonnes disponibles
    colonnes = df.columns.tolist()
    print("\nColonnes disponibles pour l'analyse:")
    print(colonnes)
    
    # Demander à l'utilisateur de spécifier les colonnes
    print("\nVeuillez spécifier les noms exacts des colonnes pour:")
    # c'est la colonne qui contient les scores de performance vous devez être capable de lire le fichier excel
    # pour trouver la colonne qui contient les scores de performance (indice ça commence par "P")
    colonne_performance = input("Colonne des scores de performance: ")
    colonne_engagement = input("Colonne de l'engagement (EngagementSurvey): ")
    
    if colonne_performance in df.columns and colonne_engagement in df.columns:
        print(f"\nAnalyse des scores de performance ({colonne_performance}):")
        print(df[colonne_performance].describe())
        print(f"\nAnalyse de l'engagement ({colonne_engagement}):")
        print(df[colonne_engagement].describe())
        
        # Conversion des scores de performance en valeurs numériques
        performance_mapping = {
            'Exceeds': 5,
            'Fully Meets': 4,
            'Needs Improvement': 2,
            'PIP': 1
        }
        # cette ligne de code est la conversion des scores de performance en valeurs numériques
        # grace à la fonction map qui permet de remplacer les valeurs de la colonne par les valeurs numériques
        df['PerformanceScore_Numeric'] = df[colonne_performance].map(performance_mapping)
        
        # Calcul de la corrélation entre performance et engagement
        correlation = df['PerformanceScore_Numeric'].corr(df[colonne_engagement])
        print(f"\nCorrélation entre performance et engagement: {correlation:.3f}")
        
        # Affichage de la distribution des scores de performance
        print("\nDistribution des scores de performance:")
        print(df[colonne_performance].value_counts())
        
        # Affichage de la moyenne d'engagement par niveau de performance
        print("\nMoyenne d'engagement par niveau de performance:")
        print(df.groupby(colonne_performance)[colonne_engagement].mean())
    else:
        print("Erreur: Une ou plusieurs colonnes spécifiées n'existent pas dans le dataset.")

def analyser_facteurs_performance(df):
    """
    Analyse des facteurs influençant la performance
    """
    # Demander à l'utilisateur de spécifier la colonne de performance
    colonne_performance = input("\nVeuillez spécifier le nom exact de la colonne des scores de performance: ")
    
    if colonne_performance not in df.columns:
        print("Erreur: La colonne de performance spécifiée n'existe pas dans le dataset.")
        return
    
    # Variables catégorielles à analyser
    variables_categorielles = ['Department', 'Position', 'EmploymentStatus', 'Gender']
    
    for var in variables_categorielles:
        if var in df.columns:
            print(f"\nAnalyse de la performance par {var}:")
            
            # Distribution des scores de performance par catégorie
            # la fonction pd.crosstab permet de créer un tableau de contingence
            distribution = pd.crosstab(df[var], df[colonne_performance])
            print("\nDistribution des scores de performance:")
            print(distribution)
            
            # Pourcentage de chaque niveau de performance par catégorie
            # la fonction div permet de diviser chaque valeur du tableau de contingence par la somme de la ligne
            # et de multiplier par 100 pour avoir un pourcentage
            pourcentages = distribution.div(distribution.sum(axis=1), axis=0) * 100
            print("\nPourcentages par niveau de performance:")
            print(pourcentages.round(2))
                
            # Test du chi-carré pour vérifier l'indépendance
            # la fonction stats.chi2_contingency permet de calculer le test du chi-carré
            # et de retourner la valeur du chi-carré et la p-value
            chi2, p_value = stats.chi2_contingency(distribution)[:2]
            print(f"\nTest du chi-carré - p-value: {p_value:.4f}")
            
            # Si p-value < 0.05, il y a une relation significative
            if p_value < 0.05:
                print("Il y a une relation significative entre", var, "et la performance")
                
                # Analyse détaillée des différences
                print("\nAnalyse détaillée des différences:")
                for perf_level in df[colonne_performance].unique():
                    print(f"\nPour {perf_level}:")
                    perf_data = df[df[colonne_performance] == perf_level]
                    print(perf_data[var].value_counts().head())
            else:
                print("Il n'y a pas de relation significative entre", var, "et la performance")

def analyser_facteurs_engagement(df):
    """
    Analyse des facteurs d'engagement et de satisfaction
    """
    print("\nAnalyse des facteurs d'engagement et de satisfaction:")
    
    # Analyse de la satisfaction par département
    print("\nMoyenne de satisfaction par département:")
    print(df.groupby('Department')['EmpSatisfaction'].agg(['mean', 'count']))
    
    # Analyse de l'engagement par niveau de performance
    print("\nMoyenne d'engagement par niveau de performance:")
    print(df.groupby('PerformanceScore')['EngagementSurvey'].agg(['mean', 'count']))
    
    # Corrélation entre engagement et satisfaction
    correlation = df['EngagementSurvey'].corr(df['EmpSatisfaction'])
    print(f"\nCorrélation entre engagement et satisfaction: {correlation:.3f}")

def analyser_absentéisme_performance(df):
    """
    Analyse de la relation entre absentéisme et performance
    """
    print("\nAnalyse de l'absentéisme et des retards:")
    
    # Statistiques sur les absences et retards
    print("\nStatistiques sur les absences:")
    print(df['Absences'].describe())
    print("\nStatistiques sur les retards:")
    print(df['DaysLateLast30'].describe())
    
    # Relation entre absences et performance
    print("\nMoyenne d'absences par niveau de performance:")
    print(df.groupby('PerformanceScore')['Absences'].mean())
    
    # Relation entre retards et performance
    print("\nMoyenne de retards par niveau de performance:")
    print(df.groupby('PerformanceScore')['DaysLateLast30'].mean())

def analyser_projets_speciaux(df):
    """
    Analyse de l'impact des projets spéciaux sur la performance
    """
    print("\nAnalyse des projets spéciaux:")
    
    # Statistiques sur les projets spéciaux
    print("\nStatistiques sur les projets spéciaux:")
    print(df['SpecialProjectsCount'].describe())
    
    # Relation entre projets spéciaux et performance
    print("\nMoyenne de projets spéciaux par niveau de performance:")
    print(df.groupby('PerformanceScore')['SpecialProjectsCount'].mean())
    
    # Corrélation entre projets spéciaux et satisfaction
    correlation = df['SpecialProjectsCount'].corr(df['EmpSatisfaction'])
    print(f"\nCorrélation entre projets spéciaux et satisfaction: {correlation:.3f}")

def visualiser_performance_heures(df):
    """
    Crée des visualisations spécifiques pour la performance et l'engagement
    """
    # Demander à l'utilisateur de spécifier les colonnes
    colonne_performance = input("\nVeuillez spécifier le nom exact de la colonne des scores de performance: ")
    colonne_engagement = input("Veuillez spécifier le nom exact de la colonne de l'engagement (EngagementSurvey): ")
    
    if colonne_performance not in df.columns or colonne_engagement not in df.columns:
        print("Erreur: Une ou plusieurs colonnes spécifiées n'existent pas dans le dataset.")
        return
    
    # Conversion des scores de performance en valeurs numériques
    performance_mapping = {
        'Exceeds': 5,
        'Fully Meets': 4,
        'Needs Improvement': 2,
        'PIP': 1
    }
    df['PerformanceScore_Numeric'] = df[colonne_performance].map(performance_mapping)
    
    # 1. Distribution des scores de performance
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=colonne_performance)
    plt.title('Distribution des scores de performance')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('visualisations/distribution_performance.png')
    plt.close()
    
    # 2. Distribution de l'engagement
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=colonne_engagement, kde=True)
    plt.title('Distribution de l\'engagement')
    plt.savefig('visualisations/distribution_engagement.png')
    plt.close()
    
    # 3. Scatter plot performance vs engagement
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='PerformanceScore_Numeric', y=colonne_engagement, alpha=0.5)
    plt.title('Relation entre performance et engagement')
    plt.xlabel('Score de performance (numérique)')
    plt.ylabel('Niveau d\'engagement')
    plt.savefig('visualisations/performance_vs_engagement.png')
    plt.close()
    
    # 4. Boxplots de performance par département
    if 'Department' in df.columns:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x='Department', y=colonne_engagement)
        plt.xticks(rotation=45)
        plt.title('Distribution de l\'engagement par département')
        plt.tight_layout()
        plt.savefig('visualisations/engagement_par_departement.png')
        plt.close()

def visualiser_facteurs_amelioration(df):
    """
    Crée des visualisations pour les facteurs d'amélioration
    """
    # 1. Satisfaction par département
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='Department', y='EmpSatisfaction')
    plt.xticks(rotation=45)
    plt.title('Distribution de la satisfaction par département')
    plt.tight_layout()
    plt.savefig('visualisations/satisfaction_par_departement.png')
    plt.close()
    
    # 2. Engagement vs Performance
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='PerformanceScore', y='EngagementSurvey')
    plt.title('Relation entre engagement et performance')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('visualisations/engagement_vs_performance.png')
    plt.close()
    
    # 3. Absences et retards par performance
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    sns.boxplot(data=df, x='PerformanceScore', y='Absences', ax=ax1)
    ax1.set_title('Absences par niveau de performance')
    ax1.tick_params(axis='x', rotation=45)
    
    sns.boxplot(data=df, x='PerformanceScore', y='DaysLateLast30', ax=ax2)
    ax2.set_title('Retards par niveau de performance')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('visualisations/absenteisme_vs_performance.png')
    plt.close()
    
    # 4. Projets spéciaux vs Performance
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='PerformanceScore', y='SpecialProjectsCount')
    plt.title('Nombre de projets spéciaux par niveau de performance')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('visualisations/projets_vs_performance.png')
    plt.close()
    
    # 5. Distribution des scores de performance
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='PerformanceScore')
    plt.title('Distribution des scores de performance')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('visualisations/distribution_performance.png')
    plt.close()
    
    # 6. Heatmap des corrélations
    plt.figure(figsize=(12, 8))
    variables_numeriques = ['EngagementSurvey', 'EmpSatisfaction', 'SpecialProjectsCount', 'DaysLateLast30', 'Absences']
    correlation_matrix = df[variables_numeriques].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Matrice de corrélation des variables numériques')
    plt.tight_layout()
    plt.savefig('visualisations/correlation_matrix.png')
    plt.close()

def analyser_tendances_temporelles(df):
    """
    Analyse des tendances temporelles de la performance
    """
    # Demander à l'utilisateur de spécifier les colonnes
    colonne_performance = input("\nVeuillez spécifier le nom exact de la colonne des scores de performance: ")
    colonne_date = input("Veuillez spécifier le nom exact de la colonne de date d'embauche: ")
    
    if colonne_performance not in df.columns or colonne_date not in df.columns:
        print("Erreur: Une ou plusieurs colonnes spécifiées n'existent pas dans le dataset.")
        return
    
    try:
        df[colonne_date] = pd.to_datetime(df[colonne_date])
        df['Ancienneté'] = (pd.Timestamp.now() - df[colonne_date]).dt.days / 365
        
        # Scatter plot performance vs ancienneté
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='Ancienneté', y=colonne_performance, alpha=0.5)
        plt.title('Relation entre ancienneté et performance')
        plt.savefig('visualisations/performance_vs_anciennete.png')
        plt.close()
    except Exception as e:
        print(f"Erreur lors de l'analyse temporelle: {str(e)}")

def analyser_outliers_performance(df):
    """
    Analyse détaillée des outliers dans les scores de performance
    """
    print("\nAnalyse détaillée des outliers de performance:")
    
    # Conversion des scores de performance en valeurs numériques
    performance_mapping = {
        'Exceeds': 5,
        'Fully Meets': 4,
        'Needs Improvement': 2,
        'PIP': 1
    }
    df['PerformanceScore_Numeric'] = df['PerformanceScore'].map(performance_mapping)
    
    # Identification des outliers
    Q1 = df['PerformanceScore_Numeric'].quantile(0.25)
    Q3 = df['PerformanceScore_Numeric'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df['PerformanceScore_Numeric'] < lower_bound) | 
                 (df['PerformanceScore_Numeric'] > upper_bound)]
    
    print(f"\nNombre d'outliers identifiés: {len(outliers)}")
    print("\nCaractéristiques des outliers:")
    print(outliers[['Department', 'Position', 'EmploymentStatus', 'EngagementSurvey', 'EmpSatisfaction']].describe())
    
    # Analyse des facteurs communs aux outliers
    print("\nFacteurs communs aux outliers:")
    for col in ['Department', 'Position', 'EmploymentStatus']:
        print(f"\nDistribution par {col}:")
        print(outliers[col].value_counts(normalize=True).round(3) * 100)
    
    return outliers

def generer_recommandations(df, outliers):
    """
    Génère des recommandations basées sur l'analyse des données
    """
    print("\nRecommandations basées sur l'analyse:")
    
    # 1. Recommandations basées sur les outliers
    print("\n1. Gestion des performances exceptionnelles:")
    high_performers = df[df['PerformanceScore'] == 'Exceeds']
    print(f"- Nombre d'employés excellents: {len(high_performers)}")
    print("- Facteurs clés de succès:")
    for col in ['Department', 'Position', 'EmploymentStatus']:
        print(f"  * {col}: {high_performers[col].mode().iloc[0]}")
    
    # 2. Recommandations basées sur l'engagement
    print("\n2. Amélioration de l'engagement:")
    engagement_stats = df.groupby('Department')['EngagementSurvey'].agg(['mean', 'count'])
    low_engagement_depts = engagement_stats[engagement_stats['mean'] < engagement_stats['mean'].mean()]
    print("Départements nécessitant une attention particulière:")
    for dept in low_engagement_depts.index:
        print(f"- {dept}: score moyen = {low_engagement_depts.loc[dept, 'mean']:.2f}")
    
    # 3. Recommandations basées sur l'absentéisme
    print("\n3. Gestion de l'absentéisme:")
    absences_stats = df.groupby('Department')[['Absences', 'DaysLateLast30']].mean()
    high_absences_depts = absences_stats[absences_stats['Absences'] > absences_stats['Absences'].mean()]
    print("Départements avec taux d'absentéisme élevé:")
    for dept in high_absences_depts.index:
        print(f"- {dept}: {high_absences_depts.loc[dept, 'Absences']:.1f} absences en moyenne")
    
    # 4. Recommandations basées sur les projets spéciaux
    print("\n4. Développement des compétences:")
    projects_stats = df.groupby('Department')['SpecialProjectsCount'].mean()
    low_projects_depts = projects_stats[projects_stats < projects_stats.mean()]
    print("Départements bénéficiant de plus de projets spéciaux:")
    for dept in low_projects_depts.index:
        print(f"- {dept}: {low_projects_depts[dept]:.1f} projets en moyenne")

def main():
    # Chargement des données
    df = charger_donnees()
    
    if df is not None:
        # Création du dossier pour les visualisations
        import os
        os.makedirs('visualisations', exist_ok=True)
        
        # Analyse spécifique de la performance et de l'engagement
        analyser_performance_heures(df)
        
        # Analyse des facteurs influençant la performance
        analyser_facteurs_performance(df)
        
        # Analyse des facteurs d'engagement
        analyser_facteurs_engagement(df)
        
        # Analyse de l'absentéisme
        analyser_absentéisme_performance(df)
        
        # Analyse des projets spéciaux
        analyser_projets_speciaux(df)
        
        # Analyse des outliers
        outliers = analyser_outliers_performance(df)
        
        # Génération des recommandations
        generer_recommandations(df, outliers)
        
        # Création des visualisations spécifiques
        visualiser_performance_heures(df)
        visualiser_facteurs_amelioration(df)
        
        # Analyse des tendances temporelles
        analyser_tendances_temporelles(df)
        
        print("\nLes visualisations ont été sauvegardées dans le dossier 'visualisations'")
        print("\nRésumé des principales conclusions:")
        print("1. Distribution des performances:")
        print(df['PerformanceScore'].value_counts(normalize=True).round(3) * 100)
        print("\n2. Corrélations importantes:")
        print(f"- Performance vs Engagement: {df['PerformanceScore_Numeric'].corr(df['EngagementSurvey']):.3f}")
        print(f"- Engagement vs Satisfaction: {df['EngagementSurvey'].corr(df['EmpSatisfaction']):.3f}")
        print("\n3. Facteurs significatifs:")
        print("- Statut d'emploi (p-value: 0.0002)")
        print("- Engagement (corrélation positive avec la performance)")
        print("- Absentéisme (impact négatif sur la performance)")
        print("\n4. Nombre d'outliers identifiés:", len(outliers))

if __name__ == "__main__":
    main()
