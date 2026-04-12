import pandas as pd
import os
import datetime

# --- CONFIGURATION ---
AFFILIATE_URL = "https://try.printify.com/r3xsnwqufe8t"
HOST = "brightlane.github.io"

def update_sitemap(all_keywords):
    """Rebuilds the sitemap.xml with all completed pages."""
    now = datetime.date.today().isoformat()
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    
    # Homepage
    xml.append(f'  <url><loc>https://{HOST}/</loc><lastmod>{now}</lastmod><priority>1.0</priority></url>')
    
    # Add only completed sites
    completed_sites = all_keywords[all_keywords['status'] == 'completed']
    for _, row in completed_sites.iterrows():
        slug = str(row['keyword']).replace(" ", "-").lower()
        xml.append(f'  <url><loc>https://{HOST}/sites/{slug}/</loc><lastmod>{now}</lastmod><priority>0.8</priority></url>')
    
    xml.append('</urlset>')
    with open('sitemap.xml', 'w') as f:
        f.write('\n'.join(xml))
    print("Sitemap.xml updated.")

def generate_schema(keyword):
    """Generates Google Product Schema for better rankings."""
    return f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": "{keyword}",
      "description": "Custom {keyword} designed for durability and style. High-quality print-on-demand.",
      "brand": {{ "@type": "Brand", "name": "Brightlane Custom" }},
      "offers": {{
        "@type": "Offer",
        "url": "{AFFILIATE_URL}",
        "priceCurrency": "USD",
        "price": "24.99",
        "availability": "https://schema.org/InStock"
      }}
    }}
    </script>
    """

def run_engine():
    if not os.path.exists('keywords.csv'):
        print("Error: keywords.csv not found.")
        return
    
    df = pd.read_csv('keywords.csv')
    batch = df[df['status'] == 'pending'].head(10)
    
    if batch.empty:
        print("No pending keywords. All sites are live!")
        return

    for index, row in batch.iterrows():
        kw = row['keyword']
        slug = str(kw).replace(" ", "-").lower()
        os.makedirs(f"sites/{slug}", exist_ok=True)
        
        # Build the HTML Landing Page
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Custom {kw} | Premium Designs</title>
            {generate_schema(kw)}
            <style>
                body {{ font-family: 'Inter', sans-serif; text-align: center; padding: 100px 20px; background: #f8fafc; color: #1e293b; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 50px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
                h1 {{ font-size: 2.5rem; margin-bottom: 20px; }}
                p {{ color: #64748b; font-size: 1.2rem; margin-bottom: 40px; }}
                .btn {{ background: #00e676; color: #000; padding: 20px 40px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block; transition: 0.3s; }}
                .btn:hover {{ transform: scale(1.05); }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Custom {kw}</h1>
                <p>Create your own unique {kw} with high-quality printing and worldwide shipping.</p>
                <a href="{AFFILIATE_URL}" class="btn">GET STARTED ON PRINTIFY</a>
            </div>
        </body>
        </html>
        """
        
        with open(f"sites/{slug}/index.html", "w") as f:
            f.write(html_content)
        
        # Update row status
        df.at[index, 'status'] = 'completed'
        df.at[index, 'date_launched'] = datetime.date.today().isoformat()
        print(f"Created: {slug}")

    # Save CSV and Rebuild Sitemap
    df.to_csv('keywords.csv', index=False)
    update_sitemap(df)

if __name__ == "__main__":
    run_engine()
