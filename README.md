# 🚀 Brightlane Perpetual SEO Engine (2026 Edition)

This is a fully automated, headless affiliate marketing machine. It programmatically generates high-converting landing pages for **Printify** products, auto-updates a Google-ready sitemap, and manages a growing keyword database—all via GitHub Actions.

## 🛠️ System Architecture

| Component | Purpose | Status |
| :--- | :--- | :--- |
| **`generator.py`** | The Engine: Builds pages, refills keywords, updates sitemap. | 🟢 Active |
| **`keywords.csv`** | The Fuel: Database of target keywords and launch status. | 🟢 Ready |
| **`.github/workflows/`** | The Pulse: Triggers the rollout every night at 00:00 UTC. | 🟢 Scheduled |
| **`sitemap.xml`** | The Map: Notifies Google of new content automatically. | 🟢 Auto-Gen |

## ⚙️ How It Works

1.  **Drip-Feed Rollout:** Every 24 hours, the GitHub Action wakes up and processes the next **10 keywords** from `keywords.csv`.
2.  **Auto-Generation:** It creates a dedicated directory in `/sites/` with an optimized `index.html` featuring:
    * **JSON-LD Schema:** To get Product Rich Snippets in Google.
    * **Printify Affiliate Link:** Hardcoded to your specific ID.
    * **Responsive UI:** Clean, modern design optimized for mobile conversions.
3.  **Perpetual Fueling:** If the `pending` keyword count drops below 20, the script automatically generates **50 new niche-specific keywords** and appends them to the CSV.
4.  **Automatic Indexing:** The `sitemap.xml` is rebuilt and pushed back to the repo, signaling Google's crawlers via the `robots.txt` pointer.

## 📈 Monitoring & Maintenance

### To Add Custom Keywords:
Simply open `keywords.csv` and add your specific long-tail terms in the following format:
`your-keyword-here,pending,`

### To Trigger an Immediate Rollout:
1.  Navigate to the **Actions** tab.
2.  Select **Daily SEO CSV Rollout**.
3.  Click **Run workflow** -> **Branch: main**.

### Affiliate Tracking:
All traffic is funneled through the affiliate identifier: `r3xsnwqufe8t`.

## 🛡️ Legal & Compliance
The site includes a centralized `legal.html` covering:
* Affiliate Disclosures
* Privacy Policy
* Printify Official Support Contact
* **Exit-Intent Capture:** Cookie-based modal to catch bouncing traffic.

---
**Admin:** [brightlane](https://github.com/brightlane)  
**Host:** [brightlane.github.io](https://brightlane.github.io/)
