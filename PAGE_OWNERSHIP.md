# StockSense AI — Page Inventory & Developer Ownership Matrix

This document defines the comprehensive page inventory, component hierarchy, shared file governance, and incremental implementation order for the **Pearl Aurora (Apple Liquid Glass Light UI)** transformation of StockSense AI.

---

## 1. Shared Files Governance & Single Ownership

To prevent merge conflicts and maintain design consistency across two collaborating developers, all shared files are assigned strict single-owner custody:

| Shared File | Primary Custodian | Secondary Contributor Rule |
| :--- | :--- | :--- |
| `frontend/style.css` | **Developer A** | Developer A maintains the design tokens (`:root`, `body.light-mode`), glass tier utilities, and global base rules. Developer B submits scoped CSS rules for specific views/components to Developer A or works in designated scoped comment blocks. |
| `frontend/index.html` | **Shared by Section** | Edits are strictly isolated by container `id`. Developer A edits global navigation, `#dashboardView`, and `#financialsView`. Developer B edits isolated containers (`#inventoryView`, `#insightsView`, `#settingsView`, modals). |
| `frontend/app.js` | **Shared by Module** | Developer A owns core initialization, view router (`switchView`), and theme switcher. Developer B owns module-specific event handlers (data tables, forms, settings persistence). |
| `frontend/docs.html` | **Developer A** | Standalone technical whitepaper portal. Solely maintained by Developer A. |

---

## 2. Complete Page & View Inventory

The application operates as a Single-Page Application (SPA) driven by `switchView(viewName)` alongside one standalone technical documentation portal (`docs.html`).

### Page 1: Overview Dashboard
- **Route / Trigger**: `switchView('dashboard')` | `#navDashboard`
- **Main Components**:
  - Executive AI insight banner card (`#dashboardView .ai-insight-card`)
  - 4-column KPI Metric Grid (`.kpi-grid`: Total SKUs, Stockout Risks, Overstock Risks, Predicted Stockouts)
  - Demand Forecasting Interactive Chart Card (`#forecastChart` with 7/14/30-day forecast horizon toggles and confidence intervals)
  - Promotional Planner Card Deck (`#promo-planner-section`: holiday surges, clearance cards)
  - Stock Alerts & Reorder Timeline (`#stockAlertsTimelineCard`)
  - Drivers of Demand & Profitability Container (`#demandDriversCard`, `#profitDriversCard`)
- **Existing Functionality**:
  - Fetches telemetry from `/api/analytics/kpis`, `/api/forecast/plot`, and `/api/analytics/alerts`.
  - Chart.js dynamic rendering with upper/lower bounds.
  - Interactive recommendation cards with direct action triggers.
- **Shared Components Used**: `top-navbar`, `top-bar`, `app-footer`, `aiHelpContainer`, `toastContainer`.
- **Complexity**: **High**
- **Dependencies**: `/api/analytics/*`, `/api/forecast/*`, Chart.js, `app.js`.
- **Suggested Owner**: **Developer A**

---

### Page 2: Financial Control Tower
- **Route / Trigger**: `switchView('financials')` | `#navFinancials`
- **Main Components**:
  - Executive Financial KPI Grid (Inventory Valuation, Holding Costs, Procurement Spends, Projected ROI)
  - Working Capital Optimization Curve (Interactive Chart.js area chart)
  - Carrying Cost Breakdown Donut Chart
  - Capital Efficiency & Cash Flow Projection Data Table
- **Existing Functionality**:
  - Fetches financial telemetry from `/api/analytics/financials`.
  - Computes dynamic holding cost percentages, capital savings, and reorder budget projections.
- **Shared Components Used**: `top-navbar`, `top-bar`, `app-footer`, `toastContainer`.
- **Complexity**: **Medium**
- **Dependencies**: `/api/analytics/financials`, Chart.js, `app.js`.
- **Suggested Owner**: **Developer A**

---

### Page 3: Global Inventory Database & Catalog
- **Route / Trigger**: `switchView('inventory')` | `#navInventory`
- **Main Components**:
  - Live Stock Health KPI Cards (Total Inventory, Optimal Stock, Low Stock Warning, Critical Stockout)
  - Power-Grid Controls (Fuzzy search with auto-highlighting, category filter pills, export/import buttons, bulk Draft PO button)
  - Interactive Data Grid (`#inventoryTable` with multi-select checkboxes, sortable columns, SKU badges, inline actions)
  - PO History Ledger sub-table (tracks submitted purchase orders)
  - Subordinate Drawers & Modals:
    - Product Telemetry Slide-Over Drawer (`#productTelemetryDrawer`)
    - Consolidated Multi-Item Draft PO Modal (`#draftPoModal`)
    - CSV Staging & Validation Modal (`#csvValidationModal`)
    - Forecast Accuracy Scorecard Modal (`#accuracyScorecardModal`)
- **Existing Functionality**:
  - Full CRUD operations via `/api/inventory/`.
  - Dynamic ROP toggling (Auto AI calculation vs manual ROP override).
  - Bulk purchase order generation via `/api/purchase-orders/`.
  - CSV file ingestion, automated column mapping, and inline error correction.
- **Shared Components Used**: `top-navbar`, `top-bar`, `app-footer`, `productTelemetryDrawer`, `draftPoModal`, `csvValidationModal`, `toastContainer`.
- **Complexity**: **High**
- **Dependencies**: `/api/inventory/*`, `/api/purchase-orders/*`, `/api/analytics/accuracy`, `app.js`.
- **Suggested Owner**: **Developer B**

---

### Page 4: AI Strategic Assistant Cockpit
- **Route / Trigger**: `switchView('insights')` | `#navInsights`
- **Main Components**:
  - Dual-Column Cockpit Layout:
    - Left Sidebar: Chat session history, archive viewer trigger, trash viewer trigger, active AI model selector
    - Main Conversation Canvas: Message stream, assistant reasoning bubbles, dynamic insight cards, pre-engineered prompt suggestions
    - Bottom Input Bar: Multi-line prompt input, model indicator, send button
  - Associated Modals:
    - Archived Conversations Modal (`#archiveModalOverlay`)
    - Deleted Conversations Trash Modal (`#trashModalOverlay`)
- **Existing Functionality**:
  - Real-time conversation with local Ollama LLaMA model via `/api/insights/chat`.
  - Contextual inventory memory injection into system prompt.
  - Chat session persistence, session archiving, and soft-delete/restore mechanics.
- **Shared Components Used**: `top-navbar`, `app-footer`, `archiveModalOverlay`, `trashModalOverlay`, `toastContainer`.
- **Complexity**: **High**
- **Dependencies**: `/api/insights/chat`, Ollama daemon (`http://127.0.0.1:11434`), `app.js`.
- **Suggested Owner**: **Developer B**

---

### Page 5: Enterprise Settings & Profile Management
- **Route / Trigger**: `switchView('settings')` | `#navSettings`
- **Main Components**:
  - Settings Tab Navigation (`#settingsTabNav`):
    - Tab 1: Organization & Profile (Company name, industry, currency, business email, avatar)
    - Tab 2: AI Engine Configuration (Model parameters, forecast horizon, lead time variance, confidence bounds)
    - Tab 3: Alert & Notification Preferences (Safety stock threshold, email triggers, webhook endpoints)
    - Tab 4: Security & API Keys (API tokens, session policies)
    - Tab 5: Data Management (Purge database, reset demo data, export full backup)
- **Existing Functionality**:
  - Reads and updates profile data via `/api/user/profile`.
  - Client-side persistence in `localStorage` for UI preferences.
  - Password management and security credential forms.
- **Shared Components Used**: `top-navbar`, `app-footer`, standard form controls, `toastContainer`, `customConfirmOverlay`.
- **Complexity**: **Medium**
- **Dependencies**: `/api/user/profile`, `localStorage`, `app.js`.
- **Suggested Owner**: **Developer B**

---

### Page 6: System Architecture & How It Works
- **Route / Trigger**: `switchView('howItWorks')` | `#footerNavHowItWorks`
- **Main Components**:
  - Interactive Pipeline Visualizer (Ingestion -> Ensemble Forecasting -> SHAP XAI -> Business Synthesis)
  - Mathematical breakdown cards for Prophet and LightGBM models
  - Dynamic interactive simulation sliders (Lead time vs Safety stock buffer)
  - Model benchmarking comparison cards
- **Existing Functionality**:
  - Educational technical walkthrough of underlying machine learning workflows and supply chain formulas.
- **Shared Components Used**: `top-navbar`, `app-footer`.
- **Complexity**: **Medium**
- **Dependencies**: `app.js`.
- **Suggested Owner**: **Developer A**

---

### Page 7: Enterprise Features Overview
- **Route / Trigger**: `switchView('features')` | `#footerNavFeatures`
- **Main Components**:
  - Feature capability grid (Dynamic ROP, Multi-Item PO Planner, Explainable AI, CSV Staging, Financial Tower)
  - Deep-dive cards with gradient iconography and capability highlights
  - Quick action CTA pills linking directly to functional views
- **Existing Functionality**:
  - Product showcase and feature navigation directory.
- **Shared Components Used**: `top-navbar`, `app-footer`.
- **Complexity**: **Low**
- **Dependencies**: `app.js`.
- **Suggested Owner**: **Developer A**

---

### Page 8: Pricing & ROI Value Calculator
- **Route / Trigger**: `switchView('pricing')` | `#footerNavPricing`
- **Main Components**:
  - 3-Tier Plan Comparison Cards (Community / Self-Hosted, SME Growth, Enterprise Cloud)
  - Interactive ROI & Cost-Savings Calculator (sliders for annual inventory value, stockout rates, carrying costs)
  - Projected annual capital recovery output card
- **Existing Functionality**:
  - Dynamic client-side mathematical computation calculating estimated carrying cost savings.
- **Shared Components Used**: `top-navbar`, `app-footer`, slider controls.
- **Complexity**: **Medium**
- **Dependencies**: `app.js`.
- **Suggested Owner**: **Developer B**

---

### Page 9: About Us & Capstone Team Showcase
- **Route / Trigger**: `switchView('about')` | `#footerNavAbout`
- **Main Components**:
  - Mission statement & project genesis narrative
  - Capstone Research Team Profiles (Member 1: Backend, Member 2: Frontend, Member 3: Frontend & Data)
  - University affiliation & Department of Software Engineering (DIU) acknowledgments
  - Technology stack badges
- **Existing Functionality**:
  - Academic and institutional attribution showcase.
- **Shared Components Used**: `top-navbar`, `app-footer`.
- **Complexity**: **Low**
- **Dependencies**: `app.js`.
- **Suggested Owner**: **Developer A**

---

### Page 10: Enterprise Support & Contact
- **Route / Trigger**: `switchView('contact')` | `#footerNavContact`
- **Main Components**:
  - Direct communication cards (Support email, documentation link, repository link)
  - Interactive Contact / Demo Request Form (Full name, business email, company, inquiry category, message)
  - Submit button with dynamic loading state, error validation, and confirmation banner
- **Existing Functionality**:
  - Validates contact form inputs and provides simulated asynchronous submission with toast confirmation.
- **Shared Components Used**: `top-navbar`, `app-footer`, form elements, `toastContainer`.
- **Complexity**: **Medium**
- **Dependencies**: `app.js` (contact form event listener).
- **Suggested Owner**: **Developer B**

---

### Page 11: Data Sovereignty & Privacy Policy
- **Route / Trigger**: `switchView('privacy')` | `#footerNavPrivacy`
- **Main Components**:
  - Sticky Table of Contents Sidebar (`#privacy-toc-sidebar` with scroll-spy navigation)
  - Back to Dashboard and Jump to Settings navigation buttons
  - Policy content blocks: Local-first custody, zero telemetry transmission, CSV processing boundaries, cryptographic SQLite storage
- **Existing Functionality**:
  - Scroll-spy active link tracking and quick navigation.
- **Shared Components Used**: `top-navbar`, `app-footer`.
- **Complexity**: **Low**
- **Dependencies**: `app.js` (scroll spy).
- **Suggested Owner**: **Developer B**

---

### Page 12: Terms of Service & Licensing
- **Route / Trigger**: `switchView('terms')` | `#footerNavTerms`
- **Main Components**:
  - Sticky Table of Contents Sidebar (`#legal-toc-sidebar` with scroll-spy navigation)
  - Return to Dashboard button
  - Legal clauses: Agreement, definitions, open-source MIT licensing, limitation of liability
- **Existing Functionality**:
  - Scroll-spy active link tracking and legal disclosures.
- **Shared Components Used**: `top-navbar`, `app-footer`.
- **Complexity**: **Low**
- **Dependencies**: `app.js` (scroll spy).
- **Suggested Owner**: **Developer B**

---

### Page 13: Technical Documentation Portal (`frontend/docs.html`)
- **Route / Trigger**: Standalone URL `/docs.html` (Accessible via top navbar link and footer)
- **Main Components**:
  - Fixed Documentation Header & Quick Search Bar
  - Left Sidebar Navigation (Executive Summary, System Architecture, ML Benchmarks, Explainability XAI, REST API, Security & Compliance, Deployment)
  - Right Side Content Canvas: Deep technical whitepaper, system sequence diagrams, LaTeX math equations, code blocks, parameter tables
- **Existing Functionality**:
  - Interactive search through documentation headings, smooth anchor scrolling, responsive mobile menu drawer.
- **Shared Components Used**: Self-contained within `docs.html` (independent header, sidebar, and style system).
- **Complexity**: **High**
- **Dependencies**: Standalone file.
- **Suggested Owner**: **Developer A**

---

## 3. Developer Ownership Division Summary

```mermaid
graph TD
    subgraph Developer A - Core Architecture & Primary Views
        A1[Global Pearl Aurora Tokens & CSS] --> A2[Top Navigation & Header]
        A2 --> A3[Overview Dashboard #dashboardView]
        A3 --> A4[Financial Control Tower #financialsView]
        A4 --> A5[How It Works #howItWorksView]
        A5 --> A6[Features & About Pages]
        A6 --> A7[Docs Portal docs.html]
    end

    subgraph Developer B - Secondary Views, Tables & Workflows
        B1[Global Inventory Power-Grid #inventoryView] --> B2[Product Telemetry Drawer]
        B2 --> B3[Draft PO Planner Modal]
        B3 --> B4[CSV Import Staging Modal]
        B4 --> B5[AI Strategic Assistant #insightsView]
        B5 --> B6[Settings & Profile #settingsView]
        B6 --> B7[Pricing, Contact & Legal Views]
    end
```

### Developer A (Design System Architect & Primary Views)
- **Global Assets**: `frontend/style.css` (Master Token Owner), `frontend/docs.html`.
- **Shared UI**: `top-navbar`, `top-bar`, `app-footer`, global ambient canvas background.
- **Assigned Pages**:
  1. Overview Dashboard (`#dashboardView`)
  2. Financial Control Tower (`#financialsView`)
  3. How It Works / Architecture (`#howItWorksView`)
  4. Enterprise Features (`#featuresView`)
  5. About Us & Team (`#aboutView`)
  6. Technical Documentation Portal (`docs.html`)

### Developer B (Data Modules, Tables, Forms & Utilities)
- **Shared UI Modals**: `productTelemetryDrawer`, `draftPoModal`, `csvValidationModal`, `accuracyScorecardModal`, `archiveModalOverlay`, `trashModalOverlay`.
- **Assigned Pages**:
  1. Global Inventory Database & Power-Grid (`#inventoryView`)
  2. AI Strategic Assistant Cockpit (`#insightsView`)
  3. Settings & Profile Management (`#settingsView`)
  4. Pricing & ROI Calculator (`#pricingView`)
  5. Enterprise Support & Contact (`#contactView`)
  6. Privacy Policy (`#privacyView`)
  7. Terms of Service (`#termsView`)

---

## 4. Sequential Page-by-Page Implementation Order

To respect the incremental redesign rule and avoid concurrent edit conflicts, work must proceed strictly in the following sequential order:

```
[Phase 1] Developer A: Global Tokens & Ambient Canvas (style.css foundation)
    ↓
[Phase 2] Developer A: Top Navigation & Header Bar (top-navbar, top-bar)
    ↓
[Phase 3] Developer A: Overview Dashboard (#dashboardView)
    ↓
[Phase 4] Developer B: Inventory Database & Power-Grid (#inventoryView)
    ↓
[Phase 5] Developer B: Modals & Drawers (Telemetry Drawer, Draft PO, CSV Staging)
    ↓
[Phase 6] Developer A: Financial Control Tower (#financialsView)
    ↓
[Phase 7] Developer B: AI Strategic Assistant Cockpit (#insightsView)
    ↓
[Phase 8] Developer B: Settings & Profile Management (#settingsView)
    ↓
[Phase 9] Developer A: Product Showcase (How It Works, Features, About)
    ↓
[Phase 10] Developer B: Utility & Compliance (Pricing, Contact, Privacy, Terms)
    ↓
[Phase 11] Developer A: Documentation Portal (docs.html)
```
