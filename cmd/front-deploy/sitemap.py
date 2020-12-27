# Standard library
import os
from xml.dom import (
    minidom,
)

# Third party libraries
from more_itertools import (
    chunked,
)

# Environment
AWS_CLOUDFRONT_DOMAIN = os.environ['AWS_CLOUDFRONT_DOMAIN']
DATA_NIXDB = os.environ['DATA_NIXDB']


def text_node(string: str) -> minidom.Text:
    text = minidom.Text()
    text.data = string
    return text


def dom_to_string(dom) -> str:
    return dom.toprettyxml(indent =" ")


def build_sitemapindex(locations) -> str:
    doc = minidom.Document()

    sitemapindex = doc.createElement('sitemapindex')
    sitemapindex.setAttribute(
        'xmlns',
        'http://www.google.com/schemas/sitemap/0.84',
    )
    sitemapindex.setAttribute(
        'xmlns:xsi',
        'http://www.w3.org/2001/XMLSchema-instance',
    )
    sitemapindex.setAttribute(
        'xsi:schemaLocation',
        ' '.join((
            'http://www.google.com/schemas/sitemap/0.84',
            'http://www.google.com/schemas/sitemap/0.84/siteindex.xsd',
        )),
    )

    for location in locations:
        sitemap = doc.createElement('sitemap')
        loc = doc.createElement('loc')
        loc.appendChild(text_node(location))
        sitemap.appendChild(loc)
        sitemapindex.appendChild(sitemap)

    doc.appendChild(sitemapindex)

    return dom_to_string(doc)


def build_sitemap(locations) -> str:
    doc = minidom.Document()

    urlset = doc.createElement('urlset')
    urlset.setAttribute(
        'xmlns',
        'http://www.google.com/schemas/sitemap/0.84',
    )
    urlset.setAttribute(
        'xmlns:xsi',
        'http://www.w3.org/2001/XMLSchema-instance',
    )
    urlset.setAttribute(
        'xsi:schemaLocation',
        ' '.join((
            'http://www.google.com/schemas/sitemap/0.84',
            'http://www.google.com/schemas/sitemap/0.84/sitemap.xsd',
        )),
    )

    for location in locations:
        url = doc.createElement('url')
        loc = doc.createElement('loc')
        loc.appendChild(text_node(location))
        url.appendChild(loc)
        urlset.appendChild(url)

    doc.appendChild(urlset)

    return dom_to_string(doc)


def main():
    urls = [
        '',
    ]

    index = 0
    for index, chunk in enumerate(chunked(urls, 1000)):
        with open(f'public/sitemap/sitemap-{index}.xml', 'w') as handle:
            handle.write(build_sitemap([
                f'https://4shells.com{url}'
                for url in urls
            ]))

    for index, chunk in enumerate(chunked(range(index + 1), 50)):
        with open(f'public/sitemap/sitemapindex-{index}.xml', 'w') as handle:
            handle.write(build_sitemapindex([
                f'https://{AWS_CLOUDFRONT_DOMAIN}/sitemap/sitemapindex-{element}.xml'
                for element in chunk
            ]))


if __name__ == '__main__':
    main()
