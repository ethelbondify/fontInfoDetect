from bs4 import BeautifulSoup
import cssutils
import json

def extract_font_styles(url):
    page = open(url)
    html_doc = page.read()

    # Parse the HTML document
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Initialize a list to store font information
    font_info = []

    # Extract and analyze inline styles
    for element in soup.find_all(style=True):
        inline_styles = cssutils.css.CSSStyleDeclaration()
        inline_styles.cssText = element['style']

        font_family = inline_styles.getPropertyValue('font-family')
        font_size = inline_styles.getPropertyValue('font-size')
        selector = get_css_selector(element)
        text = element.text

        # Store the font information in a dictionary
        font_info.append({
            "Location of Inline Text": element.sourcepos,
            "Font Family": font_family,
            "Font Size": font_size,
            "HTML Selector": selector,
            "Inline Text": text
        })

    # Convert the font information to JSON format
    json_result = json.dumps(font_info, indent=2)

    return json_result

def get_css_selector(element):
    selectors = []
    while element.parent:
        if element.get('id'):
            selectors.insert(0, f"#{element['id']}")
            break
        for i, sibling in enumerate(element.find_previous_siblings()):
            if sibling.name == element.name:
                selectors.insert(0, f"{element.name}:nth-of-type({i + 1})")
                break
        selectors.insert(0, element.name)
        element = element.parent
    return ' > '.join(selectors)

# Call the function to extract font styles
result = extract_font_styles("../../Sample_multiligual_text.html")

# Print or use the JSON result as needed
print(result)
