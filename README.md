# TechWater — Site vitrine

> **Water solutions driven by innovative technologies.**

Site web statique multi-pages présentant l'offre TechWater : équipements et solutions sur mesure pour toute la chaîne de l'eau.

## Aperçu rapide

- Page d'accueil **`index.html`** avec :
  - Hero événementiel **White Fridays** (compte à rebours JS automatique vers le dernier vendredi du mois)
  - Grille des **9 domaines** : Water, Wastewater, Swimming Pool, Agriculture, Industrie, Économie d'eau, Water Reuse, Smart Water, Water Analytics
  - Bloc **Solutions sur mesure** (100% sur mesure, partenariat ADIQUIMICA)
  - Agenda des événements (mensuel · semestriel · annuel)
- Une page dédiée par domaine (10 pages produits)
- **`solutions-sur-mesure.html`** — démarche projet en 5 étapes et expertise traitement/analyse
- **`about.html`** — vision, mission, valeurs, partenaires
- **`contact.html`** — formulaire de devis multi-domaines
- Logo SVG vectoriel personnalisé qui traduit la vision (goutte d'eau + circuit imprimé)

## Lancer en local

C'est un site statique pur (HTML/CSS/JS). N'importe quel serveur statique fait l'affaire :

```bash
# Python 3
python3 -m http.server 8080

# Ou Node
npx serve .
```

Puis ouvrir <http://localhost:8080>.

## Structure

```
.
├── index.html
├── water.html, wastewater.html, swimming-pool.html
├── agriculture.html, industrie.html, economie-eau.html
├── water-reuse.html, water-connect.html, water-analytics.html
├── solutions-sur-mesure.html
├── about.html, contact.html
└── assets/
    ├── css/style.css
    ├── js/main.js
    └── img/logo.svg, favicon.svg
```

## Nom de domaine

Le domaine `techwater.com` est presque certainement **déjà enregistré** (mot très générique).
La vérification doit être faite via un registrar (OVH, GoDaddy, Namecheap, Gandi) ou `whois techwater.com`.

### Alternatives recommandées, alignées avec la baseline « Water solutions driven by innovative technologies »

| Domaine | Pourquoi |
|---|---|
| `techwater.ma` | Ancrage Maroc, court, mémorisable |
| `techwater.africa` | Ambition continentale |
| `techwater.io` / `.tech` | Positionnement tech / innovation |
| `gotechwater.com` | Variante disponible la plupart du temps |
| `techwater-solutions.com` | Descriptif, SEO-friendly |
| `mytechwater.com` | Variante orientée client |
| `techwaterhub.com` | Connote l'écosystème |
| `aquatech-innov.com` | Alternative si la marque « TechWater » est prise |

Recommandation : sécuriser un **bouquet** (`.com` + `.ma` + `.africa`) pour protéger la marque et le SEO local.

## Logo & identité

Le logo `assets/img/logo.svg` représente :

- Une **goutte d'eau** en dégradé cyan → bleu, symbolisant la ressource.
- Un **motif de circuit imprimé** blanc à l'intérieur, symbolisant la technologie innovante.
- Le wordmark **TechWater** en gradient bleu → turquoise, sous-titré par la baseline en capitales.

Le tout en SVG vectoriel : net à toutes les tailles, prêt pour l'impression et le web.

## Personnalisation rapide

- Numéro de téléphone et email : remplacer `+212 5 00 00 00 00` et `contact@techwater.com` dans toutes les pages (faire un `find/replace` global).
- Couleurs marque : variables CSS dans `assets/css/style.css` (`--c-primary`, `--c-accent`, etc.).
- Compte à rebours White Friday : entièrement automatique dans `assets/js/main.js` (calcule chaque mois le prochain dernier vendredi).
- Formulaire de contact : actuellement en démo (JS local). À connecter à un endpoint (Formspree, Netlify Forms, backend custom) en remplaçant le `submit` handler.

## Stack

- HTML5, CSS3 (variables, grid, flex), JavaScript vanilla (zero dépendance).
- Typo Inter via Google Fonts.
- 100% responsive (mobile, tablette, desktop) — testé via media queries à 900px et 520px.
- Accessible (sémantique HTML, contrastes, focus visibles, alt textes).
