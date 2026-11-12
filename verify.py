import re
import sys
import urllib.request

BASE = 'http://localhost:8080'
PAGES = [
    'index.html',
    'acquire.html',
    'how-we-rate.html',
    'reviews/clickcease.html',
    'reviews/trafficguard.html',
    'reviews/spider-af.html',
    'reviews/anura.html',
    'compare/clickcease-vs-trafficguard.html',
    'compare/clickcease-vs-spider-af.html',
    'guides/clickcease-alternatives.html',
    'guides/does-google-refund-invalid-clicks.html',
    'guides/click-fraud-on-meta-ads.html',
    'guides/best-click-fraud-tool-small-business.html',
    'guides/what-is-click-fraud.html',
    'guides/how-to-detect-click-fraud.html',
    'sitemap.xml',
    'robots.txt',
]


def fetch(path):
    return urllib.request.urlopen(f'{BASE}/{path}').read().decode('utf-8')


def check(label, condition):
    print(f'{"PASS" if condition else "FAIL"}  {label}')
    return bool(condition)


failures = 0

# All pages respond.
for page in PAGES:
    try:
        fetch(page)
        print(f'PASS  HTTP 200 {page}')
    except Exception as exc:  # noqa: BLE001 - simple CLI verifier
        print(f'FAIL  HTTP {page}: {exc}')
        failures += 1

content = fetch('index.html')

checks = [
    ('Threat banner removed', 'THREAT LEVEL' not in content),
    ('Hero CTA anchors to calculator', 'href="#calculator" class="nav-aff-btn"' in content),
    ('Hero uses 22% framing', '22% of your PPC budget' in content),
    ('Source superscripts present', content.count('class="source-link"') == 2),
    ('Recoverable conversions removed', 'Recoverable Conversions' not in content),
    ('SITE_CONFIG present', 'const SITE_CONFIG' in content),
    ('Spend threshold configured', 'spendThreshold: 5000' in content),
    ('Dynamic calculator CTA', 'buildRecommendationMarkup' in content),
    ('Affiliate links are sponsored', 'rel="sponsored noopener"' in content),
    ('Affiliate links open new tab', 'target="_blank"' in content),
    ('Affiliate disclosure near matrix', 'We may earn a commission' in content),
    ('Inspector below matrix', content.index('id="inspector"') > content.index('id="compare"')),
    ('Inspector retitled', 'Curious? See What Fraud Tools See About Your Browser' in content),
    ('Inspector copy line', 'This checks your browser, not your ad traffic.' in content),
    ('Inspector CTA links to compare', '<a href="#compare" class="btn">Compare Tools' in content),
    ('Free trial column', '<th>Free Trial</th>' in content),
    ('Last verified placeholder', 'Last verified: {{DATE}}' in content),
    ('Tool names link to reviews', 'href="reviews/clickcease.html"' in content),
    ('How we rate link', 'href="how-we-rate.html"' in content),
    ('Domain block removed from index', 'Premium Domain' not in content),
    ('Acquisition footer link', 'href="acquire.html">Acquisition inquiries' in content),
    ('Mobile compare button', 'id="mobileCompareBtn"' in content),
    ('Mobile compare hidden in view', 'entry.isIntersecting' in content),
    ('Email endpoint placeholder', '{{EMAIL_PROVIDER_FORM_ACTION}}' in content),
    ('Email source field', 'name="source"' in content),
    ('Email success links to compare', 'Compare tools →' in content),
    ('Organization schema', '"@type": "Organization"' in content),
    ('WebSite schema', '"@type": "WebSite"' in content),
    ('Twitter meta', 'name="twitter:card"' in content),
    ('OG meta', 'property="og:title"' in content),
    ('All FAQ answers link to guides', content.count('Read the full guide →') == 4),
]
for label, condition in checks:
    failures += 0 if check(label, condition) else 1

print(f'\n{"All checks passed" if failures == 0 else f"{failures} check(s) failed"}')
sys.exit(1 if failures else 0)
