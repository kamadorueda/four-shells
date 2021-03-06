# Standard library
import glob
import os
import urllib.parse
from xml.dom import (
    minidom,
)

# Third party libraries
from more_itertools import (
    chunked,
)

# Environment
DATA_NIXDB = os.environ['DATA_NIXDB']


def text_node(string: str) -> minidom.Text:
    text = minidom.Text()
    text.data = string
    return text


def dom_to_string(dom) -> bytes:
    return dom.toprettyxml(encoding='UTF-8', indent=' ', newl='\n')


def build_sitemapindex(locations) -> bytes:
    doc = minidom.Document()

    sitemapindex = doc.createElement('sitemapindex')
    sitemapindex.setAttribute(
        'xmlns',
        'http://www.sitemaps.org/schemas/sitemap/0.9',
    )
    sitemapindex.setAttribute(
        'xmlns:xsi',
        'http://www.w3.org/2001/XMLSchema-instance',
    )
    sitemapindex.setAttribute(
        'xsi:schemaLocation',
        ' '.join((
            'http://www.sitemaps.org/schemas/sitemap/0.9',
            'http://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd',
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


def build_sitemap(locations) -> bytes:
    doc = minidom.Document()

    urlset = doc.createElement('urlset')
    urlset.setAttribute(
        'xmlns',
        'http://www.sitemaps.org/schemas/sitemap/0.9',
    )
    urlset.setAttribute(
        'xmlns:xsi',
        'http://www.w3.org/2001/XMLSchema-instance',
    )
    urlset.setAttribute(
        'xsi:schemaLocation',
        ' '.join((
            'http://www.sitemaps.org/schemas/sitemap/0.9',
            'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd',
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
        '/cachipfs',
        '/docs',
        '/docs/source',
        '/nixdb/search',
    ]

    for pkg_path in glob.iglob(f'{DATA_NIXDB}/pkgs/*.json'):
        pkg = os.path.basename(pkg_path)
        pkg = os.path.splitext(pkg)[0]
        pkg = urllib.parse.quote_plus(pkg)
        urls.append(f'/nixdb/pkg/{pkg}')

    urls.sort()

    index = 0
    for index, chunk in enumerate(chunked(urls, 1000)):
        path = f'back/sitemap/sitemap-{index}.xml'
        print(f'[INFO] Writting: {path}')
        with open(path, 'wb') as handle:
            handle.write(build_sitemap([
                f'https://4shells.com{url}'
                for url in chunk
            ]))

    with open('back/robots.txt', 'w') as robots_handle:
        robots_handle.write('User-agent: *\n')
        robots_handle.write('Disallow:\n')

        for index, chunk in enumerate(chunked(range(index + 1), 10)):
            path = f'back/sitemap/sitemapindex-{index}.xml'
            print(f'[INFO] Writting: {path}')
            robots_handle.write(f'Sitemap: https://4shells.com/sitemapindex-{index}.xml\n')
            with open(path, 'wb') as handle:
                handle.write(build_sitemapindex([
                    f'https://4shells.com/sitemap-{element}.xml'
                    for element in chunk
                ]))


if __name__ == '__main__':
    main()
