from flask import Flask, request, jsonify, render_template, abort, make_response, session
import os
import hashlib

from logging import basicConfig, getLogger, DEBUG
basicConfig(level=DEBUG)
logger = getLogger(__name__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

## Custom import
import db_connect

## WebSite UI
@app.route('/', methods=['GET'])
def root():
    html = get_urldata('_toppage', '_root')
    return html
    
@app.route('/<category>', methods=['GET'])
def category(category):
    if category == '':
        category = '_toppage'
    html = get_urldata(category, '_root')
    return html

@app.route('/<category>/<custom_url>', methods=['GET'])
def other(category, custom_url):
    html = get_urldata(category, custom_url)
    return html
    
## WebSite UI common
def get_urldata(category, custom_url):

    url_info = db_connect.get_url_t(category, custom_url)
    site_info = db_connect.get_site_t(url_info['site_id'])
    doc_info = db_connect.get_doc_t(url_info['url_id'])
    cate_info = db_connect.get_category_l(url_info['site_id'])
    if category == 'album' and custom_url != '_root':
        musicgroup, albuminfo, trackinfo = db_connect.get_head_l(custom_url)
    else:
        musicgroup = {}
        albuminfo = {}
        trackinfo = []

    page_info = {
        'category': category,
        'custom_url': custom_url
    }

    html = render_template('output.html', url_info=url_info, site_info=site_info, doc_info=doc_info, cate_info=cate_info, musicgroup=musicgroup, albuminfo=albuminfo, trackinfo=trackinfo, page_info=page_info)

    return html

