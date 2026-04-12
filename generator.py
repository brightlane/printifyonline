import pandas as pd
import os
import datetime

# --- CONFIG ---
AFFILIATE_URL = "https://try.printify.com/r3xsnwqufe8t"
HOST = "brightlane.github.io"

def update_sitemap(all_keywords):
    now = datetime.date.today().isoformat()
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap.org/0.9">']
    
    # Home Page
    xml.append(f'<url><loc>https://{HOST}/</loc><lastmod>{now}</lastmod><priority>1.0</priority></url>')
    
    # Only add 'completed' sites to the sitemap
    for index, row in all_keywords[all_keywords['status'] == 'completed'].iterrows():
        slug = row['keyword'].replace(" ", "-").lower()
        xml.append(f'<url><loc>https://{HOST}/sites/{slug}/</loc><lastmod>{now}</lastmod><priority>0.8</priority></url>')
    
    xml.append('</urlset>')
    with open('sitemap.xml', 'w') as f:
        f.write('\n'.join(xml))

def run_engine():
    df = pd.read_csv('keywords.csv')
    batch = df[df['status'] == 'pending'].head(10)
    
    if batch.empty:
        print("No pending keywords left!")
        return

    for index, row in batch.iterrows():
        kw = row['keyword']
        slug = kw.replace(" ", "-").lower()
        os.makedirs(f"sites/{slug}", exist_ok=True)
        
        # Optimized HTML with your Printify Link
        html = f"""
        <html>
        <head><title>{kw} | Custom Shop</title></head>
        <body style="text-align:center; padding:50px; font-family:sans-serif;">
            <h1>Custom {kw} Designs</h1>
            <p>Premium quality print-on-demand items.</p>
            <a href="{AFFILIATE_URL}" style="background:#00e676; color:black; padding:20px; text-decoration:none; border-radius:50px; font-weight:bold;">SHOP ON PRINTIFY</a>
        </body>
        </html>"""
        
        with open(f"sites/{slug}/index.html", "w") as f:
            f.write(html)
            
        df.at[index, 'status'] = 'completed'
        df.at[index, 'date_launched'] = datetime.date.today().isoformat()

    # Save CSV and Update Sitemap
    df.to_csv('keywords.csv', index=False)
    update_sitemap(df)

if __name__ == "__main__":
    run_engine()
