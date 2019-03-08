from io import StringIO
from flask import (
    Blueprint, redirect, render_template, request, session, url_for, jsonify, current_app
)

import csv2wiki, subprocess

from wikis import db, signin_required

bp = Blueprint('wikis', __name__, url_prefix='/wikis/', template_folder='templates')

def create_wiki():
    new_wiki = Wiki(username=session.get("account_username"),
                    wikiname=request.form["name"])
    db.session.add(new_wiki)
    db.session.commit()

    wiki_db_name = "librehq_wikis_" + str(new_wiki.id)

    # Let this error if the script isn't here, since we're in prototype mode
    session.get("account_username")
    subprocess.call([
        'ansible-playbook',
        'wikis/ansible/mediawiki-add-wiki.yml',
        '-e', 'wiki_name=' + request.form["name"],
        '-e', 'wiki_db=' + wiki_db_name
    ])

@bp.route('')
@signin_required
def dashboard():
    return render_template("wikis.html")

@bp.route("/wikisdata")
@signin_required
def wiki_data():
    wikis = Wiki.query.filter_by(username=session.get("account_username")).all()
    wikisdata = map(lambda w: {
        "wikiname": w.wikiname,
        "id": w.id,
        "url": "http://" + w.wikiname + "." + current_app.config.get("WIKI_URL")
    }, wikis)
    return jsonify(list(wikisdata))

@bp.route('createwiki', methods=(["POST"]))
@signin_required
def create_plain():
    create_wiki()

    return ("<a href='http://" +
        request.form["name"] +
        "." +
        current_app.config.get("WIKI_URL") +
        "'>New wiki: " +
        request.form["name"] + "</a>")

@bp.route('deletewiki', methods=(["POST"]))
@signin_required
def delete_wiki():
    wiki = Wiki.query.get(request.form["wiki_id"])
    wiki_db_name = "librehq_wikis_" + str(wiki.id)

    db.session.delete(wiki)
    db.session.commit()

    subprocess.call([
        'ansible-playbook',
        'wikis/ansible/mediawiki-delete-wiki.yml',
        '-e', 'wiki_name=' + wiki.wikiname,
        '-e', 'wiki_db=' + wiki_db_name
    ])

    return redirect(url_for(".dashboard"))

@bp.route('renamewiki', methods=(["POST"]))
@signin_required
def rename_wiki():
    wiki = Wiki.query.get(request.form["wiki_id"])
    old_wiki_name = wiki.wikiname
    new_wiki_name = request.form["new_wiki_name"]

    wiki.wikiname = new_wiki_name
    db.session.add(wiki)
    db.session.commit()

    subprocess.call([
        'ansible-playbook',
        'wikis/ansible/mediawiki-rename-wiki.yml',
        '-e', 'wiki_name_old=' + old_wiki_name,
        '-e', 'wiki_name_new=' + new_wiki_name
    ])

    return redirect(url_for(".dashboard"))

@bp.route('uploadcsv', methods=(["POST"]))
@signin_required
def create_with_csv():
    if "name" in request.form:
        wikiname = request.form["name"]
        create_wiki()
    else:
        wiki = Wiki.query.get(request.form["wiki_id"])
        wikiname = wiki.wikiname

    if "yesUseConfigForm" == request.form["configuration"]:
        config = {}
        config["sec_map"] = request.form["pageSectionLayout"]
        config["title_tmpl"] = request.form["pageTitleTemplate"]
        config["toc_name"] = request.form["toc"]
        config["cat_col"] = request.form["categoryColumn"]
    else:
        config = csv2wiki.parse_config_string(request.files["config"].read().decode("utf-8"))

    # Override config options with our known parameters
    config["wiki_url"] = "http://" + wikiname + "." + current_app.config.get("WIKI_URL")
    # These are set in the addWiki.sh script
    config["username"] = "librehq_control"
    config["password"] = current_app.config.get("MW_CONTROL_USER_PW")

    csv_in = csv2wiki.CSVInput(StringIO(request.files["csv"].read().decode('utf-8')), config)
    output = StringIO()
    wiki_sess = csv2wiki.WikiSession(config, csv_in, False, output)
    wiki_sess.make_pages(None, "size")
    return ("<pre>" + output.getvalue() + "</pre>" +
            "<a href='http://" +
            wikiname +
            "." +
            current_app.config.get("WIKI_URL") +
            "'>New wiki: " +
            wikiname + "</a>")

class Wiki(db.Model):
    __bind_key__ = "wikis"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    wikiname = db.Column(db.String(128))
