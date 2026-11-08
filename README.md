# Crypto Analytics Dashboard

Application web d’analyse et de visualisation des marchés de cryptomonnaies en temps réel, développée avec **Streamlit** et alimentée par l’API **CCXT**.
---

## Fonctionnalités

* 📈 **Graphiques avancés**

  * Chandeliers (Candlestick)
  * Bandes de Bollinger
  * Moyennes mobiles (SMA 20 / 50)
  * RSI (Relative Strength Index)
  * MACD

* **Données en temps réel**

  * Connexion aux exchanges via CCXT
  * Rafraîchissement automatique des données

*  **Analyse de marché**

  * Top volumes (USDT)
  * Variation des prix (24h)
  * Corrélation entre actifs
  * Distribution des rendements

*  **Dashboard interactif**

  * Comparaison multi-actifs
  * Scatter plot (Volume vs Variation)
  * Heatmap de corrélation

---

## Technologies utilisées

* **Python 3.10+**
* **Streamlit** → Interface web interactive
* **CCXT** → API crypto multi-exchanges
* **Pandas / NumPy** → Traitement des données
* **Plotly** → Visualisation avancée

---




## Sources de données

L’application utilise **CCXT** pour récupérer les données depuis des exchanges comme :

* Binance
* KuCoin
* Kraken
* Bybit

---

## Limites

ccxt refuse les requests prod 

le but maintenant d'avoir une solution de se cacher lors de l'interrogation de l'api 

**En cours d'etude** : 
une api local consome  ccxt  et notre application va consomer cette api (proxy caché)



