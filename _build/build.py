"""Builds the static site: every page, sitemap.xml, robots.txt, llms.txt, the web manifest and security.txt.

Run from anywhere:  python _build/build.py
Products, companies and contact details live once, below; edit them here and rebuild.
Jekyll skips folders starting with "_", so this script is not published.
"""
import json
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://sentrywave.com"
TODAY = date.today().isoformat()

EMAIL = "info@sentrywave.com"
PHONE = "+263782135087"
PHONE_SHOWN = "+263 78 213 5087"
CIPZ = "https://cipz.pfms.gov.zw:8090/Info/Checkacompany?={}"

SOCIAL = {
    "LinkedIn": "https://www.linkedin.com/company/sentrywave",
    "Facebook": "https://www.facebook.com/sentrywave",
    "X": "https://twitter.com/sentrywave",
    "GitHub": "https://github.com/sentrywave",
}

COMPANIES = {
    "sentrywave": {
        "name": "Sentrywave (Private) Limited", "short": "Sentrywave", "no": "104894A1042026", "css": "",
        "about": "Software development, payments and online platforms. Builds and runs SentryWave Hotspot and Dariro.",
    },
    "siteaxis": {
        "name": "SiteAxis Enterprises (Private) Limited", "short": "SiteAxis Enterprises", "no": "139680A0292026", "css": " siteaxis",
        "about": "Building materials supply and delivery. Trades as BuildMate.",
    },
}

PRODUCTS = [
    {
        "key": "hotspot", "name": "SentryWave Hotspot", "url": "https://hotspot.sentrywave.com/", "domain": "hotspot.sentrywave.com",
        "company": "sentrywave", "category": "WiFi hotspot billing",
        "headline": "Sell WiFi access. Get paid by mobile money.",
        "summary": "A billing platform for WiFi providers. Customers join your WiFi, pick a package and pay with EcoCash, InnBucks or O'mari, and their token reaches your router automatically.",
        "points": [
            "Customers pay on their phone with EcoCash, InnBucks or O'mari",
            "Tokens are created on the router for you, and stock tops itself up",
            "Works with MikroTik and Ruijie, even without a public IP",
        ],
        "chips": ["MikroTik", "Ruijie", "RADIUS", "Mobile money"],
        "shot": "hotspot.webp", "shot_alt": "The SentryWave Hotspot home page, showing a phone choosing a WiFi package and paying by mobile money",
    },
    {
        "key": "dariro", "name": "Dariro", "url": "https://dariro.co.zw/", "domain": "dariro.co.zw",
        "company": "sentrywave", "category": "Paid social media promotion",
        "headline": "Brands pay. Promoters post. Everyone gets what they paid for.",
        "summary": "Paid promotion on social media in Zimbabwe. Brands put their song, show, shop or cause in front of real followers, and Dariro holds the money until the post is up.",
        "points": [
            "A brand's money is held from the moment a promoter takes the job, and returned if nobody posts",
            "Every promoter profile is checked: no bought likes, no fake followers",
            "Promoters are paid to their wallet within 48 hours, and cash out to EcoCash",
        ],
        "chips": ["TikTok", "Instagram", "Facebook", "X", "YouTube"],
        "shot": "dariro.webp", "shot_alt": "The Dariro home page: Brands pay. Promoters post. Everyone gets what they paid for.",
    },
    {
        "key": "buildmate", "name": "BuildMate", "url": "https://buildmate.co.zw/", "domain": "buildmate.co.zw",
        "company": "siteaxis", "category": "Building materials delivery",
        "headline": "Bricks, sand and stone delivered. Priced in 30 seconds.",
        "summary": "Compare brick yards and quarries around Harare, see the full delivered price to your site, and order online or on WhatsApp.",
        "points": [
            "Prices straight from the yards, with delivery and road fees included",
            "Pay with EcoCash, OneMoney, card or bank transfer, or on delivery",
            "Building from abroad? Pay by Visa or Mastercard and we deliver to your site",
        ],
        "chips": ["Harare", "Chitungwiza", "Ruwa", "Norton", "Marondera"],
        "shot": "buildmate.webp", "shot_alt": "The BuildMate home page with an instant delivered-price calculator for bricks",
    },
]


# ---------------------------------------------------------------- icons

def icon(body, sw=2):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>')

I = {
    "arrow": icon('<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>'),
    "tick": icon('<circle cx="12" cy="12" r="10"/><path d="m8.5 12 2.5 2.5 4.5-5"/>'),
    "lock": icon('<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>', 2.4),
    "shield": icon('<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>'),
    "mail": icon('<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>'),
    "phone": icon('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>'),
    "pin": icon('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>'),
    "menu": icon('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "wifi": icon('<path d="M2 9a15 15 0 0 1 20 0"/><path d="M5 12.5a10 10 0 0 1 14 0"/><path d="M8.5 16a5 5 0 0 1 7 0"/><path d="M12 19.5h.01"/>', 2.2),
}

def brand(path):
    return f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="{path}"/></svg>'

SOCIAL_ICONS = {
    "LinkedIn": brand("M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"),
    "Facebook": brand("M24 12.07C24 5.41 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.04V9.41c0-3.02 1.8-4.7 4.54-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.89v2.26h3.33l-.53 3.5h-2.8V24C19.62 23.1 24 18.1 24 12.07"),
    "X": brand("M18.9 1.15h3.68l-8.04 9.19L24 22.85h-7.4l-5.8-7.58-6.63 7.58H.49l8.6-9.83L0 1.15h7.59l5.24 6.93 6.07-6.93Zm-1.3 19.5h2.04L6.48 3.24H4.3l13.3 17.41Z"),
    "GitHub": brand("M12 .3a12 12 0 0 0-3.8 23.38c.6.12.83-.26.83-.57L9 21.07c-3.34.72-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.08-.74.09-.73.09-.73 1.2.09 1.83 1.24 1.83 1.24 1.07 1.83 2.81 1.3 3.5 1 .1-.78.42-1.31.76-1.61-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.14-.3-.54-1.52.1-3.18 0 0 1-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.28-1.55 3.29-1.23 3.29-1.23.64 1.66.24 2.88.12 3.18a4.65 4.65 0 0 1 1.23 3.22c0 4.61-2.8 5.63-5.48 5.92.42.36.81 1.1.81 2.22l-.01 3.29c0 .31.2.69.82.57A12 12 0 0 0 12 .3"),
}


def arcs(dome="#121212", cls="arcs"):
    """The three rings of the Sentrywave logo, drawn as a background motif."""
    return (f'<svg class="{cls}" viewBox="0 0 200 100" aria-hidden="true" focusable="false">'
            f'<path d="M9 100a91 91 0 0 1 182 0" stroke="#f26624" stroke-width="18"/>'
            f'<path d="M37 100a63 63 0 0 1 126 0" stroke="#0071bb" stroke-width="18"/>'
            f'<path d="M64 100a36 36 0 0 1 72 0z" fill="{dome}"/></svg>')


def window(p, eager=False, cls=""):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<div class="window{cls}"><div class="window-bar"><span class="dots"><i></i><i></i><i></i></span>'
            f'<span class="url">{I["lock"]}{p["domain"]}</span></div>'
            f'<img src="/assets/img/products/{p["shot"]}" width="1200" height="750" alt="{escape(p["shot_alt"])}" {load} decoding="async"></div>')


def mark(p):
    if p["key"] == "hotspot":
        return f'<span class="mark" style="background:#1d64d8;color:#fff">{I["wifi"]}</span>'
    if p["key"] == "dariro":
        return '<span class="mark"><img src="/assets/img/products/dariro-mark.png" width="128" height="128" alt=""></span>'
    return '<span class="mark" style="background:#fff"><img src="/assets/img/products/buildmate-mark.png" width="256" height="256" alt=""></span>'


# ---------------------------------------------------------------- structured data

ORG_ID = f"{SITE}/#organization"

def org_graph():
    sw, sa = COMPANIES["sentrywave"], COMPANIES["siteaxis"]
    return [
        {
            "@type": "Organization", "@id": ORG_ID, "name": "Sentrywave", "legalName": sw["name"],
            "alternateName": ["Sentrywave (Pvt) Ltd", "SentryWave"],
            "url": SITE + "/", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/brand/icon-512.png", "width": 512, "height": 512},
            "image": f"{SITE}/assets/img/brand/og-image.png",
            "description": "Zimbabwean software company that builds and runs SentryWave Hotspot and Dariro, and builds software and payment integrations for clients.",
            "email": EMAIL, "telephone": PHONE,
            "address": {"@type": "PostalAddress", "addressLocality": "Harare", "addressCountry": "ZW"},
            "areaServed": {"@type": "Country", "name": "Zimbabwe"},
            "identifier": {"@type": "PropertyValue", "propertyID": "CIPZ company number", "value": sw["no"]},
            "sameAs": list(SOCIAL.values()),
            "knowsAbout": ["Software development", "Mobile money payments", "EcoCash", "WiFi hotspot billing", "Online marketplaces", "Influencer marketing"],
            "brand": [{"@type": "Brand", "name": p["name"], "url": p["url"]} for p in PRODUCTS if p["company"] == "sentrywave"],
            "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", "email": EMAIL, "telephone": PHONE, "areaServed": "ZW", "availableLanguage": "English"}],
        },
        {
            "@type": "Organization", "@id": f"{SITE}/#siteaxis", "name": "SiteAxis Enterprises", "legalName": sa["name"],
            "address": {"@type": "PostalAddress", "addressLocality": "Harare", "addressCountry": "ZW"},
            "identifier": {"@type": "PropertyValue", "propertyID": "CIPZ company number", "value": sa["no"]},
            "brand": [{"@type": "Brand", "name": "BuildMate", "url": "https://buildmate.co.zw/"}],
        },
        {
            "@type": "WebSite", "@id": f"{SITE}/#website", "url": SITE + "/", "name": "Sentrywave",
            "inLanguage": "en", "publisher": {"@id": ORG_ID},
        },
    ]


def products_ld():
    return {
        "@type": "ItemList", "@id": f"{SITE}/#products", "name": "Products built by Sentrywave",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {
                "@type": "WebApplication" if p["key"] != "buildmate" else "OnlineStore",
                "name": p["name"], "url": p["url"], "description": p["summary"],
                **({"applicationCategory": "BusinessApplication", "operatingSystem": "Web"} if p["key"] != "buildmate" else {}),
                "provider": {"@id": ORG_ID} if p["company"] == "sentrywave" else {"@id": f"{SITE}/#siteaxis"},
            }} for i, p in enumerate(PRODUCTS)
        ],
    }


def breadcrumbs(path, title):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": title, "item": f"{SITE}/{path}"},
    ]}


def ld(nodes):
    data = json.dumps({"@context": "https://schema.org", "@graph": nodes}, indent=2, ensure_ascii=False)
    return f'\n    <script type="application/ld+json">\n{data}\n    </script>'


# ---------------------------------------------------------------- layout

NAV = [("/", "Home"), ("/#products", "Products"), ("/about.html", "About"), ("/contact.html", "Contact")]


def head(path, title, desc, nodes=(), noindex=False, preload=None):
    url = SITE + "/" + ("" if path == "index.html" else path)
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    pre = f'\n    <link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="{escape(desc)}">
    <meta name="robots" content="{robots}">
    <link rel="canonical" href="{url}">
    <meta name="author" content="Sentrywave (Private) Limited">
    <meta name="geo.region" content="ZW-HA">
    <meta name="geo.placename" content="Harare">
    <meta name="theme-color" content="#ffffff">
    <meta name="color-scheme" content="light">
    <meta name="format-detection" content="telephone=no">

    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Sentrywave">
    <meta property="og:locale" content="en_ZW">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{escape(desc)}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{SITE}/assets/img/brand/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="Sentrywave logo">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@sentrywave">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{escape(desc)}">
    <meta name="twitter:image" content="{SITE}/assets/img/brand/og-image.png">

    <link rel="icon" href="/favicon.ico" sizes="32x32">
    <link rel="icon" href="/assets/img/brand/icon-192.png" type="image/png" sizes="192x192">
    <link rel="apple-touch-icon" href="/assets/img/brand/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">
    <link rel="alternate" type="text/plain" href="/llms.txt" title="LLM-readable summary">
    <link rel="sitemap" type="application/xml" href="/sitemap.xml">{pre}
    <link rel="stylesheet" href="/assets/css/site.css">
    <script>document.documentElement.classList.add('js')</script>
    <script src="/assets/js/site.js" defer></script>{ld(list(nodes)) if nodes else ""}
</head>
<body>
    <a class="skip-link" href="#main">Skip to content</a>
"""


def header(active):
    cur = ' aria-current="page"'
    links = "\n".join(
        f'                    <li><a href="{h}"{cur if h == active else ""}>{l}</a></li>' for h, l in NAV)
    return f"""
    <header class="site-header">
        <div class="container">
            <a class="brand" href="/" aria-label="Sentrywave, home"><img src="/assets/img/brand/sentrywave-logo.png" width="362" height="160" alt="Sentrywave"></a>
            <button class="nav-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu">{I["menu"]}</button>
            <nav class="nav" id="site-nav" aria-label="Main">
                <ul>
{links}
                </ul>
                <a class="btn btn-accent btn-sm" href="/contact.html">Start a project</a>
            </nav>
        </div>
    </header>
"""


def footer():
    social = "\n".join(f'                        <a href="{u}" rel="me noopener" aria-label="Sentrywave on {n}">{SOCIAL_ICONS[n]}</a>' for n, u in SOCIAL.items())
    prods = "\n".join(f'                        <li><a href="{p["url"]}" rel="noopener">{p["name"]}</a></li>' for p in PRODUCTS)
    legal = "\n".join(
        f'            <p>{c["name"]} &middot; company no. {c["no"]} &middot; '
        f'<a href="{CIPZ.format(c["no"])}" target="_blank" rel="noopener noreferrer">Verify on the CIPZ register</a></p>'
        for c in COMPANIES.values())
    return f"""
    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="/" aria-label="Sentrywave, home"><img src="/assets/img/brand/sentrywave-logo-white.png" width="362" height="160" alt="Sentrywave" loading="lazy"></a>
                    <p>We build software and run it as real businesses, from Harare, for Zimbabwe.</p>
                    <div class="social">
{social}
                    </div>
                </div>
                <nav aria-label="Products">
                    <h4>Products</h4>
                    <ul>
{prods}
                    </ul>
                </nav>
                <nav aria-label="Company">
                    <h4>Company</h4>
                    <ul>
                        <li><a href="/about.html">About</a></li>
                        <li><a href="/contact.html">Contact</a></li>
                        <li><a href="/privacy.html">Privacy policy</a></li>
                        <li><a href="/terms.html">Terms &amp; conditions</a></li>
                    </ul>
                </nav>
                <div>
                    <h4>Contact</h4>
                    <address style="font-style:normal">
                        <ul>
                            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
                            <li><a href="tel:{PHONE}">{PHONE_SHOWN}</a></li>
                            <li>Harare, Zimbabwe</li>
                        </ul>
                    </address>
                </div>
            </div>
        </div>
        <div class="container legal">
            <p>&copy; <span id="year">{date.today().year}</span> Sentrywave (Private) Limited. All rights reserved.</p>
{legal}
            <p>EcoCash, InnBucks, O'mari, MikroTik and Ruijie are trademarks of their owners, shown to identify payment methods and hardware our products support. No endorsement is implied.</p>
        </div>
        <div class="footer-stripe" aria-hidden="true"><i></i><i></i><i></i></div>
    </footer>
</body>
</html>
"""


def page_hero(eyebrow, title, lead=""):
    lead = f'\n                <p class="lead">{lead}</p>' if lead else ""
    return f"""
        <section class="page-hero">
            {arcs()}
            <div class="container">
                <span class="eyebrow"><span class="dot"></span>{eyebrow}</span>
                <h1>{title}</h1>{lead}
            </div>
        </section>
"""


def company_cards():
    out = []
    for key, c in COMPANIES.items():
        runs = ", ".join(p["name"] for p in PRODUCTS if p["company"] == key)
        out.append(f"""                <article class="company{c["css"]} reveal">
                    <div class="kicker">Registered in Zimbabwe</div>
                    <h3>{c["name"]}</h3>
                    <p>{c["about"]}</p>
                    <dl>
                        <dt>Company number</dt><dd class="mono">{c["no"]}</dd>
                        <dt>Registry</dt><dd>CIPZ, Zimbabwe</dd>
                        <dt>Runs</dt><dd>{runs}</dd>
                    </dl>
                    <a class="link-arrow verify" href="{CIPZ.format(c["no"])}" target="_blank" rel="noopener noreferrer">{I["shield"]} Verify on the CIPZ register</a>
                </article>""")
    return "\n".join(out)


def cta():
    return f"""
        <section class="section" style="padding-top:0">
            <div class="container">
                <div class="cta reveal">
                    {arcs("#ffffff")}
                    <div>
                        <h2>Have something to build?</h2>
                        <p>Tell us about the product, the payments it needs to take, and who will use it. We'll tell you honestly how we'd build it.</p>
                    </div>
                    <div class="actions">
                        <a class="btn btn-accent" href="/contact.html">Start a project {I["arrow"]}</a>
                        <a class="btn btn-line" href="mailto:{EMAIL}">{EMAIL}</a>
                    </div>
                </div>
            </div>
        </section>
"""


PARTNERS = f"""
        <section class="partners" aria-label="Payment methods and hardware our products support">
            <div class="container">
                <div class="group">
                    <span class="label">Payments</span>
                    <img src="/assets/img/partners/ecocash.webp" width="225" height="42" alt="EcoCash" loading="lazy">
                    <img class="tall" src="/assets/img/partners/innbucks.webp" width="302" height="120" alt="InnBucks" loading="lazy">
                    <img class="tall" src="/assets/img/partners/omari.webp" width="297" height="120" alt="O'mari" loading="lazy">
                </div>
                <div class="group">
                    <span class="label">Routers</span>
                    <img src="/assets/img/partners/mikrotik.svg" width="259" height="45" alt="MikroTik" loading="lazy" style="height:22px">
                    <img src="/assets/img/partners/ruijie.svg" width="155" height="46" alt="Ruijie" loading="lazy" style="height:28px">
                </div>
            </div>
        </section>
"""


# ---------------------------------------------------------------- pages

def index():
    h, d, b = PRODUCTS
    rows = []
    for i, p in enumerate(PRODUCTS):
        c = COMPANIES[p["company"]]
        ticks = "\n".join(f'                        <li>{I["tick"]}<span>{t}</span></li>' for t in p["points"])
        chips = "".join(f'<span class="chip">{x}</span>' for x in p["chips"])
        dome = "#ffd23f" if p["key"] == "dariro" else "#121212"
        rows.append(f"""
            <article class="product p-{p["key"]}{" flip" if i % 2 else ""}" id="{p["key"]}">
                <div class="product-copy reveal">
                    <div class="product-brand">
                        {mark(p)}
                        <div><div class="name">{p["name"]}</div><div class="domain">{p["category"]} &middot; {p["domain"]}</div></div>
                    </div>
                    <h3>{p["headline"]}</h3>
                    <p>{p["summary"]}</p>
                    <ul class="ticks">
{ticks}
                    </ul>
                    <div class="chips">{chips}</div>
                    <div class="meta">
                        <a class="btn btn-primary" href="{p["url"]}" rel="noopener">Visit {p["domain"]} {I["arrow"]}</a>
                        <span class="operator">Run by <strong>{c["name"]}</strong></span>
                    </div>
                </div>
                <div class="product-media reveal">
                    {arcs(dome)}
                    {window(p)}
                </div>
            </article>""")
    rows = "\n".join(rows)

    services = [
        ("01", "Product engineering", "Web and mobile applications, back ends and admin tools, built to be maintained for years by people who will still be here.", ["Web", "Mobile", "APIs", "Admin tools"]),
        ("02", "Payments that work here", "Checkout that takes EcoCash, InnBucks, O'mari, OneMoney, cards and bank transfers, and reconciles itself. We run these flows in our own products every day.", ["Mobile money", "Cards", "Reconciliation"]),
        ("03", "Hosting and operations", "Deployment, monitoring, backups and support. Our own businesses depend on the same setup, so it gets looked after.", ["Cloud", "Monitoring", "Backups", "Support"]),
    ]
    svc = "\n".join(f"""                <article class="service reveal">
                    <span class="num">{n}</span>
                    <h3>{t}</h3>
                    <p>{x}</p>
                    <ul>{"".join(f"<li>{c}</li>" for c in cs)}</ul>
                </article>""" for n, t, x, cs in services)

    desc = ("Sentrywave is a Harare software company that builds and runs SentryWave Hotspot (WiFi billing by mobile money), "
            "Dariro (paid social media promotion) and, through SiteAxis Enterprises, BuildMate (building materials delivery).")
    return head("index.html", "Sentrywave | Software company in Harare, Zimbabwe", desc,
                org_graph() + [products_ld()], preload="/assets/img/products/hotspot.webp") + header("/") + f"""
    <main id="main">
        <section class="hero">
            {arcs()}
            <div class="container hero-grid">
                <div class="hero-copy">
                    <span class="eyebrow"><span class="dot"></span>Software company &middot; Harare, Zimbabwe</span>
                    <h1>We build the software. <span class="hl">Then we run the business on it.</span></h1>
                    <p class="lead">Sentrywave designs, builds and operates digital products for Zimbabwe: WiFi billing, paid social promotion and building materials delivery, all taking payment the way people here actually pay.</p>
                    <div class="actions">
                        <a class="btn btn-primary" href="#products">See our products {I["arrow"]}</a>
                        <a class="btn btn-line" href="/contact.html">Start a project</a>
                    </div>
                    <div class="hero-facts">
                        <div><strong>3</strong><span>products live</span></div>
                        <div><strong>2</strong><span>registered companies</span></div>
                        <div><strong>6+</strong><span>ways to pay supported</span></div>
                    </div>
                </div>
                <div class="stack" aria-hidden="true">
                    {window(b, cls=" w1")}
                    {window(d, cls=" w2")}
                    {window(h, eager=True, cls=" w3")}
                </div>
            </div>
        </section>
{PARTNERS}
        <section class="section" id="products">
            <div class="container">
                <div class="section-head reveal">
                    <span class="eyebrow"><span class="dot"></span>Our products</span>
                    <h2>Three businesses, built and run in-house</h2>
                    <p>Each one has its own customers, support and payments. They're also where we prove the tools we build for clients.</p>
                </div>
{rows}
            </div>
        </section>

        <section class="section section-dark" id="services">
            {arcs("#ffffff")}
            <div class="container" style="position:relative">
                <div class="section-head reveal">
                    <span class="eyebrow"><span class="dot"></span>Work with us</span>
                    <h2>What we build for clients</h2>
                    <p>The same team, the same stack and the same standards as our own products.</p>
                </div>
                <div class="grid grid-3">
{svc}
                </div>
            </div>
        </section>

        <section class="section section-sand" id="companies">
            <div class="container">
                <div class="section-head reveal">
                    <span class="eyebrow"><span class="dot"></span>Who we are</span>
                    <h2>Registered companies you can check</h2>
                    <p>Our products are run by two companies registered with the Companies and Intellectual Property Office of Zimbabwe (CIPZ). Each number links to the public register.</p>
                </div>
                <div class="grid grid-2">
{company_cards()}
                </div>
            </div>
        </section>

        <div style="height:112px"></div>
{cta()}
    </main>
""" + footer()


FAQ = [
    ("What does Sentrywave do?",
     "Sentrywave (Private) Limited is a software company in Harare, Zimbabwe. It builds and runs its own products, SentryWave Hotspot and Dariro, and builds software and payment integrations for clients."),
    ("Who runs BuildMate?",
     "BuildMate is run by SiteAxis Enterprises (Private) Limited, company number 139680A0292026, which trades as BuildMate."),
    ("Is Sentrywave a registered company?",
     "Yes. Sentrywave (Private) Limited is registered in Zimbabwe with company number 104894A1042026. You can check it on the CIPZ register."),
    ("Which payment methods do your products support?",
     "Depending on the product: EcoCash, InnBucks, O'mari, OneMoney, Visa and Mastercard cards, bank transfer, and cash on delivery."),
    ("How do I contact Sentrywave?",
     f"Email {EMAIL} or call {PHONE_SHOWN}. For help with a product, contact that product's team directly."),
]


def about():
    faq_ld = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    faq_html = "\n".join(f"""                    <details class="faq reveal">
                        <summary>{q}</summary>
                        <p>{a}</p>
                    </details>""" for q, a in FAQ)
    principles = [
        ("Design for the phone first", "Most people we serve browse and pay on a phone, often on a slow connection. Pages stay light and flows stay short."),
        ("Take the money people have", "Mobile money and local cards come first, with cash on delivery where it makes sense, and everything reconciled automatically."),
        ("Show the full price", "Customers see what they will pay before they pay it. No fees discovered at the end."),
        ("Run what we ship", "We host, monitor and support our own products. Client work gets the same treatment."),
    ]
    pr = "\n".join(f"""                    <div class="principle reveal"><h3>{t}</h3><p>{x}</p></div>""" for t, x in principles)
    desc = "About Sentrywave (Private) Limited, a Harare software company, and SiteAxis Enterprises (Private) Limited, the company behind BuildMate."
    return head("about.html", "About Sentrywave | Harare software company", desc,
                org_graph() + [breadcrumbs("about.html", "About"), faq_ld]) + header("/about.html") + f"""
    <main id="main">
{page_hero("About us", "A Zimbabwean software company that runs what it builds.",
           "Sentrywave started as a software development company. Today we also own and operate our own products, so the software we write for clients is held to the standard our own customers need.")}
        <section class="section">
            <div class="container split">
                <div class="reveal">
                    <span class="eyebrow"><span class="dot"></span>How we work</span>
                    <h2>Practical software for how Zimbabwe works</h2>
                    <div class="grid grid-2" style="margin-top:2.25rem;gap:32px 28px">
{pr}
                    </div>
                </div>
                <figure class="photo reveal" style="margin:0">
                    <img src="/assets/img/photos/truck-crane-loaded.webp" width="1200" height="791" alt="A BuildMate crane truck loaded with pallets of bricks at the yard" loading="lazy" decoding="async">
                    <figcaption>A BuildMate delivery, loaded at the yard in Harare</figcaption>
                </figure>
            </div>
        </section>

        <section class="section section-sand">
            <div class="container">
                <div class="section-head reveal">
                    <span class="eyebrow"><span class="dot"></span>Our companies</span>
                    <h2>Who runs what</h2>
                    <p>Both companies are registered in Zimbabwe. Check either on the CIPZ register.</p>
                </div>
                <div class="grid grid-2">
{company_cards()}
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container" style="max-width:860px">
                <div class="section-head reveal">
                    <span class="eyebrow"><span class="dot"></span>Questions</span>
                    <h2>Frequently asked</h2>
                </div>
                <div class="faqs">
{faq_html}
                </div>
            </div>
        </section>
{cta()}
    </main>
""" + footer()


def contact():
    h, d, b = PRODUCTS
    page_ld = {"@type": "ContactPage", "@id": f"{SITE}/contact.html", "url": f"{SITE}/contact.html", "name": "Contact Sentrywave", "about": {"@id": ORG_ID}}
    desc = f"Contact Sentrywave in Harare, Zimbabwe: {EMAIL}, {PHONE_SHOWN}. Support for SentryWave Hotspot, Dariro and BuildMate."
    return head("contact.html", "Contact Sentrywave | Harare, Zimbabwe", desc,
                org_graph() + [breadcrumbs("contact.html", "Contact"), page_ld]) + header("/contact.html") + f"""
    <main id="main">
{page_hero("Contact", "Let's talk.", "New project, payments integration, partnership, or a question about one of our products: this is the place.")}
        <section class="section">
            <div class="container contact-grid">
                <div class="panel reveal">
                    <h2 style="font-size:1.7rem">Sentrywave</h2>
                    <p style="color:var(--muted)">For new projects, partnerships and anything else.</p>
                    <ul class="contact-list">
                        <li><span class="ic">{I["mail"]}</span><div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
                        <li><span class="ic b">{I["phone"]}</span><div><small>Phone</small><a href="tel:{PHONE}">{PHONE_SHOWN}</a></div></li>
                        <li><span class="ic">{I["pin"]}</span><div><small>Office</small><span class="v">Harare, Zimbabwe</span></div></li>
                    </ul>
                    <a class="btn btn-accent" href="mailto:{EMAIL}?subject=New%20project">Email us about a project {I["arrow"]}</a>
                </div>
                <div class="reveal">
                    <h2 style="font-size:1.7rem">Product support</h2>
                    <p style="color:var(--muted)">If you use one of our products, its own team will answer fastest.</p>
                    <div class="support">
                        <div class="support-item">{mark(h)}<div><h3>SentryWave Hotspot</h3><p>Router setup, payments and tokens.</p><a href="{h["url"]}" rel="noopener">hotspot.sentrywave.com</a></div></div>
                        <div class="support-item">{mark(d)}<div><h3>Dariro</h3><p>Campaigns, promoters and payouts.</p><a href="mailto:support@dariro.co.zw">support@dariro.co.zw</a></div></div>
                        <div class="support-item">{mark(b)}<div><h3>BuildMate</h3><p>Prices, quotations and deliveries.</p><a href="mailto:sales@buildmate.co.zw">sales@buildmate.co.zw</a> &middot; <a href="tel:+263790090090">+263 790 090 090</a></div></div>
                    </div>
                </div>
            </div>
        </section>
    </main>
""" + footer()


PRIVACY = """                <p>Our chatbot is designed to offer paid AI services and other convenience tools to users who communicate
                    with it via WhatsApp. We are committed to protecting the privacy of our users and have implemented
                    measures to ensure that their personal information is safeguarded. This privacy policy outlines the
                    types of information we collect from users and how we use that information.</p>

                <h2>Information We Collect</h2>

                <p>When you interact with our chatbot, we may collect the following types of information:</p>

                <ol>
                    <li>Personal Information: We may collect your name, phone number, and other contact information that you
                        provide us when you sign up for our services or subscribe to our newsletter.</li>
                    <li>Conversational Data: We may collect information about your interactions with our chatbot, including
                        the messages you send and receive, the time and date of those messages, and any other data related
                        to your use of our services.</li>
                    <li>Payment Information: If you choose to purchase our services, we do not collect payment information,
                        such as your credit card number or other payment details.</li>
                </ol>

                <h2>How We Use Your Information</h2>

                <p>We use the information we collect from users to provide our services and improve the user experience.
                    Specifically, we may use your information for the following purposes:</p>

                <ol>
                    <li>To provide our services and respond to your requests.</li>
                    <li>To process payments for our services.</li>
                    <li>To communicate with you about our services, updates, and other relevant information.</li>
                    <li>To personalize your experience and improve our services.</li>
                    <li>To analyze user behavior and improve our chatbot's functionality.</li>
                </ol>

                <h2>Data Security</h2>

                <p>We take data security seriously and have implemented measures to protect the personal information we collect
                    from users. We use industry-standard encryption to secure data transmissions and follow best practices to
                    safeguard user data from unauthorized access, disclosure, or destruction.</p>

                <h2>Third-Party Providers</h2>

                <p>We may use third-party providers to help us deliver our services, process payments, and analyze user
                    behavior. These providers may have access to your personal information, but only to the extent necessary to
                    provide their services. We ensure that all third-party providers we work with are compliant with data
                    protection regulations and follow industry-standard security practices.</p>

                <h2>Updates to Our Privacy Policy</h2>

                <p>We may update this privacy policy from time to time to reflect changes in our services, industry
                    regulations, or other relevant factors. We recommend that users review this policy periodically to stay
                    informed of any changes.</p>"""

TERMS = """                <p>By using our service, you agree to comply with these terms and conditions. Please read them carefully
                    before using our chatbot.</p>

                <ol>
                    <li><strong>Payment:</strong> You will need tokens to use our chatbot service. You can purchase tokens in the app,
                        and we will charge your account. Tokens are non-refundable and non-transferable.</li>
                    <li><strong>Usage:</strong> Our chatbot service is for personal use only. You may not share your account with
                        anyone else. We may restrict or cancel your access to our service if we suspect that you have
                        violated this clause.</li>
                    <li><strong>Refunds:</strong> Refunds will only be made after thorough investigation and deliberation by our team.
                        We reserve the right to reject any refund request as we deem fit.</li>
                    <li><strong>Liability:</strong> We are not responsible for any damages or losses incurred by you or any third
                        party as a result of your use of our chatbot service. We are not liable for any damages or losses
                        that result from your phone getting into the wrong hands.</li>
                    <li><strong>Errors:</strong> We strive to provide accurate and error-free service. However, we cannot guarantee
                        that errors will not occur from time to time. We will make every effort to correct any errors as
                        soon as possible.</li>
                    <li><strong>Legal action:</strong> You agree not to take any legal action against us for any damages or losses
                        incurred by you or any third party as a result of your use of our chatbot service.</li>
                </ol>

                <p>We reserve the right to modify these terms and conditions at any time without prior notice. Your
                    continued use of our chatbot service after any modifications indicate that you agree to the
                    changes.</p>

                <p>If you have any questions or concerns about these terms and conditions, please contact us at
                    <a href="mailto:info@sentrywave.com">info@sentrywave.com</a>.</p>"""


def legal(path, title, desc, body):
    return head(path, f"{title} | Sentrywave", desc, [breadcrumbs(path, title)]) + header("") + f"""
    <main id="main">
{page_hero("Legal", title)}
        <section class="section">
            <div class="container prose">
{body}
            </div>
        </section>
    </main>
""" + footer()


def not_found():
    return head("404.html", "Page not found | Sentrywave", "The page you were looking for could not be found.", noindex=True) + header("") + f"""
    <main id="main">
{page_hero("404", "We couldn't find that page.", "It may have moved, or the link may be out of date.")}
        <section class="section" style="padding-top:64px">
            <div class="container" style="display:flex;gap:.75rem;flex-wrap:wrap">
                <a class="btn btn-primary" href="/">Back to home {I["arrow"]}</a>
                <a class="btn btn-line" href="/#products">See our products</a>
                <a class="btn btn-line" href="/contact.html">Contact us</a>
            </div>
        </section>
    </main>
""" + footer()


# ---------------------------------------------------------------- text files

def sitemap(pages):
    imgs = {
        "": [f"/assets/img/products/{p['shot']}" for p in PRODUCTS] + ["/assets/img/brand/og-image.png"],
        "about.html": ["/assets/img/photos/truck-crane-loaded.webp"],
    }
    urls = []
    for path, prio, freq in pages:
        im = "".join(f"\n    <image:image><image:loc>{SITE}{i}</image:loc></image:image>" for i in imgs.get(path, []))
        urls.append(f"  <url>\n    <loc>{SITE}/{path}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>{im}\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
            + "\n".join(urls) + "\n</urlset>\n")


ROBOTS = f"""# Everything here is public. Search engines and AI crawlers are welcome.
User-agent: *
Allow: /
Disallow: /404.html

Sitemap: {SITE}/sitemap.xml
"""


def llms():
    prods = "\n".join(
        f"- [{p['name']}]({p['url']}): {p['summary']} Run by {COMPANIES[p['company']]['name']}." for p in PRODUCTS)
    comps = "\n".join(
        f"- {c['name']}, company number {c['no']}. {c['about']} Verify: {CIPZ.format(c['no'])}" for c in COMPANIES.values())
    return f"""# Sentrywave

> Sentrywave (Private) Limited is a software company in Harare, Zimbabwe. It builds and runs its own products (SentryWave Hotspot and Dariro) and builds web and mobile software, mobile-money payment integrations and hosting for clients. BuildMate, a building materials delivery business, is run by the related company SiteAxis Enterprises (Private) Limited.

Key facts:

- Location: Harare, Zimbabwe. Serves customers across Zimbabwe.
- Contact: {EMAIL}, {PHONE_SHOWN}
- Payment methods supported across the products: EcoCash, InnBucks, O'mari, OneMoney, Visa, Mastercard, bank transfer, cash on delivery.
- Hardware supported by SentryWave Hotspot: MikroTik (RouterOS) and Ruijie/Reyee routers.

## Products

{prods}

## Companies

{comps}

## Pages

- [Home]({SITE}/): products, services and companies
- [About]({SITE}/about.html): how we work, who runs what, frequently asked questions
- [Contact]({SITE}/contact.html): email, phone and product support contacts

## Optional

- [Privacy policy]({SITE}/privacy.html): privacy policy for the Sentrywave WhatsApp chatbot
- [Terms and conditions]({SITE}/terms.html): terms for the Sentrywave WhatsApp chatbot
- [GitHub]({SOCIAL['GitHub']})
- [LinkedIn]({SOCIAL['LinkedIn']})
"""


MANIFEST = {
    "name": "Sentrywave", "short_name": "Sentrywave", "start_url": "/", "display": "browser",
    "background_color": "#ffffff", "theme_color": "#ffffff",
    "icons": [
        {"src": "/assets/img/brand/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/assets/img/brand/icon-512.png", "sizes": "512x512", "type": "image/png"},
    ],
}

SECURITY = f"""Contact: mailto:{EMAIL}
Expires: {date.today().year + 1}-12-31T23:59:59.000Z
Preferred-Languages: en
Canonical: {SITE}/.well-known/security.txt
"""


def main():
    files = {
        "index.html": index(),
        "about.html": about(),
        "contact.html": contact(),
        "privacy.html": legal("privacy.html", "Privacy Policy", "How Sentrywave collects, uses and protects information from users of its WhatsApp chatbot.", PRIVACY),
        "terms.html": legal("terms.html", "Terms &amp; Conditions", "Terms and conditions for using the Sentrywave WhatsApp chatbot.", TERMS),
        "404.html": not_found(),
        "sitemap.xml": sitemap([("", "1.0", "monthly"), ("about.html", "0.8", "monthly"), ("contact.html", "0.7", "yearly"),
                                ("privacy.html", "0.3", "yearly"), ("terms.html", "0.3", "yearly")]),
        "robots.txt": ROBOTS,
        "llms.txt": llms(),
        "site.webmanifest": json.dumps(MANIFEST, indent=2) + "\n",
        ".well-known/security.txt": SECURITY,
    }
    for name, text in files.items():
        p = ROOT / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")
        print("wrote", name)


if __name__ == "__main__":
    main()
