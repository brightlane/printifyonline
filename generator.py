import pandas as pd
import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- CONFIGURATION ---
AFFILIATE_URL = "https://try.printify.com/r3xsnwqufe8t"
HOST = "brightlane.github.io" # Update this if you use a new domain

# --- GOOGLE AUTHENTICATION ---
def get_google_service():
    # Pulls the JSON key from the GitHub Secret you set up in Step 2
    service_info = json.loads(os.getenv("GOOGLE_JSON_KEY"))
    credentials = service_account.Credentials.from_service_account_info(service_info)
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/indexing'])
    return build('indexing', 'v3', credentials=scoped_credentials)

# --- GOOGLE INDEXING PING ---
def ping_google(url, service):
    body = {"url": url, "type": "URL_UPDATED"}
    try:
        service.urlNotifications().publish(body=body).execute()
        print(f"Google Indexed: {url}")
    except Exception as e:
        print(f"Google API Error for {url}: {e}")

# --- SCHEMA GENERATOR (For Google Rich Results) ---
def generate_schema(keyword):
    return f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": "{keyword}",
      "description": "Custom {keyword} available now. High-quality print-on-demand.",
      "brand": {{ "@type": "Brand", "name": "Brightlane Printify" }},
      "offers": {{
        "@type": "Offer",
        "url": "{AFFILIATE_URL}",
        "priceCurrency": "USD",
        "price": "29.99",
        "availability": "https://schema.org/InStock"
      }}
    }}
    </script>
    """

def run_engine():
    if not os.path.exists('keywords.csv'): return
    
    df = pd.read_csv('keywords.csv')
    batch = df[df['status'] == 'pending'].head(10)
    
    if batch.empty: return

    service = get_google_service()
    new_urls = []

    for index, row in batch.iterrows():
        kw = row['keyword']
        slug = kw.replace(" ", "-").lower()
        os.makedirs(f"sites/{slug}", exist_ok=True)
        
        # Build the HTML with your Schema and Affiliate Link
        html_content = f"""
        <html>
        <head>
            <title>{kw} | Custom Designs</title>
            {generate_schema(kw)}
            <style>body{{font-family:sans-serif; text-align:center; padding:50px;}} .btn{{background:#00e676; padding:20px; color:black; text-decoration:none; border-radius:50px; font-weight:bold;}}</style>
        </head>
        <body>
            <h1>Get your custom {kw}</h1>
            <p>High quality, fast shipping, and unique designs.</p>
            <br><br>
            <a href="{AFFILIATE_URL}" class="btn">SHOP NOW ON PRINTIFY</a>
        </body>
        </html>
        """
        
        with open(f"sites/{slug}/index.html", "w") as f:
            f.write(html_content)
        
        url = f"https://{HOST}/sites/{slug}/"
        new_urls.append(url)
        ping_google(url, service)
        
        df.at[index, 'status'] = 'completed'
        df.at[index, 'date_launched'] = datetime.date.today().isoformat()

    df.to_csv('keywords.csv', index=False)

if __name__ == "__main__":
    run_engine()
