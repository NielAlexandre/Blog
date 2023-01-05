#!/usr/bin/python3
# -*- coding: utf-8 -*-
#é

import os

from Anana import Consts

from collections import OrderedDict, namedtuple
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for

from blog import Post, filter_post
from random import choice

app = Flask(__name__)

@app.route("/", methods=['GET'])
def main():
    entries = [Post(f) for f in Path("posts").glob("*") if not f.name.startswith('.')]
    page = request.args.get("p", "0")
    if not page.isdigit():
        page = 0
    else:
        page = int(page)

    filterin = request.args.get("fi", "")
    if filterin:
        filterin = filterin.split(',')
    filterout = request.args.get("fo", '')
    if filterout:
        filterout = filterout.split(',')
    entries = list(filter_post(entries, filterin, filterout))
    sentries = sorted(entries, key=lambda x: x.ctime, reverse=True)
    pentries = sentries[page*5:(page+1)*5]
    [e.load_img() for e in pentries]

    ppage = str(page-1) if page > 0 else None
    npage = page+1 if (page+1)*5 <= len(entries) else None

    return render_template("blog.html",
            title="Rien Ici",
            entries=pentries,
            ppage=ppage, npage=npage,
            filters=f"fi={','.join(filterin)}&fo={','.join(filterout)}")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
