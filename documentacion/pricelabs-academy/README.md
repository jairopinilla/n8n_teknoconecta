# PriceLabs Knowledge Base (Academia)

Scraping completo del portal de ayuda de PriceLabs en español
(https://help.pricelabs.co/portal/es/kb/pricelabs).

**Fecha de extraccion:** 2026-05-15
**Total de articulos:** 365 (de ~375 disponibles)
**Idioma:** Espanol

## Archivos por categoria

| Archivo | Categoria | Articulos |
|---------|-----------|-----------|
| `dynamic-pricing.md` | Dynamic Pricing | 281 |
| `market-dashboards.md` | Market Dashboards | 26 |
| `portfolio-analytics.md` | Portfolio Analytics | 19 |
| `pricing-and-billing.md` | Precios y Facturacion | 12 |
| `account.md` | Cuenta | 10 |
| `new-users.md` | Empezar con PriceLabs | 9 |
| `listing-optimizer.md` | Listing Optimizer | 8 |

## Subcategorias en Dynamic Pricing

- Basic Setup (10 arts)
- Pricing Dashboard (7 arts)
- Customizations
  - Other Useful Customizations (7 arts)
  - Stay Restrictions (8 arts)
  - General (5 arts)
  - Seasonal and Minimum Prices (4 arts)
  - Advanced Customizations (9 arts)
  - Bulk Customizations (3 arts)
- Algorithm (4 arts)
- PMS Integrations
  - General PMS Information (7 arts)
  - A-F (51 arts)
  - G-M (52 arts)
  - N-S (45 arts)
  - T-Z (23 arts)
- Price Calculations (12 arts)
- Pricing Strategies (8 arts)
- PriceLabs for Hotels (12 arts)
- Multicalendar (1 art)
- Manage Listings (4 arts)
- DP FAQs (15 arts)

## Metodologia de scraping

1. Extraccion de URLs navegando categorias/subcategorias via Playwright (Python)
2. Descarga individual de cada articulo extrayendo solo contenido principal
3. Consolidacion en archivos markdown por categoria

## Notas

- 5 articulos no se pudieron descargar por timeout del servidor
- El contenido esta en texto plano extraido del `<article>` HTML
- Las imagenes no se incluyeron; las URLs de imagenes permanecen en el HTML original
- Para ver el HTML completo de cualquier articulo, consultar `/tmp/pl_html_articles/`

## Fuente original

https://help.pricelabs.co/portal/es/kb/pricelabs
