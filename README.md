# WP-Migrate #

WP Migrate is a tool to process the WordPress sql and change
the table name prefix, if applicable, and domain name.

The guid for posts will be changed if it is the same as the domain.  This utility
should not be used for sites where resetting the reader feed will cause problems.

Tests are provided using pytest

This application has been designed to run under Python 2 and 3, but has
not been tested on P3 yet.


## Running the Application ##


To run the application:

    clone the repository to your local computer: default folder is wp-migrate

    copy the sql to a folder, the default location is in the application
    at data/data/<newfolder> or you can give the absolute path to the sql.  Only
    one sql file can exist in the folder.

    ftp the wp_content folder new site.  The assumption is wordpress has been installed.

    from the main application folder enter:

        python wp_migrate

    A prompt for the following parameters will be shown:

    Path:

        The path is relative to the application root directory or an
        absolute path.  The ending / must be entered.

    Table Prefix:

        The table name prefix is optional and if not used, then is
        skipped.  The prefix is established in the wp-config.php file
        in the php value $table_prefix.

    Domain:

        Domain name references are stored in two forms: text and serialized
        text.  The application will scan for the domain name and
        determine if the string is in standard text or serialized text.

    URL:

        If the site is installed in a subdirectory (ie, not in the root dir
        of the domain, then the URL will be different from the Domain.  If
        they are the same, the URL can be omitted, ie just press return.

    Full Path:

        Some of the internal paths require the full path to the site.  If a
        Linux environment, the path is in the form of /home/<userid>/<site-domain>

    Other comments

    This application should run under Python 2.7 or Python 3.3.
    See the requirements.txt file for Python module dependencies.

## Structure ##

The application code in is the wp_migrate folder, data in the data folder and
tests are in the tests folder.

The data folder should contain sub-folders which hold the original files
generated from the test.  All results related to the test are kept in the
the sub-folder.


## Data ##

The data/data folder will contain a sub-folder for each test.  Usually the folder
name is the test number.

If you choose, you can put the sql file in any folder and provide the full path
to the sql file at run time.

