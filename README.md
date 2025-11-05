# Portfolio Risk Parity - Analyse de 8 Actions Tech

## 📊 Vue d'ensemble

Ce projet implémente une stratégie d'allocation de portefeuille basée sur le **Risk Parity** appliqué à 8 actions technologiques majeures. L'analyse comparative est réalisée avec le NASDAQ-100 (QQQ) comme benchmark de marché.

## 🎯 Actions analysées

Le portefeuille est composé de 8 actions tech de premier plan :
- **NVDA** (NVIDIA)
- **META** (Meta Platforms)
- **TSLA** (Tesla)
- **JPM** (JPMorgan Chase)
- **GLD** (SPDR Gold Trust)
- **CAT** (Caterpillar)
- **UNH** (UnitedHealth Group)

**Période d'analyse** : 1er janvier 2015 - 31 décembre 2024 (10 ans)

## 🔧 Méthodologie

### 1. Calcul du Risk Parity

L'allocation Risk Parity est calculée de manière simple mais efficace :

```python
weights[i] = 0.0 if std == 0 else 1.0 / std
```

**Principe** : Chaque actif reçoit un poids **inversement proportionnel à sa volatilité annualisée**. Les actifs plus risqués reçoivent moins de poids, et vice versa, pour équilibrer les contributions au risque.

### 2. Construction du portefeuille

1. **Collecte des données** : Téléchargement des prix ajustés via `yfinance`
2. **Calcul des rendements** : Rendements logarithmiques quotidiens
3. **Mesure de volatilité** : Écart-type annualisé pour chaque action
4. **Allocation Risk Parity** : Poids inversement proportionnels à la volatilité
5. **Normalisation** : Les poids sont normalisés pour sommer à 100%

### 3. Comparaison avec le marché

Le portefeuille Risk Parity est comparé au **NASDAQ-100 (QQQ)** sur la même période, permettant d'évaluer la performance relative de la stratégie.

## 📈 Métriques de performance calculées

Le notebook calcule un ensemble complet de métriques financières :

### Métriques de rendement
- **Rendement annualisé** : Performance moyenne composée
- **Volatilité annualisée** : Risque du portefeuille (σ × √252)

### Ratios ajustés au risque
- **Ratio de Sharpe** : (Rendement - Rf) / Volatilité
  - Taux sans risque : 2% annuel
- **Ratio de Sortino** : Rendement excédentaire / Downside deviation
- **Ratio de Treynor** : Rendement excédentaire / Beta

### Métriques de risque
- **Beta** : Sensibilité au marché (covariance / variance du marché)
- **Maximum Drawdown** : Perte maximale depuis un pic
- **Skewness** : Asymétrie de la distribution des rendements
- **Kurtosis** : Épaisseur des queues de distribution

### Métriques avancées
- **Information Ratio** : Alpha / Tracking Error
  - Mesure la performance ajustée au risque actif

## 📊 Visualisations

Le notebook génère plusieurs graphiques analytiques :

1. **Rendements cumulés** : Évolution du portefeuille avec identification des pics et creux
2. **Running Maximum Drawdown** : Visualisation du risque de perte en continu
3. **Histogramme des rendements** : Distribution des rendements du portefeuille
4. **Heatmap mensuelle** : Rendements mensuels par année (style calendrier)
5. **Comparaison Portfolio vs QQQ** : Performance relative avec leverage 2x pour amplifier les différences

## 🛠️ Technologies utilisées

```python
import yfinance as yf           
import math                     
import pandas as pd             
import numpy as np              
import matplotlib.pyplot as plt 
from tabulate import tabulate   
import seaborn as sns          
import warnings                 
```

## 📦 Installation

### Prérequis

```bash
pip install yfinance pandas numpy matplotlib seaborn tabulate
```

### Exécution

```bash
jupyter notebook 01_RP_Perf_ana.ipynb
```

Ou avec JupyterLab :
```bash
jupyter lab 01_RP_Perf_ana.ipynb
```

## 🔍 Résultats et insights

### Points clés de l'analyse

1. **Allocation équilibrée par le risque** : Les actifs les plus volatils (ex: TSLA, NVDA) reçoivent automatiquement moins de poids

2. **Diversification améliorée** : La stratégie Risk Parity tend à mieux diversifier qu'une allocation équipondérée

3. **Comparaison avec le marché** : 
   - Le benchmark QQQ représente l'indice tech le plus suivi
   - L'utilisation d'un leverage 2x permet de visualiser les écarts de performance

4. **Métriques complètes** : Le tableau final récapitule toutes les métriques dans un format structuré

### Exemple de sortie

Le code génère un tableau formaté avec toutes les métriques :

```
Parameters          Value
----------------  -------
Annual Returns      X.XX%
Annual Volatility   X.XX%
Sharpe Ratio        X.XX
Sortino Ratio       X.XX
Beta                X.XX
Treynor Ratio       X.XX
Information Ratio   X.XX
Skewness            X.XX
Kurtosis            X.XX
Maximum Drawdown    X.XX%
```

## 💡 Approche méthodologique

⚠️ **Limitations** :
- Ne prend pas en compte les corrélations entre actifs
- Ne garantit pas strictement l'égalité des contributions au risque
- Version simplifiée du "True Risk Parity" qui utiliserait la matrice de covariance complète

## 📝 Structure du code

```
├── Import des librairies
├── Téléchargement des données (2015-2024)
├── Calcul des rendements et statistiques par actif
├── Allocation Risk Parity (inverse volatility)
├── Construction du portefeuille
├── Calcul des métriques de performance
│   ├── Rendement et volatilité annualisés
│   ├── Sharpe, Sortino, Treynor ratios
│   ├── Beta, Information Ratio
│   └── Moments supérieurs (Skewness, Kurtosis)
├── Analyse du drawdown
├── Visualisations
│   ├── Cumulative returns
│   ├── Running maximum drawdown
│   ├── Histogramme des rendements
│   ├── Heatmap mensuelle
│   └── Comparaison vs NASDAQ-100
└── Tableau récapitulatif des métriques
```

## 👤 Auteur

🧑🏽‍💻 Bonny Ryan Fotsing


