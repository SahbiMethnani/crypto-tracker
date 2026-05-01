# 🚀 Crypto Analytics Dashboard

Application web d’analyse et de visualisation des marchés de cryptomonnaies en temps réel, développée avec **Streamlit** et alimentée par l’API **CCXT**.

---

## 📊 Fonctionnalités

* 📈 **Graphiques avancés**

  * Chandeliers (Candlestick)
  * Bandes de Bollinger
  * Moyennes mobiles (SMA 20 / 50)
  * RSI (Relative Strength Index)
  * MACD

* 🔄 **Données en temps réel**

  * Connexion aux exchanges via CCXT
  * Rafraîchissement automatique des données

* 📉 **Analyse de marché**

  * Top volumes (USDT)
  * Variation des prix (24h)
  * Corrélation entre actifs
  * Distribution des rendements

* 📊 **Dashboard interactif**

  * Comparaison multi-actifs
  * Scatter plot (Volume vs Variation)
  * Heatmap de corrélation

---

## 🛠️ Technologies utilisées

* **Python 3.10+**
* **Streamlit** → Interface web interactive
* **CCXT** → API crypto multi-exchanges
* **Pandas / NumPy** → Traitement des données
* **Plotly** → Visualisation avancée

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/your-username/crypto-dashboard.git
cd crypto-dashboard
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## ▶️ Lancer l’application

```bash
streamlit run app.py
```

Puis ouvrir dans ton navigateur :

```
http://localhost:8501
```

---

## 🔌 Configuration

Tu peux modifier les paramètres dans :

* `config.py` → couleurs, styles, layout
* `app.py` → logique principale
* `charts.py` → personnalisation des graphiques

---

## 📡 Sources de données

L’application utilise **CCXT** pour récupérer les données depuis des exchanges comme :

* Binance
* KuCoin
* Kraken
* Bybit

---

## 📁 Structure du projet

```
crypto-dashboard/
│
├── app.py              # Application principale Streamlit
├── charts.py           # Génération des graphiques
├── data.py             # Récupération des données CCXT
├── indicators.py       # Calcul des indicateurs techniques
├── config.py           # Configuration UI / couleurs
├── requirements.txt   # Dépendances
├── ui.py           #  UI 
└── README.md

```



