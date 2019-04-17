import psycopg2
import os

from logging import basicConfig, getLogger, DEBUG
basicConfig(level=DEBUG)
logger = getLogger(__name__)

def get_conn():
    pg_url = os.environ['POSTGRES_URL']
    
    conn = psycopg2.connect(pg_url)
    return conn
    
def get_url_t(category, custom_url):
    sql_u = 'SELECT url_id, category, title, custom_url, site_id FROM simpleweb_url_t WHERE category=%s AND custom_url=%s;'
    
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(sql_u, (category, custom_url,))
        result_u = cur.fetchone()
    
    url_info = {
        'url_id': result_u[0],
        'category': result_u[1],
        'title': result_u[2],
        'custom_url': result_u[3],
        'site_id': result_u[4]
    }
    return url_info

def get_url_l(category):
    sql_l = 'SELECT url_id, category, title, custom_url, site_id FROM simpleweb_url_t WHERE category=%s;'

    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(sql_l, (category,))
        result_l = cur.fetchall()

    url_list = []
    for item in result_l:
        url_info = {
            'url_id': item[0],
            'category': item[1],
            'title': item[2],
            'custom_url': item[3],
            'site_id': item[4]
        }
        url_list.append(url_info)
    return url_list

def get_site_t(site_id):
    sql_s = 'SELECT site_id, site_name, domain_name, copyright FROM simpleweb_site_t WHERE site_id=%s;' 
    
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(sql_s, (site_id,))
        result_s = cur.fetchone()

    site_info = {
        'site_id': result_s[0],
        'site_name': result_s[1],
        'domain_name': result_s[2],
        'copyright': result_s[3]
    }
    return site_info
    
def get_doc_t(url_id):
    sql_d = 'SELECT doc_id, doc_title, doc_text, priority, url_id, anchor FROM simpleweb_doc_t WHERE url_id=%s ORDER BY priority ASC;'
    
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(sql_d, (url_id,))
        result_s = cur.fetchall()
        
    doc_info = []
    for row in result_s:
        page_docs = {
            'doc_id': row[0],
            'doc_title': row[1],
            'doc_text': row[2],
            'priority': row[3],
            'url_id': row[4],
            'anchor': row[5]
        }
        doc_info.append(page_docs)

    return doc_info

def get_category_l(site_id):
    sql_l = 'SELECT cate_id, category, title, site_id FROM simpleweb_cate_t WHERE site_id=%s;'

    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(sql_l, (site_id,))
        result_l = cur.fetchall()

    category_list = []
    for row in result_l:
        category_info = {
            'cate_id': row[0],
            'category': row[1],
            'title': row[2],
            'site_id': row[3]
        }
        if not category_info['category'] == '_toppage':
            category_list.append(category_info)
    return category_list

def get_head_l(custom_url):

    sql_mu = 'SELECT muscian_id, url, image, name, same_as, description, url_template, in_language, country FROM simpleweb_ext_musicgroup_t;'
    conn = get_conn()
    with conn.cursor() as cur_mu:
        cur_mu.execute(sql_mu)
        result_mu = cur_mu.fetchone()

    musicgroup = {
        'musician_id': result_mu[0],
        'url': result_mu[1],
        'image': result_mu[2],
        'name': result_mu[3],
        'same_as': result_mu[4],
        'description': result_mu[5],
        'url_template': result_mu[6],
        'in_language': result_mu[7],
        'country': result_mu[8]
    }

    sql_al = 'SELECT album_id, url, genre, image, name, numtracks, description, by_artist, date_published, producer, url_template, in_language, country FROM simpleweb_ext_albuminfo_t WHERE custom_url=%s;'

    with conn.cursor() as cur_al:
        cur_al.execute(sql_al, (custom_url,))
        result_al = cur_al.fetchone()

    albuminfo = {
        'album_id': result_al[0],
        'url': result_al[1],
        'genre': result_al[2],
        'image': result_al[3],
        'name': result_al[4],
        'numtracks': result_al[5],
        'desription': result_al[6],
        'by_artist': result_al[7],
        'date_published': result_al[8],
        'producer': result_al[9],
        'url_template': result_al[10],
        'in_language': result_al[11],
        'country': result_al[12]
    }

    sql_tr = 'SELECT track_id, album_id, position, name, url, duration, creator, copyright_holder, date_published FROM simpleweb_ext_trackinfo_t WHERE album_id=%s;'

    with conn.cursor() as cur_tr:
        cur_tr.execute(sql_tr, (albuminfo['album_id'],))
        result_tr = cur_tr.fetchall()

    trackinfo = []
    for item in result_tr:
        track = {
            'track_id': item[0],
            'album_id': item[1],
            'position': item[2],
            'name': item[3],
            'url': item[4],
            'duration': item[5],
            'creator': item[6],
            'copyright_holder': item[7],
            'date_published': item[8]
        }
        trackinfo.append(track)
    
    return musicgroup, albuminfo, trackinfo