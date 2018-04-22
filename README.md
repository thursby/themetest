# themetest
An open source framework for automated performance testing of WordPress themes

## Quick Start
Install WordPress, WP CLI, Python, do a bunch of setup.

Import the ACF Custom Fields.

Create a scripts/local_settings.py with your config:

```python
THEMETEST_CONFIG = {
    # Define where the test sites are installed and what URL to use to reach them
    'testsite_basedir': "/var/www/wordpress-sites.test/testsites/",
    'testsite_baseurl': "https://wordpress-sites.test/testsites/",
    'images_path': "/home/ubuntu/workspace/theme-images",
    
    # The Target WordPress instance to create posts on
    'wp_path': "/var/www/themes-site.test",
    'wp_url': 'https://themes-site.test/', # include /
    'report_category_id': '2', # The ID of the target category for theme report posts
    'rundown_category_id': '3', # The ID of the rundown category
    'dbhost': 'db_hostname',
    'dbname': 'db_name',
    'dbuser': 'db_username',
    'dbpass': 'dbpassword',   
    
    # WP_CLI path
    'wp_cli_path': '/usr/local/bin/wp'
}
```
