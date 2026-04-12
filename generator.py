import pandas as pd
import os
import datetime
import random

# --- CONFIGURATION ---
AFFILIATE_URL = "https://try.printify.com/r3xsnwqufe8t"
HOST = "brightlane.github.io"

# --- PERPETUAL FUEL (Keyword Components) ---
NICHES = ["German Shepherd", "Siberian Husky", "Digital Nomad", "Vegan", "Minimalist", "Retro Gaming", "Mental Health", "Zodiac", "Sustainable", "Crypto", "90s Vintage", "Pickleball"]
PRODUCTS = ["Hoodie", "Coffee Mug", "Canvas Tote", "Water Bottle", "Phone Case", "Comfort Tee", "Leggings", "Fleece Blanket"]
MODIFIERS = ["Premium", "Custom", "Hand-Drawn", "Minimalist", "Vintage Style"]

def refill_keywords(df):
    """Automatically adds 50 new unique keywords if the queue is low."""
    pending_count = len(df[df['status'] == 'pending'])
    if pending_count < 20:
        print("Fuel low! Generating 50 new keywords...")
        new_items = []
        while len(new_items) < 50:
            kw = f"{random.choice(MODIFIERS)} {random.choice(NICHES)} {random.choice(PRODUCTS)}"
            if kw not in df['keyword'].values:
                new_items.append({"keyword": kw, "status": "pending", "date_launched": ""})
        
        df = pd.concat([df, pd.DataFrame(new_items)], ignore_index=True)
    return df

def update_sitemap(df):
    """Rebuilds the sitemap.xml for Google Crawlers."""
    now = datetime.date.today().isoformat()
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.append(f'  <url><loc>https://{HOST}/</loc><lastmod>{now}</lastmod><priority>1.0</priority></url>')
    
    completed = df[df['status'] == 'completed']
    for _, row in completed.iterrows():
        slug = str(row['keyword']).replace(" ", "-").lower()
        xml.append(f'  <url><loc>https://{HOST}/sites/{slug}/</loc><lastmod>{now}</lastmod><priority>0.8</priority></url>')
    
    xml.append('</urlset>')
    with open('sitemap.xml', 'w') as f:
        f.write('\n'.join(xml))

def run_engine():
    # 1. Load or Initialize CSV
    if os.path.exists('keywords.csv'):
        df = pd.read_csv('keywords.csv')
    else:
        df = pd.DataFrame(columns=['keyword', 'status', 'date_launched'])

    # 2. Refill if necessary
    df = refill_keywords(df)
    
    # 3. Grab the next 10 items
    batch = df[df['status'] == 'pending'].head(10)
    if batch.empty:
        print("No pending keywords found.")
        return

    for index, row in batch.iterrows():
        kw = row['keyword']
        slug = str(kw).replace(" ", "-").lower()
        os.makedirs(f"sites/{slug}", exist_ok=True)
        
        # HTML Content with SEO Schema & Affiliate Link
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8"><title>Custom {kw} | Shop Now</title>
            <script type="application/ld+json">
            {{"@context":"https://schema.org/","@type":"Product","name":"{kw}","brand":{{"@type":"Brand","name":"Brightlane"}},"offers":{{"@type":"Offer","url":"{AFFILIATE_URL}","priceCurrency":"USD","price":"24.99","availability":"https://schema.org/InStock"}}}}
            </script>
            <style>body{{font-family:sans-serif;text-align:center;padding:100px;background:#f4f4f9;}} .card{{background:#fff;padding:50px;border-radius:20px;display:inline-block;box-shadow:0 10px 20px rgba(0,0,0,0.1);}} .btn{{background:#00e676;color:#000;padding:20px 40px;text-decoration:none;border-radius:50px;font-weight:bold;}}</style>
        </head>
        <body>
            <div class="card">
                <h1>Exclusive {kw}</h1>
                <p>Limited edition custom {kw} designs. High quality guaranteed.</p>
                <br><br>
                <a href="{AFFILIATE_URL}" class="btn">BUY ON PRINTIFY</a>
            </div>
        </body>
        </html>"""
        
        with open(f"sites/{slug}/index.html", "w") as f:
            f.write(html)
        
        df.at[index, 'status'] = 'completed'
        df.at[index, 'date_launched'] = datetime.date.today().isoformat()
        print(f"Generated: {kw}")

    # 4. Save and Update
    df.to_csv('keywords.csv', index=False)
    update_sitemap(df)

if __name__ == "__main__":
    run_engine()
