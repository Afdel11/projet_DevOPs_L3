# 🎓 DIT Teaching Evaluation System  

## 📖 Aperçu  
Solution interne développée pour le **Dakar Institute of Technology** afin de :  
- **Remplacer Typeform** (limités en contrôle des données et analyses).  
- **Automatiser** la collecte et l'analyse des évaluations enseignants/cours.  
- **Garantir la confidentialité** (données hébergées en interne).  

## 🛠 Fonctionnalités  
### Pour les Étudiants  
- Évaluation des cours via interface simplifiée (notes/commentaires).  
- Sélection dynamique des classes/matières.  

### Pour les Administrateurs  
- Génération de rapports PDF/Excel (stats agrégées, tendances).  
- Gestion des classes/matières et réinitialisation des sondages.  

## ⚙️ Architecture  
```mermaid  
graph TD  
    A[Flask Backend] --> B[(SQLite)]  
    A --> C[Frontend HTML/Tailwind]  
    D[Jenkins CI/CD] --> E[Docker Containers]  
    E --> F[Kubernetes Cluster]  
