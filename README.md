# Calibre Audiobook Plugin

This is a simple audiobook plugin for [Calibre](https://calibre-ebook.com/) designed to extract and display metadata from audiobooks. The plugin reads basic metadata such as title, author, description and cover providing a streamlined way to organize and manage your audiobook collection in Calibre.

**Features include:**
* Extracts title, authors, description, year, cover
* Strips unwanted parts from the metadata (e.g., "(Unabridged)" suffix)
* Automatically extracts and displays audiobook duration


Note: To use the duration feature, you must first create a custom column in Calibre:
1. Go to Preferences > Add your own columns
2. Click "Add custom column"
3. Set Lookup name to: duration
4. Set Column heading to: Duration
5. Set Column type to: Text, column shown in the Tag browser

The plugin will then automatically populate this column with the audiobook's duration in HH:MM:SS format.

**Todo - Update Existing Audio:**

Menu button that extracts metadata and updates audiobooks that were imported before the plugin was installed.
* Bulk update feature to refresh metadata for multiple books
* Selective metadata update - choose which fields to update
