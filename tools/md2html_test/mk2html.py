#!/usr/bin/env python3

import markdown
import markdown2
import pygments


def md2html2(content):
    exts = [
        'code-friendly',
        'code-color',
        'tables',
        # 'markdown.extensions.toc'
    ]
    # markdown covert to html
    # mk = markdown2.Markdown(extras=exts)
    # html = mk.convert(content)
    html = markdown.markdown(content, extras=exts)
    return html


def md2html(content):
    exts = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.toc'
    ]
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.toc',
    ])
    # markdown covert to html
    # html = markdown.markdown(content, extensions=exts)
    html = md.convert(content)
    toc = md.toc
    print(toc)
    return html


def main():
    with open('./test.md', 'r') as f:
        mkd = f.read()

    with open('./template.html', 'r') as f:
        template = f.read()

    content = md2html(mkd)
    html = template.replace("{{content}}", content)
    with open('./test.html', 'w') as f:
        f.write(html)


if __name__ == "__main__":
    main()
