# wikidata-properties-dumper
A python script to get a JSON file listing wikidata properties ids and their label in a given language

## Properties Dumps

* [English](properties/en.json)
* [French](properties/fr.json)
* [German](properties/de.json)

## How to use this

```bash
python dumper.py [lang]
```
Where lang can be one of the available languages (see all supported with
`python dumper.py --help`)

## Adding more languages
It's simple to add more languages.

   1. Fork [https://quarry.wmflabs.org/query/50295](https://quarry.wmflabs.org/query/50295) (button on top-right)
   2. Change `en` in the line `AND wbxl_language   = 'en'` to you language's 2-letter code (e.g. 'pl' for Polish)
   3. Click `Submit query` and wait until it finishes (may take minutes)
   4. edit the file `queries.json` add another line *at the top* like:

      ```json
      "XX": { "query": "YYYYY", "json": "ZZZZZZ" },
      ```

      Where:
        - `XX` is the language 2-character code
        - `YYYYY` is the query id (it's on the URL of your fork)
        - `ZZZZZZ` is the results id. You can get it by on your fork, after having submitted the query, you click on `Download data`
        and right-click over `JSON` and click `Copy link location` (or
        equivalent). If you paste it somewhere else, you'll find the
        number in that URL.

    5. Save the file
    6. try running the dumber now and it should support the new language
    7. (optional) open a Pull Request on github to add those changes


## Implementation

This uses the quarry service to query the wikidata database with the
following query (for the english labels)

```sql
SELECT
	CONCAT('P', wbpt_property_id),
	wbx_text
FROM wbt_property_terms
	INNER JOIN wbt_term_in_lang ON wbpt_term_in_lang_id = wbtl_id
	INNER JOIN wbt_type ON wbtl_type_id = wby_id
	INNER JOIN wbt_text_in_lang ON wbtl_text_in_lang_id = wbxl_id
	INNER JOIN wbt_text  ON wbxl_text_id = wbx_id
WHERE
    wby_name        = 'label'
    AND wbxl_language   = 'en'
```

See the above query in action [here](https://quarry.wmflabs.org/query/50295) and feel free to play around with it by forking it.

## Credits

This is a reimplementation in python of the deprecated [wikidata-properties-dumper](https://github.com/maxlath/wikidata-properties-dumper) by maxlath.