mendeley-extractions
====================

This is a simple experimental script for extracting data from a users' Mendeley library. It uses a very lightly modified version of the [example Mendeley API client](https://github.com/Mendeley/mendeley-oapi-example).

### Extraction types
* **Paper-keywords:** extracts keywords from each paper, along with some other basic metadata.
* **Co-author networks:** not yet implemented.

### Output types
* **CSV:** Comma-separated values
* **TSV:** Tab-separated values
* **SIF:** Not yet implemented
* **XML:** Not yet implemented

Installation and use
--------------------

* Download and unpack this repository to some folder on your computer, e.g. {HOME}/scripts
* (Get a Mendeley API key)[http://dev.mendeley.com/applications/register/], and update the values in config.json
* In a new terminal window, go to the folder where you put this script, and open a new python shell:

```
$ python
```

* Import the module, and run the interface() method:

```
>>> import mendeley_extractions as me
>>> me.interface()
```

* Follow the prompts.

Questions, comments, concerns
--------------------
erick [dot] peirson [at] asu [dot] edu


