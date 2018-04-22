#!/usr/bin/env python

import traceback
import sys
import argparse
import os
import time
import requests
import datetime
import json
from requests.auth import HTTPBasicAuth
import jinja2
import logging
import subprocess
import shutil
import csv
from local_settings import THEMETEST_CONFIG

# Load in the virtualenv
activate_this = os.path.abspath(os.path.dirname(sys.argv[0])) + "/env/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))


# coding=utf8
def force_to_unicode(text):
    "If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"
    return text if isinstance(text, unicode) else text.decode('utf8')


# Define where the test sites are installed and what URL to use to reach them
testsite_basedir = THEMETEST_CONFIG['testsite_basedir']
testsite_baseurl = THEMETEST_CONFIG['testsite_baseurl']
images_path = THEMETEST_CONFIG['images_path']

# The Target WordPress instance to create posts on
wp_path = THEMETEST_CONFIG['wp_path']

with open('.gtcredentials') as f:
    gtmetrix_api_username, gtmetrix_api_password = f.readline().split(":")


# Change this to logging.INFO to reduce the noise on the screen once everything is running nicely
screen_logging_level = logging.DEBUG
log_filename = __file__ + '.log'
log_file_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
log_screen_format = log_file_format

# Logging setup
logging.basicConfig(level=logging.DEBUG,
                    format=log_file_format,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_filename)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(screen_logging_level)
# set a format which is simpler for console use
formatter = logging.Formatter(log_screen_format, datefmt='%Y-%m-%d %H:%M:%S')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

parser = argparse.ArgumentParser(
    description="""A script to do several things:
    Read a list of featured themes from a JSON file
    Automatically install them
    Test them with GTMetrix
    Publish the results to WordPress

    Neat eh?""")

parser.add_argument(
    '--dry_run', 
    action='store_true',
    help='perform a dry run (make no external calls) (default: true)')

parser.add_argument(
    'test_action',
    choices=['generate_sites', 'test_gt', 'post_pages', 'cleanup', 'rundown', 'auto'],
    help='Which part of the process to perform, or auto for fully automated operation.')

args = parser.parse_args()
logging.info('Started %s' % __file__)
if args.dry_run:
    print("Dry run %s" % args.test_action)
else:
    print("Real run %s" % args.test_action)

@jinja2.contextfunction
def get_context(c):
    return c

def render(tpl_path, context):
    """ Standard Jinja render function, DebugUndefined leaves undefined 
    variables in place."""

    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        undefined=jinja2.DebugUndefined,
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context=context)


def load_theme_data(filename='../data/featured.json'):
    """This loads the theme data from a JSON formatted list like from 
    api.wordpress.org"""

    with open(filename, "r") as f:
        data = json.load(f)
    goodthemes = []
    for theme in data['data']['themes']:
        if theme['slug'] != 'twentyseventeen':
            goodthemes.append(theme)
    return goodthemes


def load_gtmetrix_data(wp_instance_name):
    """This loads data from a GTMetrix test"""

    filename = "gtmetrix/" + wp_instance_name + "-test.log"
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def generate_sites(themedata):
    """This takes the JSON object created by load_theme_data and installs 
    WordPress + the theme"""

    log = logging.getLogger('generate_sites')
    for theme in themedata:
        wp_theme = theme['slug']
        log.info('Installing %s' % wp_theme)
        wp_instance_name = wp_theme + "01"
        prefix_db = wp_instance_name.replace('.', '').replace('-', '') + "_"
        dbhost = THEMETEST_CONFIG['dbhost']
        dbname = THEMETEST_CONFIG['dbname']
        dbuser = THEMETEST_CONFIG['dbuser']
        dbpass = THEMETEST_CONFIG['dbpass']
        site_url = testsite_baseurl + wp_instance_name
        site_path = testsite_basedir + wp_instance_name
        wp_cli_base = "wp --path=%s " % site_path
        if args.dry_run: wp_cli_base = 'echo ' + wp_cli_base
        log.debug("%s | %s | %s | %s | %s" % (
            wp_instance_name, prefix_db, site_url, site_path, wp_cli_base))
        os.system(wp_cli_base + "core download")
        #os.system(wp_cli_base + "core config --dbhost=localhost --dbname=wp03_themetest --dbprefix=%s --dbuser=wp03_themetest --dbpass=MYSwaterloo1815" % (dbname, prefix_db, dbuser, dbpass))
        os.system(wp_cli_base + "core config --dbhost=%s --dbname=%s --dbprefix=%s --dbuser=%s --dbpass=%s" % (dbhost, dbname, prefix_db, dbuser, dbpass))
        os.system(wp_cli_base + "core install --url=%s --title='Your Blog Title' --admin_name=wpadmin --admin_password=nDNNjOI12840DKndf38 --admin_email=you@example.com" % site_url)
        os.system(wp_cli_base + "theme install %s" % wp_theme)
        os.system(wp_cli_base + "theme activate %s" % wp_theme)


def test_gtmetrix(themedata, readonly=False):
    """This takes the JSON object created by load_theme_data and tests each 
    site using GTMetrix"""

    log = logging.getLogger('test_gtmetrix')
    for theme in themedata:

        wp_theme = theme['slug']
        wp_instance_name = wp_theme + "01"
        prefix_db = wp_instance_name + "_"
        site_url = testsite_baseurl + wp_instance_name
        site_path = testsite_basedir + wp_instance_name
        gtmetrix_data_filename = "../data/" + wp_instance_name + "-test.log"
        gtmetrix_screenshot_filename = "%s/%s-ss.png" % (images_path, wp_theme)
        readonly = readonly or args.dry_run
        #wp_cli_base = "wp --path=%s " % site_path
        #print("%s | %s | %s | %s | %s" % (wp_instance_name, prefix_db, site_url, site_path, wp_cli_base))
        if readonly:
            log.info('Read only, loading data from %s' % gtmetrix_data_filename)
            gtmetrix_data = json.load(open(gtmetrix_data_filename))
        else:
            log.info("Starting GTMetrix test for " + wp_instance_name)
            r = requests.post('https://gtmetrix.com/api/0.1/test',
                                auth=HTTPBasicAuth(
                                    gtmetrix_api_username, gtmetrix_api_password),
                                data={'url': site_url, 'x-metrix-cookies': 'c9.live.user.click-through = ok'})
            log.info("Request finished, status code: %s" % r.status_code)
            log.info("Complete Response: %s" % r.text)
            data = r.json()
            try:
                test_id = data['test_id']
                credits_left = data['credits_left']
                log.info('Test %s successfully queued. %s credits left.' %
                        (test_id, credits_left))
            except:
                trace = traceback.format_exc()
                data['error']
                log.error(r.json(), trace)
            test_state = "just started"
            total_run_time = 0

            while (test_state != "completed") and (test_state != "error"):
                r = requests.get('https://gtmetrix.com/api/0.1/test/%s' % test_id,
                                auth=HTTPBasicAuth(gtmetrix_api_username, gtmetrix_api_password))
                log.debug("HTTP Returned: %s" % r.status_code)
                log.debug(r.text)
                gtmetrix_data = r.json()
                test_state = gtmetrix_data['state']
                log.info(test_state)

                if test_state != "completed":
                    time.sleep(6)
                    total_run_time += 6

            log.info("Test completed, saving to: %s" % gtmetrix_data_filename)          
            with open(gtmetrix_data_filename, "w") as f:
                f.write(json.dumps(gtmetrix_data, indent=2))

        # Save the result to the theme object provided as an arugment
        theme['gtmetrix'] = gtmetrix_data

        # Now save the screenshot
        screenshot_url = gtmetrix_data['resources']['screenshot']
        log.info("Screenshot URL: %s" % screenshot_url)
        if readonly:
            log.info("Read only, not downloading to %s" % gtmetrix_screenshot_filename)
        else:
            log.info("Downloading to %s" % gtmetrix_screenshot_filename)
            response = requests.get(screenshot_url, auth=HTTPBasicAuth(
                gtmetrix_api_username, gtmetrix_api_password), stream=True)

            # Throw an error for bad status codes
            response.raise_for_status()

            with open(gtmetrix_screenshot_filename, 'wb') as handle:
                for block in response.iter_content(1024):
                    handle.write(block)

            time.sleep(6)


def build_acfdata(themedata):
    """Take themedata that has been loaded and run thru the above processes
     and now process them."""
    res = {}
  
    log = logging.getLogger('build_acfdata')
    for theme in themedata:
        wp_theme = theme['name']
        log.info("Name %s, Slug: %s, Version %s" % (theme['name'], theme['slug'], theme['version']))
        screenshot_filename = "%s/%s.png" % (images_path, theme['slug'])
        screenshot_url = 'http:' + theme['screenshot_url']
        log.info("Screenshot URL: %s" % screenshot_url)
        if args.dry_run:
            log.info("Read only, not downloading to %s" % screenshot_filename)
        else:
            if not os.path.isfile(screenshot_filename):
                log.info("Downloading to %s" % screenshot_filename)
                response = requests.get(screenshot_url, auth=HTTPBasicAuth(
                    gtmetrix_api_username, gtmetrix_api_password), stream=True)
                # Throw an error for bad status codes
                response.raise_for_status()

                with open(screenshot_filename, 'wb') as handle:
                    for block in response.iter_content(1024):
                        handle.write(block)
            else:
                log.info("File exists, skipping %s" % screenshot_filename)      
       
        # build post meta values for custom fields
        acfdata = {}
        acfdata['theme_name'] = theme['name']
        acfdata['theme_slug'] = theme['slug']
        acfdata['theme_version'] = theme['version']
        acfdata['theme_author'] = theme['author']
        acfdata['theme_rating'] = theme['rating']
        acfdata['theme_num_ratings'] = theme['num_ratings']
        acfdata['theme_downloaded'] = theme['downloaded']
        acfdata['theme_last_updated'] = theme['last_updated']
        acfdata['theme_homepage'] = theme['homepage']
        acfdata['theme_description'] = theme['description']
        acfdata['pagespeed_score'] = theme['gtmetrix']['results']['pagespeed_score']
        acfdata['yslow_score'] = theme['gtmetrix']['results']['yslow_score']
        acfdata['page_elements'] = theme['gtmetrix']['results']['page_elements']
        acfdata['html_bytes'] = theme['gtmetrix']['results']['html_bytes']
        acfdata['page_bytes'] = theme['gtmetrix']['results']['page_bytes']
        acfdata['report_url'] = theme['gtmetrix']['results']['report_url']
        acfdata['page_load_time'] = theme['gtmetrix']['results']['page_load_time']
        res[acfdata['theme_slug']] = acfdata

    return res


def create_wp_post(post_content, post_category, post_excerpt, post_title):
    log = logging.getLogger('create_wp_post')
    if not post_content.endswith('.html'):
        post_content = "--post-content='%s'" % post_content      

    log.debug("Params: %s, %s, %s, %s" % (post_content, post_category, post_excerpt, post_title))
    wpcli_base = "%s --path=%s " % (THEMETEST_CONFIG['wp_cli_path'], wp_path)
    if args.dry_run: wpcli_base = "echo " + wpcli_base
    post_excerpt = post_excerpt.encode('ascii', 'ignore')
    post_excerpt = post_excerpt.replace('\n', ' ').replace('\r', '')
    import_command = wpcli_base + r"""post create %s --post_category=%s --post_excerpt="%s" --porcelain --post_title="%s" """ % (post_content, post_category, post_excerpt, post_title)
    log.info("Executing: " + import_command)
    if args.dry_run:
        post_id = 4321
    else:
        post_id = subprocess.check_output(import_command, shell=True)
        post_id = post_id.replace('\n', ' ').replace('\r', '')
    return post_id


def post_pages(acfdata):
    log = logging.getLogger('post_pages')
    for wp_theme, theme in acfdata.iteritems():
        log.debug(theme)
        wp_theme = theme['theme_slug']
        wp_instance_name = wp_theme + "01"
        image_filename = "%s/%s.png" % (images_path, wp_theme)
        ss_filename = "%s/%s-ss.png" % (images_path, wp_theme)
        gtmetrix_data_filename = "gtmetrix/" + wp_instance_name + "-test.log"
        gtmetrix_screenshot_filename = "%s/%s-ss.png" % (images_path, wp_theme)

        # TODO: set all of the metadata at post create, for now just do it afterwards
        # porcelain makes it just output the ID
        wpcli_base = "%s --path=%s " % (THEMETEST_CONFIG['wp_cli_path'], wp_path)
        if args.dry_run: wpcli_base = "echo " + wpcli_base
        value = theme['theme_description']
        value_asc = value.encode('ascii', 'ignore')
        value_asc = value_asc.replace('\n', ' ').replace('\r', '').replace("'", r"'\''")
        import_command = wpcli_base + r"""post create --post_content='[themetest_results_full]' --post_category=theme-performance-reports --post_excerpt="%s" --post_title='%s' --porcelain""" % (
            value_asc,
            "%s - WordPress Theme Performance Test" % theme['theme_name'])
        log.info("Import command: " + import_command)
        if args.dry_run:
            post_id = 4321
        else:
            res = subprocess.check_output(import_command, shell=True)
            post_id = res.splitlines()[len(res.splitlines()) - 1].replace('\n', ' ').replace('\r', '')

        #with open("posts.csv", "a+") as f:

        log.info("Slug: %s Post ID: %s" % (theme['theme_slug'], post_id))
        meta_command = wpcli_base + "post meta set %s " % str(post_id)
        for key in theme:
            if isinstance(theme[key], int):
                value = str(theme[key])
            else:
                value = theme[key]
            value_asc = value.encode('ascii', 'ignore')
            #value = str(value).replace(u"\u2018", "'").replace(u"\u2019", "'")
            value_asc = value_asc.replace('\n', ' ').replace('\r', '').replace("'", r"'\''")
            set_meta_command = meta_command + """%s "%s" """ % (key, value_asc)
            log.info("Setting meta: %s - %s" % (key, value_asc))
            log.debug("Full Command: %s" % set_meta_command)
            if not args.dry_run:
                subprocess.check_output(set_meta_command, shell=True)
        import_command = wpcli_base + r"""media import "%s" --post_id=%s --featured_image --porcelain""" % (
            image_filename,
            str(post_id).strip())
        log.info("Import: " + import_command)
        if args.dry_run:
            log.info("Dry run, faking id")
            image_feat_id = 5432
        else:
            image_feat_id = subprocess.check_output(import_command, shell=True)

        log.info(image_feat_id)


def post_rundown(acfdata):

    log = logging.getLogger('post_rundown')
    log.debug(acfdata)
    report_category_id = THEMETEST_CONFIG['report_category_id']
    #with open('posts.json') as json_file:  
#        data = json.load(json_file)
    #http://wpthemetest.waynethursby.com/testwp/wp-json/wp/v2/posts?after=2018-04-18T20:00:00&categories=3
    timestamp = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
    params = dict(
        after=timestamp,
        categories=report_category_id,
        post_status="publish"
    )
    wp_url = THEMETEST_CONFIG['wp_url']
    tmp_filename = "../tmp/rundown-output.html"
    template_filename = '../templates/rundown-template.html'
    r = requests.get("%swp-json/wp/v2/posts" % wp_url, params=params)
    log.debug(r.text)
    jsonstring = r.text.split('[{"id"', 1)[-1]
    jsonstring = '[{"id"' + jsonstring
    data = json.loads(jsonstring)
    postdata = {}
    for key in data:
        post_id = str(key['id'])
        theme_name = key['slug']
        theme_name = theme_name.split('-wordpress-theme-performance')[0]
        log.info("Proccesing %s:%s" % (theme_name, post_id))
        postdata[theme_name] = post_id
    r = render(template_filename, context=postdata)
    with open(tmp_filename, "w") as f:
       f.write(r)
    post_id = create_wp_post(
        tmp_filename, 
        3, 
        "Hey everyone we're back here with another rundown.", 
        "WordPress Theme Performance Rundown - %s" % datetime.datetime.today().strftime("%B %d %Y")
    )
    #api_url = "http://wpthemetest.waynethursby.com/testwp/wp-json/wp/v2/posts?after=%s&categories=3" % timestamp
    #print(api_url)
    # matchup = {}
    # for key in data:
    #     print(key['slug'])
    #     matchup[key['slug']] = key['id']

    # r = render('rundown-template.html', context=matchup)
    # with open('rundown-output.html', "w") as f:
    #     f.write(r)


    #res = render('rundown-template.php', acfdata)
    #log.info(res)
 

def main():
    themedata = load_theme_data()
    logging.info("Action: " + args.test_action)
    if args.test_action == "auto":
        generate_sites(themedata)
        test_gtmetrix(themedata)
        acfdata = build_acfdata(themedata)
        post_pages(acfdata)
        post_rundown(acfdata)

    if args.test_action == "generate_sites":
        generate_sites(themedata)

    if args.test_action == "test_gt":
        test_gtmetrix(themedata)

    if args.test_action == "post_pages":
        test_gtmetrix(themedata, readonly=True)
        acfdata = build_acfdata(themedata)
        post_pages(acfdata)

    if args.test_action == "cleanup":
        site_path = os.listdir(testsite_basedir)[0]
        wp_cli_base = "wp --path=%s " % site_path
        if args.dry_run: wp_cli_base = 'echo ' + wp_cli_base
        os.system("%s db reset --path=%s" % (wp_cli_base, site_path))
        os.system("%s db optimize --path=%s" % (wp_cli_base, site_path))
        for directory in os.listdir(testsite_basedir):
            logging.info("Deleting: " + directory)
            if not args.dry_run:
                shutil.rmtree(directory)

    if args.test_action == "archive":
        pass
    """ Write a thing to do all necessary log roation """

    if args.test_action == "rundown":
        test_gtmetrix(themedata, readonly=True)
        acfdata = build_acfdata(themedata)
        post_rundown(acfdata)
        #post_content = render('rundown-template.html', acfdata)
        #print(post_content)
    
if __name__== "__main__":
  main()