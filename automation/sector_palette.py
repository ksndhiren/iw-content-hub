"""Sector taxonomy and colours sourced from the Employers_SM_Ads sheet.

This is the durable "memory" used by featured-job graphics. Each sheet sector has
one assigned colour; styles are only used to pick the matching illustration family.
"""
import re

SECTOR_PALETTE_VERSION = "2026-08-19-employers-sm-ads-v1"
SECTORS = ['Accountancy', 'Administration', 'PA', 'VA', 'Aerospace', 'Agriculture', 'Environment', 'Architecture', 'Interior Design', 'Arts', 'Dance', 'Theater', 'Entertainment', 'Music', 'Automotive', 'Transportation', 'Business Management', 'Business Development', 'Charity', 'NGO', 'Social Services', 'Non Profit', 'Construction', 'Consulting', 'Customer Service', 'Graphic Design', 'Web Design', 'Distribution', 'Warehouse', 'Education', 'Teaching', 'Engineering (Break down in different fiels of Eng - then, code them!)', 'Events', 'Fashion', 'Luxury', 'Jewellery', 'Financial Services', 'Banking', 'Insurance', 'Freight', 'Logistics', 'Procurement', 'Health', 'Hospitality', 'Catering', 'HR', 'Recruitment', 'Information Technology (IT)', 'Web Development', 'Online Business', 'Mobile', 'Language', 'Translation', 'Legal', 'Market Research', 'Analysis', 'Marketing', 'Advertising', 'Social Media', 'Media', 'New Media', 'Miscellaneous', 'Photography', 'Videography', 'Project Management', 'Property Management', 'Real Estate', 'Public Relations (PR)', 'Communications', 'Public Sector', 'Government', 'Retail', 'Sales', 'Scientific', 'Pharmaceutical', 'Biotech', 'Security', 'Defence', 'Sports', 'Surveying', 'Telecommunications', 'Training', 'Development', 'Travel', 'Leisure', 'Energy', 'Water', 'Gas', 'Blockchain', 'Crypto currency']
SECTOR_COLORS = {'Accountancy': '#00A676', 'Administration': '#4F7CAC', 'PA': '#C02BD4', 'VA': '#B6D42B', 'Aerospace': '#2B85D4', 'Agriculture': '#D42B54', 'Environment': '#2BD434', 'Architecture': '#10B981', 'Interior Design': '#D4962B', 'Arts': '#2BD4C7', 'Dance': '#D42BAF', 'Theater': '#7ED42B', 'Entertainment': '#2B4DD4', 'Music': '#D43B2B', 'Automotive': '#2BD46C', 'Transportation': '#9D2BD4', 'Business Management': '#D4CE2B', 'Business Development': '#FF9F45', 'Charity': '#D42B77', 'NGO': '#46D42B', 'Social Services': '#422BD4', 'Non Profit': '#D4732B', 'Construction': '#C084FC', 'Consulting': '#D42BD2', 'Customer Service': '#A1D42B', 'Graphic Design': '#7B5CE6', 'Web Design': '#6251D8', 'Distribution': '#2BD449', 'Warehouse': '#7B2BD4', 'Education': '#D4AC2B', 'Teaching': '#2BCBD4', 'Engineering (Break down in different fiels of Eng - then, code them!)': '#D42B99', 'Events': '#A855F7', 'Fashion': '#2B37D4', 'Luxury': '#D4512B', 'Jewellery': '#2BD482', 'Financial Services': '#37D67A', 'Banking': '#0EA5A4', 'Insurance': '#14B8A6', 'Freight': '#D42B61', 'Logistics': '#30D42B', 'Procurement': '#582BD4', 'Health': '#D4892B', 'Hospitality': '#22C55E', 'Catering': '#16A34A', 'HR': '#8BD42B', 'Recruitment': '#2B5AD4', 'Information Technology (IT)': '#3FD0E0', 'Web Development': '#2E6BE6', 'Online Business': '#902BD4', 'Mobile': '#D4C12B', 'Language': '#2BB5D4', 'Translation': '#D42B84', 'Legal': '#53D42B', 'Market Research': '#352BD4', 'Analysis': '#D4662B', 'Marketing': '#FF6B6B', 'Advertising': '#E24A68', 'Social Media': '#5AA9E8', 'Media': '#FF5CA8', 'New Media': '#D946EF', 'Miscellaneous': '#2BD43C', 'Photography': '#6D2BD4', 'Videography': '#D49E2B', 'Project Management': '#2BD4CF', 'Property Management': '#D18E14', 'Real Estate': '#FFB120', 'Public Relations (PR)': '#2FBFB0', 'Communications': '#1E8A80', 'Public Sector': '#2BD474', 'Government': '#A62BD4', 'Retail': '#D1D42B', 'Sales': '#F97316', 'Scientific': '#D42B6E', 'Pharmaceutical': '#3DD42B', 'Biotech': '#4A2BD4', 'Security': '#D47C2B', 'Defence': '#2BD4AD', 'Sports': '#D42BC9', 'Surveying': '#F59E0B', 'Telecommunications': '#2B67D4', 'Training': '#D42B36', 'Development': '#2BD452', 'Travel': '#832BD4', 'Leisure': '#D4B42B', 'Energy': '#2BC2D4', 'Water': '#D42B91', 'Gas': '#60D42B', 'Blockchain': '#2563EB', 'Crypto currency': '#06B6D4'}
SECTOR_STYLES = {'Accountancy': 'finance', 'Administration': 'generic', 'PA': 'generic', 'VA': 'generic', 'Aerospace': 'tech', 'Agriculture': 'generic', 'Environment': 'generic', 'Architecture': 'property', 'Interior Design': 'design', 'Arts': 'design', 'Dance': 'design', 'Theater': 'design', 'Entertainment': 'design', 'Music': 'design', 'Automotive': 'tech', 'Transportation': 'generic', 'Business Management': 'sales', 'Business Development': 'sales', 'Charity': 'generic', 'NGO': 'generic', 'Social Services': 'generic', 'Non Profit': 'generic', 'Construction': 'property', 'Consulting': 'marketing', 'Customer Service': 'sales', 'Graphic Design': 'design', 'Web Design': 'design', 'Distribution': 'sales', 'Warehouse': 'sales', 'Education': 'generic', 'Teaching': 'generic', 'Engineering (Break down in different fiels of Eng - then, code them!)': 'tech', 'Events': 'events', 'Fashion': 'design', 'Luxury': 'design', 'Jewellery': 'design', 'Financial Services': 'finance', 'Banking': 'finance', 'Insurance': 'finance', 'Freight': 'sales', 'Logistics': 'sales', 'Procurement': 'sales', 'Health': 'generic', 'Hospitality': 'events', 'Catering': 'events', 'HR': 'generic', 'Recruitment': 'generic', 'Information Technology (IT)': 'tech', 'Web Development': 'tech', 'Online Business': 'marketing', 'Mobile': 'marketing', 'Language': 'generic', 'Translation': 'generic', 'Legal': 'generic', 'Market Research': 'marketing', 'Analysis': 'marketing', 'Marketing': 'marketing', 'Advertising': 'marketing', 'Social Media': 'social', 'Media': 'media', 'New Media': 'media', 'Miscellaneous': 'generic', 'Photography': 'social', 'Videography': 'social', 'Project Management': 'marketing', 'Property Management': 'property', 'Real Estate': 'property', 'Public Relations (PR)': 'pr', 'Communications': 'pr', 'Public Sector': 'generic', 'Government': 'generic', 'Retail': 'sales', 'Sales': 'sales', 'Scientific': 'generic', 'Pharmaceutical': 'generic', 'Biotech': 'generic', 'Security': 'generic', 'Defence': 'generic', 'Sports': 'generic', 'Surveying': 'property', 'Telecommunications': 'tech', 'Training': 'marketing', 'Development': 'marketing', 'Travel': 'events', 'Leisure': 'events', 'Energy': 'tech', 'Water': 'tech', 'Gas': 'tech', 'Blockchain': 'tech', 'Crypto currency': 'tech'}
SECTOR_ALIASES = {'Information Technology (IT)': ['information technology', 'it internship', 'technology'], 'Financial Services': ['finance', 'financial'], 'Accountancy': ['accounting', 'accounts', 'accountant'], 'Public Relations (PR)': ['public relations', ' pr ', 'pr internship'], 'Real Estate': ['real estate', 'estate agency'], 'Property Management': ['property management'], 'Business Development': ['business development', 'bd internship'], 'Social Media': ['social media'], 'Market Research': ['market research'], 'Web Development': ['web development', 'frontend', 'backend', 'full stack', 'developer'], 'Graphic Design': ['graphic design'], 'Web Design': ['web design'], 'New Media': ['new media'], 'Crypto currency': ['crypto currency', 'cryptocurrency', 'crypto'], 'Engineering (Break down in different fiels of Eng - then, code them!)': ['engineering'], 'Theater': ['theatre', 'theater'], 'Non Profit': ['non profit', 'non-profit']}

_DEFAULT_SECTOR = "Miscellaneous"
_DEFAULT_COLOR = SECTOR_COLORS.get(_DEFAULT_SECTOR, "#5FC7A6")

_KEYWORDS = []
for _sector in SECTORS:
    _terms = {_sector.lower()}
    _terms.update(t.lower() for t in SECTOR_ALIASES.get(_sector, []))
    for _term in _terms:
        _clean = re.sub(r"\s+", " ", _term).strip()
        if _clean:
            _KEYWORDS.append((_sector, _clean))
_KEYWORDS.sort(key=lambda item: len(item[1]), reverse=True)


def _normalise(text):
    text = (text or "").lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9+() ]+", " ", text)
    return " " + re.sub(r"\s+", " ", text).strip() + " "


def classify_sector_text(*texts):
    haystack = _normalise(" ".join(t for t in texts if t))
    for sector, keyword in _KEYWORDS:
        needle = _normalise(keyword).strip()
        if f" {needle} " in haystack:
            return sector
    return _DEFAULT_SECTOR


def classify_featured_job(job):
    title_sector = classify_sector_text(job.get("title", ""))
    sector = title_sector if title_sector != _DEFAULT_SECTOR else classify_sector_text(job.get("fields", ""))
    return {
        "sector": sector,
        "style": SECTOR_STYLES.get(sector, "generic"),
        "accent": SECTOR_COLORS.get(sector, _DEFAULT_COLOR),
    }


def sector_palette(sector):
    return {
        "version": SECTOR_PALETTE_VERSION,
        "sector": sector,
        "accent": SECTOR_COLORS.get(sector, _DEFAULT_COLOR),
        "style": SECTOR_STYLES.get(sector, "generic"),
    }
