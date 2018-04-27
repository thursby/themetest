# ThemeTest

An unimaginatively-named open source framework for automated performance testing of WordPress themes.

## Getting Started

Install WordPress, with Advanced Custom Fields (ACF), WP CLI, Python 2.7, pip, virtualenv.

Import the ACF Custom Fields from ```templates/advanced-custom-field-export.xml```

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

Set up the ```env``` and install the requirements with ```pip```:
```bash
cd scripts
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Create a file named ```.gtcredentials``` with your GTmetrix Credentils in the format user:pass
```
user.name@domain.com:1343434apikey438484848
```

## Current Roadmap
* v0.1.0 - Stable tool performing daily GT Metrix tests and saving all data to WordPress
* v0.2.0 - Separate all components into logical units, produce a framework
* v0.3.0 - Expand testing to include additional tests
* v0.4.0 - Integrate control and reporting into WordPress UI
* v0.5.0 - Create the ability to run tests remotely (AWS or similar)

## Release targets for v1.0.0
* Detect new themes from a variety of configurable sources
* Automatically install themes with a range of configurable generated content
* Test the installations with a variety of configurable tests
* Save all data into WordPress custom fields
* Ensure saved data is accessible via WP API
* Remove dependency on external Advanced Custom Fields

## Built With

* [Python](https://www.python.org/) - Primary scripting and automation
* [WordPress](https://www.wordpress.org) - Used for testing and deployment
* [WP CLI](https://wp-cli.org/) - The best way to manage WordPress
* [Jinja](http://jinja.pocoo.org/docs/2.10/) - Jinja HTML templates
* [GTmetrix](https://gtmetrix.com/) - Performance Testing

## Contributing

If you're interested in contributing please submit a pull request or open an issue.

## Authors

* **Wayne Thursby** - *Initial work* - [WayneThursby.com](https://www.waynethursby.com)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



