import pandas as pd
import requests
import time

character = pd.read_table('./data/character.metadata.tsv', header = None)
character.columns = ['wikipedia_movie_id','rebase_movie_ID','Movie release date','character_name','Actor_DOB','Actor_gender','actor_height','Actor_etnicity','Actor_name','Actor_age_at_movie_release','Freebase_character_map','Freebase_character_ID','Freebase_actor_ID']

sent= pd.read_csv('./data/plot_sentiment.csv')
sentiment = sent.wiki_id.drop_duplicates()
ethn = character.Actor_etnicity.drop_duplicates()

dict_ethnicities = {}

def map_ethnicities(arr_ethn):
    """
    Queries the FreeBase dump to get ethnicities as dict instead of Freebase ID.
    :param arr_ethn: array of ethnicities
    :return:
    """
    etn = []
    for x in arr_ethn[1:]:
        time.sleep(1.4)
        x = x.split('/')[2]
        query = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json&query=PREFIX%20wd%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fentity%2F%3E%0APREFIX%20wdt%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fprop%2Fdirect%2F%3E%0APREFIX%20wikibase%3A%20%3Chttp%3A%2F%2Fwikiba.se%2Fontology%23%3E%0A%0ASELECT%20%20%3Fs%20%3FsLabel%20WHERE%20%7B%0A%20%3Fs%20wdt%3AP646%20%22%2Fm%2F{}%22.%0A%0A%20%20%20SERVICE%20wikibase%3Alabel%20%7B%0A%20%20%20%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22%20.%0A%20%20%20%7D%0A%20%7D'.format(x)
        response_json = requests.get(query).json()['results']['bindings']
        if len(response_json) != 0 :
            etn.append(response_json[0]['sLabel']['value'])
        else :
            etn.append(-1)
    return arr_ethn, etn


arr_etn, etn = map_ethnicities(sentiment)
test = pd.DataFrame({'id' : arr_etn[1:], 'ethnicity' : etn})
test.to_csv('./data/etnicities.csv')