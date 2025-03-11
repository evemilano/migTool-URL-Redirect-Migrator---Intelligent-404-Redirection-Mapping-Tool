# %%
### .\script\migTool\migenv\Scripts\activate ### win
### source script\migTool\migenv\Scripts\activate ### linux

### to do:
# - add a function to check if the previous folder level is 200 available

# %%

import logging
import time

# Logging for library loading
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
def log_loading(library_name):
    logging.info(f"Loading {library_name}")

# Standard libraries
log_loading("datetime")
import datetime

log_loading("os")
import os

log_loading("io")
import io

log_loading("re")
import re

# URL and HTTP processing
log_loading("urllib.parse")
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode, unquote

log_loading("httpx")
import httpx

# Data manipulation and analysis
log_loading("pandas")
import pandas as pd

log_loading("numpy")
import numpy as np

# Signal processing
log_loading("scipy.signal")
from scipy.signal import argrelextrema

# String similarity
log_loading("fuzzywuzzy")
from fuzzywuzzy import fuzz

log_loading("difflib")
import difflib
from difflib import SequenceMatcher

log_loading("Levenshtein")
import Levenshtein as lev

log_loading("spacy")
import spacy

log_loading("jellyfish")
from jellyfish import jaro_winkler_similarity

# Parallel processing
log_loading("joblib")
from joblib import Parallel, delayed

# Machine learning and NLP
log_loading("sklearn.feature_extraction.text")
from sklearn.feature_extraction.text import TfidfVectorizer

log_loading("sklearn.metrics.pairwise")
from sklearn.metrics.pairwise import cosine_similarity

log_loading("BERTopic")
from bertopic import BERTopic


# %%
### OPZIONI ###

use_404check = 'y'
use_fuzzy = 'y'
use_levenshtein = 'y'
use_jaccard = 'y'
use_hamming = 'y'
use_ratcliff = 'y'
use_tversky = 'y'
use_spacy = 'y'
use_vector = 'y'
use_jaro_winkler = 'y'
use_bertopic = 'y'
# secondi di pausa tra il crawling per check status code
pauza = 1




def load_nlp():
    language = input("Scegli la lingua (IT/EN): ").strip().lower()
    
    if language == "it":
        nlp = spacy.load("it_core_news_lg", disable=["tagger", "parser", "ner"])
        print("Modello italiano caricato.")
    elif language == "en":
        nlp = spacy.load("en_core_news_lg", disable=["tagger", "parser", "ner"])
        print("English model loaded.")
    else:
        print("Scelta non valida. Riprova.")
        return load_nlp()  # Riprova in caso di input errato
    
    return nlp
if use_spacy == 'y':
    nlp = load_nlp()



# %%

# Configura il logging
logging.basicConfig(
    level=logging.INFO,  # Imposta il livello minimo di log che vuoi vedere (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(levelname)s - %(message)s',  # Formato del messaggio di log
    handlers=[
        logging.StreamHandler()  # Stampa i log nella console
    ]
)


# %%
# Percorso della cartella
# Ottieni il percorso assoluto della directory dello script corrente
script_directory = os.path.dirname(os.path.abspath(__file__))
# Percorso della cartella input rispetto alla directory dello script
folder_path = os.path.join(script_directory, "input")
# Creazione della cartella se non esiste
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    
#apri url live
print('Carica URL del sito live, oppure URL in 404, che dovranno venire redirezionati')
# Lista dei file Excel nella cartella
excel_files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx") or f.endswith(".xls")]

# Controlla se ci sono file Excel nella cartella
if excel_files:
    print("Ecco l'elenco dei file Excel presenti nella cartella:")
    for index, file in enumerate(excel_files, start=1):
        print(f"{index}. {file}")
else:
    print("Nessun file Excel trovato nella cartella specificata.")

# %%
# fogli disponibili
while True:
    try:
        file_number = int(input("Carica URL del sito live, oppure URL in 404, che dovranno venire redirezionati. Inserisci il numero corrispondente al file da caricare: "))
        if 1 <= file_number <= len(excel_files):
            filename = os.path.join(folder_path, excel_files[file_number - 1])
            xl = pd.ExcelFile(filename)
            break
        else:
            print("Il numero inserito non corrisponde a nessun file. Riprova.")
    except ValueError:
        print("Si prega di inserire un numero valido.")

# ottieni la lista dei nomi dei fogli del file Excel
nomi_fogli = xl.sheet_names

# stampa i nomi dei fogli
print("I fogli disponibili sono:")
for i, nome in enumerate(nomi_fogli):
    print(f"{i + 1}. {nome}")

# %%
# chiedi all'utente di selezionare un foglio da leggere
while True:
    try:
        indice_foglio = int(input("Inserisci il numero del foglio con gli URL da redirezionare: ")) - 1
        if 0 <= indice_foglio < len(nomi_fogli):
            nome_foglio = nomi_fogli[indice_foglio]
            break
        else:
            print("Il numero inserito non è valido. Riprova.")
    except ValueError:
        print("Inserisci un numero valido. Riprova.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}. Riprova.")

# leggi il foglio selezionato dall'utente
df = pd.read_excel(filename, sheet_name=nome_foglio)
df.head(5)
print('foglio letto')

# Crea una copia del dataframe originale
df1 = df.copy()

# Mostra all'utente le colonne disponibili nel dataframe
print("Here are the columns available in the dataframe:")
for i, col in enumerate(df1.columns):
    print(f"{i}: {col}")

# %%
# Chiedi all'utente di selezionare la colonna da mantenere
colonna_index = input("Inserisci il numero colonna con gli URL da redirezionare: ")

# Continua a chiedere all'utente di inserire una colonna finché non viene fornita un'input valida
while not colonna_index.isdigit() or int(colonna_index) >= len(df1.columns):
    colonna_index = input("Invalid input. Please enter a valid column number: ")

colonna_da_mantenere = df1.columns[int(colonna_index)]

# %%
# Cancella tutte le colonne tranne quella selezionata dall'utente
df1 = df1[[colonna_da_mantenere]]

# rimuovi le righe con valori nulli o vuoti
df1 = df1.dropna()
df1.rename(columns={colonna_da_mantenere: "LIVE URLS"}, inplace=True)
print('foglio rinominato')
# togli duplicazioni
df1.drop_duplicates(subset='LIVE URLS', keep='first', inplace=True)
print('duplicaizoni rimosse')
# Stampa il dataframe risultante
df1.head(5)

# %%
#apri URL dev
if excel_files:
    print("Ecco l'elenco dei file Excel presenti nella cartella. Selezione il file DEV con gli URL finali:")
    for index, file in enumerate(excel_files, start=1):
        print(f"{index}. {file}")

# %%
while True:
    try:
        file_number = int(input("Inserisci il numero corrispondente al file da caricare con gli URL finali: "))
        if 1 <= file_number <= len(excel_files):
            filename = os.path.join(folder_path, excel_files[file_number - 1])
            xl = pd.ExcelFile(filename)
            break
        else:
            print("Il numero inserito non corrisponde a nessun file. Riprova.")
    except ValueError:
        print("Si prega di inserire un numero valido.")

nomi_fogli2 = xl.sheet_names
# stampa i nomi dei fogli
print("I fogli disponibili sono:")
for i, nome in enumerate(nomi_fogli2):
    print(f"{i + 1}. {nome}")
   

# %%
# chiedi all'utente di selezionare un foglio da leggere con gestione caratteri speciali nei nomi dei fogli
while True:
    try:
        indice_foglio2 = int(input("Inserisci il numero del foglio che desideri leggere con gli URL finali: ")) - 1
        if 0 <= indice_foglio2 < len(nomi_fogli2):
            break
        else:
            print("Il numero inserito non è valido. Riprova.")
    except ValueError:
        print("Inserisci un numero valido. Riprova.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}. Riprova.")

# leggi il foglio selezionato dall'utente
df2 = pd.read_excel(filename, sheet_name=indice_foglio2)
df2.head(5)
print('foglio letto')
df2.head(5)


# %%
# Mostra all'utente le colonne disponibili nel dataframe
print("Queste sono le colonne disponibili nel foglio:")
for i, col in enumerate(df2.columns):
    print(f"{i}: {col}")

# %%
# Crea una copia del dataframe originale
df22 = df2.copy()

# Chiedi all'utente di selezionare la colonna da mantenere
colonna_index2 = input("inserisci il numero della colonna che contiene gli URL finali: ")

# Continua a chiedere all'utente di inserire una colonna finché non viene fornita un'input valida
while not colonna_index2.isdigit() or int(colonna_index2) >= len(df22.columns):
    colonna_index2 = input("Invalid input. Please enter a valid column number: ")

colonna_da_mantenere2 = df22.columns[int(colonna_index2)]

df22.head(5)


# %%
print('Fine uploading')
print('inizio pulizia')
# Cancella tutte le colonne tranne quella selezionata dall'utente
df22 = df22[[colonna_da_mantenere2]]

# rimuovi le righe con valori nulli o vuoti
df22 = df22.dropna()
df22.rename(columns={colonna_da_mantenere2: "DEV URLS"}, inplace=True)
print('foglio rinominato')
# togli duplicazioni
df22.drop_duplicates(subset='DEV URLS', keep='first', inplace=True)
print('duplicaizoni rimosse')
# Stampa il dataframe risultante
print('URL da redirezionare caricati')
df22.head(5)

# %%
# funzione pulizia URL
def clean_url(url):
    # Se l'URL è vuoto, restituisce una stringa vuota
    if not url:
        return ''
    # Decodifica l'URL e lo analizza nelle sue componenti
    parsed = urlparse(unquote(url))
    # Divide il percorso in segmenti, rimuove i segmenti vuoti e li unisce con spazi
    path = ' '.join(filter(None, parsed.path.split('/')))
    # Estrae i parametri dall'URL
    params = parsed.params
    if params:
        # Se ci sono parametri, li ordina alfabeticamente
        params = '&'.join(sorted(params.split('&')))
    # Sostituisce trattini, underscore e cancelletti con spazi nel percorso
    path = re.sub(r'[-_#]', ' ', path)
    # Ricostruisce l'URL pulito: percorso + parametri (se presenti)
    cleaned_url = (path + ('?' + params if params else '')).strip()
    # Converte l'URL pulito in minuscolo e lo restituisce
    return cleaned_url.lower()

# %%
# crea nuovi df
mig_df_404 =df1.copy()
mig_df_live = df22.copy()


# %%
# stampa 404
mig_df_404.head(1)


# %%
# stampa live
mig_df_live.head(1)

# %%
# rinomina la prima colonna
#mig_df_404.columns.values[0] = 'URL'
#mig_df_live.columns.values[0] = 'URL'
# 202502 Rename columns using rename method instead of direct assignment
mig_df_404 = mig_df_404.rename(columns={mig_df_404.columns[0]: 'URL'})
mig_df_live = mig_df_live.rename(columns={mig_df_live.columns[0]: 'URL'})

# Verifica le colonne
print("Colonne mig_df_404:", mig_df_404.columns)
print("Colonne mig_df_live:", mig_df_live.columns)


# Convert URL columns to string type to handle numeric URLs correctly
mig_df_404['URL'] = mig_df_404['URL'].astype(str)
mig_df_live['URL'] = mig_df_live['URL'].astype(str)


#print(mig_df_404.columns)
#print(mig_df_live.columns)
mig_df_404.columns = mig_df_404.columns.str.strip()
mig_df_live.columns = mig_df_live.columns.str.strip()
mig_df_404.head(1)

# %%

# rimuovi parametri utm

from urllib.parse import urlparse, urlunparse

def remove_utm_parameters(url):
    """
    Rimuove tutti i parametri da un URL se contiene il parametro 'utm'.
    """
    if isinstance(url, str):
        parsed_url = urlparse(url)
        # Controlla se 'utm' è nei parametri
        if 'utm' in parsed_url.query:
            # Ricostruisce l'URL senza parametri
            url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
    return url

# pulizia url da spazi e caratteri non stampabili
def clean_invalid_characters(url):
    """
    Rimuove caratteri non validi, come spazi, nuove righe e caratteri non stampabili, da un URL.
    """
    if isinstance(url, str):
        # Rimuove spazi all'inizio/fine e caratteri non stampabili
        url = url.strip()
        url = ''.join(c for c in url if c.isprintable())
    return url
# Pulisce gli URL nel DataFrame
mig_df_404['URL'] = mig_df_404['URL'].apply(clean_invalid_characters).apply(remove_utm_parameters)

# rimuovi duplicati
print("Removing duplicates...")  # Message above the progress bar
mig_df_404 = mig_df_404.drop_duplicates(subset='URL')
mig_df_live = mig_df_live.drop_duplicates(subset='URL')


urls = mig_df_404['URL'].tolist()



# %%
mig_df_404['Cleaned URLs'] = mig_df_404['URL'].apply(clean_url)
mig_df_live['Cleaned URLs'] = mig_df_live['URL'].apply(clean_url)
mig_df_404

# %%
# Stampa solo le prime 10 righe dei dataframe
#print("Top records - 404 URLs:")
mig_df_404.head(3)
#st.write(f"Total rows in 404 dataframe: {len(mig_df_404)}")  # Aggiunto
print(f"Total rows in 404 dataframe: {len(mig_df_404):,}")  # Con formattazione delle migliaia

#print("Top records - Live URLs:")
mig_df_live.head(3)
#st.write(f"Total rows in Live dataframe: {len(mig_df_live)}")  # Aggiunto
print(f"Total rows in Live dataframe: {len(mig_df_live):,}")  # Con formattazione delle migliaia


# %%
initial404 = len(mig_df_404)  # Calcola il numero totale di URL
print(f'URL 404 inviati: {initial404}')

# %%
print('Verifica URL 404')

# %%
# check veri 404 in mig_df_404
# Configurazione del logging



def check_status_http2(client, url, index, total_urls):
    try:
        response = client.get(url, follow_redirects=True, timeout=30)
        status_code = response.status_code
        logging.info(f"Verificato URL {index+1} di {total_urls}: {url} - Status: {status_code}")
        return status_code
    except httpx.TimeoutException:
        logging.warning(f"Timeout per URL {index+1} di {total_urls}: {url}")
        return 'timeout'
    except httpx.RequestError as e:
        logging.error(f"Errore nella verifica di URL {index+1} di {total_urls}: {url} - Errore: {e}")
        return 'error'

def check_urls_http2(urls, pause):
    results = []
    total_urls = len(urls)
    
    # Abilita HTTP/2 nel client
    with httpx.Client(http2=True, headers={
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36'
    }) as client:
        for index, url in enumerate(urls):
            cleaned_url = clean_invalid_characters(url)
            try:
                status = check_status_http2(client, cleaned_url, index, total_urls)
                results.append((url, status))  # Mantiene l'URL originale per riferimento
            except Exception as e:
                logging.error(f"Errore durante il controllo dell'URL {index+1}: {cleaned_url} - Errore: {e}")
                results.append((url, 'invalid'))
            time.sleep(pause)
    
    return results


if use_404check == 'y':
    # Pulisce gli URL nel DataFrame
    mig_df_404['URL'] = mig_df_404['URL'].apply(clean_invalid_characters)
    urls = mig_df_404['URL'].tolist()
    results = check_urls_http2(urls, pause=pauza)
    
    # Aggiorna il DataFrame con i risultati
    status_dict = dict(results)
    mig_df_404['status_code'] = mig_df_404['URL'].map(status_dict)
    
    # Crea il DataFrame per gli URL problematici
    #problematic_codes = [403, 430, 500, 501, 502, 503, 504, 'timeout', 'error']
    problematic_codes = [403, 430, 500, 501, 502, 503, 504, 'timeout', 'error', 'invalid']

    df_problematic_urls = mig_df_404[mig_df_404['status_code'].isin(problematic_codes)][['URL', 'status_code']]

    # Rimuovi gli URL che non sono effettivamente 404
    mig_df_404 = mig_df_404[mig_df_404['status_code'] == 404]

    logging.info(f"Totale URL verificati: {len(urls)}")
    logging.info(f"URL problematici: {len(df_problematic_urls)}")
    logging.info(f"URL 404 confermati: {len(mig_df_404)}")


# %%
if df_problematic_urls.empty:
    print("Il DataFrame df_problematic_urls è vuoto")
else:
    print("Il DataFrame df_problematic_urls non è vuoto")

print(df_problematic_urls)

# %%
# mostra pagine non 404
# Filtrare mig_df_404 per includere solo righe con status code diverso da 404
df_non_404 = mig_df_404[mig_df_404['status_code'] != 404]
# Stampare il nuovo dataframe
df_non_404

# %%
# Filtra per mantenere solo gli URL con stato 404
mig_df_404 = mig_df_404[mig_df_404['status_code'] == 404]
mig_df_404.head(3)

# %%
final_urls = len(mig_df_404)  # Calcola il numero totale di URL
print(f'URL 404 rimossi: {initial404 - final_urls}')
print(f'URL 404 rimanenti: {final_urls}')

# %%
# Seconda scansione per URL problematici
def retry_problematic_urls():
    """
    Riprova le richieste per gli URL problematici usando HTTP/2.
    """
    with httpx.Client(http2=True, headers={
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36'
    }) as client:
        for i, row in df_problematic_urls.iterrows():
            url = row['URL']
            time.sleep((pauza * 2) + 3)  # Pausa prima di riprovare
            status = check_status_http2(client, url, i, len(df_problematic_urls))
            df_problematic_urls.at[i, 'status_code'] = status  # Aggiorna il risultato nel DataFrame
            
            # Se lo status è 404, aggiungi l'URL a mig_df_404
            if status == 404:
                new_row = pd.DataFrame({'URL': [url], 'status_code': [status]})
                global mig_df_404
                mig_df_404 = pd.concat([mig_df_404, new_row], ignore_index=True)


# Verifica se il DataFrame è vuoto e chiama la funzione se non lo è
if not df_problematic_urls.empty:
    print("Riprovo gli URL problematici...")
    retry_problematic_urls()
else:
    print("Il DataFrame df_problematic_urls è vuoto")


# rimuovi duplicati
mig_df_404 = mig_df_404.drop_duplicates(subset='URL')


# %%
print('Inizio matching')

# %%
# genera df finale
final_mig_df = mig_df_404.copy()

# %%
print(f'Generazione df finale final_mig_df: {final_mig_df}')















# %%
# Fuzzy (Fuzzy Matching)
# Punto di forza: Eccelle nel trovare corrispondenze in stringhe con piccole differenze 
# o errori di battitura, utilizzando una misura di somiglianza basata sul numero di operazioni 
# di modifica necessarie per trasformare una stringa nell'altra.

# Limitazione: Potrebbe non essere ottimale per confronti su larga scala a causa della sua 
# complessità computazionale e può fornire punteggi elevati anche per stringhe che non sono strettamente correlate.

def find_best_match_fuzzy(url, live_df, selected_column, threshold):
    cleaned_url = clean_url(url)
    best_score = 0
    best_match = None
    for index, row in live_df.iterrows():
        score = fuzz.token_sort_ratio(cleaned_url, row['Cleaned URLs'])
        if score > best_score:
            best_score = score
            best_match = row[selected_column]

    if best_score >= threshold:
        return best_match
    return None

def compute_max_similarity(live_url, mig_df_404):
    max_score = 0
    for dev_url in mig_df_404['Cleaned URLs']:
        score = fuzz.token_sort_ratio(live_url, dev_url)
        max_score = max(max_score, score)
    return max_score

# Trova la soglia ottimale utilizzando l'algoritmo dell'"elbow"
def find_optimal_threshold(max_similarity_scores):
    hist, bin_edges = np.histogram(max_similarity_scores, bins='auto', density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    hist_derivative = np.diff(hist) / np.diff(bin_centers)
    extrema = argrelextrema(hist_derivative, np.greater)
    if extrema[0].size > 0:
        elbow_index = extrema[0][0]
        threshold = bin_centers[elbow_index]
    else:
        print("No extrema found. Falling back to default threshold of 50.")
        threshold = 50  # Imposta una soglia di default se non vengono trovati estremi.
    return threshold

if use_fuzzy == 'y':
    print("Esecuzione algoritmo Fuzzy...")  # Message above the progress bar
    start_time = time.time()  # Misura il tempo di esecuzione

    # Parallel computation of max similarity scores
    num_cores = -1  # Use all available cores
    # Calcolo e stampa del numero totale di combinazioni da calcolare
    total_combinations = len(mig_df_live) * len(mig_df_404)
    max_similarity_scores = Parallel(n_jobs=num_cores)(delayed(compute_max_similarity)(live_url, mig_df_404) for live_url in mig_df_live['Cleaned URLs'])
    #st.write("Optimal threshold calculation...")  # Message above the progress bar
    # Find optimal threshold
    print("Optimal threshold calculation...")  # Message above the progress bar
    threshold = find_optimal_threshold(np.array(max_similarity_scores))
    # FUZZY Calcola la soglia ottimale
    final_mig_df['Fuzzy'] = final_mig_df['URL'].apply(lambda url: find_best_match_fuzzy(url, mig_df_live, "URL", threshold))
    # Calcola il punteggio Fuzzy e aggiungilo alla colonna "Fuzzy" nel DataFrame finale
    final_mig_df['Fuzzy_Score'] = final_mig_df['URL'].apply(lambda url: fuzz.token_sort_ratio(clean_url(url), clean_url(final_mig_df['Fuzzy'].iloc[0])))
    # normalizza da 0-100 a 0-1
    final_mig_df['Fuzzy_Score'] = final_mig_df['Fuzzy_Score'] / 100

    # Stampa il tempo di esecuzione
    end_time = time.time()
    print(f"Algoritmo Fuzzy completato in {end_time - start_time:.2f} secondi")













# %%
# Levenshtein (Distanza di Levenshtein)
# Punto di forza: Misura efficacemente la distanza di modifica tra due stringhe, considerando inserimenti, 
# cancellazioni e sostituzioni. È utile per correzioni ortografiche e confronti di testo.
# Limitazione: La sua efficienza diminuisce con l'aumentare della lunghezza delle stringhe e non tiene conto 
# # della struttura semantica o del significato delle parole.


def find_most_similar_levenshtein(url, live_df):
    cleaned_url = clean_url(url)
    # Apply the Levenshtein distance calculation across the 'Cleaned URLs' column
    distances = live_df['Cleaned URLs'].apply(lambda x: lev.distance(cleaned_url, x))
    # Find the index of the minimum distance
    min_index = distances.idxmin()
    # Return the corresponding original URL
    return live_df.at[min_index, "URL"]

if use_levenshtein == 'y':
    print("Esecuzione algoritmo Levenshtein...")  # Message above the progress bar
    start_time = time.time()  # Misura il tempo di esecuzione
    final_mig_df['Levenshtein'] = final_mig_df['Cleaned URLs'].apply(lambda url: find_most_similar_levenshtein(url, mig_df_live))
    final_mig_df['Levenshtein_Score'] = final_mig_df.apply(lambda row: lev.distance(row['Cleaned URLs'], clean_url(row['Levenshtein'])), axis=1)
    max_len = final_mig_df.apply(lambda row: max(len(row['Cleaned URLs']), len(clean_url(row['Levenshtein']))), axis=1)
    final_mig_df['Levenshtein_Score'] = 1 - (final_mig_df['Levenshtein_Score'] / max_len)
    # Stampa il tempo di esecuzione
    end_time = time.time()
    print(f"Algoritmo Levenshtein completato in {end_time - start_time:.2f} secondi")




# %%
# Jaccard (Indice di Jaccard)
# Punto di forza: Misura la somiglianza e la diversità tra campioni di insiemi. È semplice e 
# efficace per confronti di insiemi, come gruppi di parole o caratteri.
# Limitazione: Non considera la frequenza dei termini e può non essere efficace per testi 
# con molte parole comuni ma con significati diversi.

def jaccard_similarity(str1, str2):
    """
    Calcola la somiglianza di Jaccard tra due stringhe.
    """
    set1 = set(str1)
    set2 = set(str2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0

def parallel_jaccard(mig_df_404, live_df, num_jobs=-1):
    """
    Parallelizza il calcolo della somiglianza di Jaccard.
    """
    # Creare un dizionario {Cleaned URL: Original URL}
    live_urls_dict = dict(zip(live_df['Cleaned URLs'], live_df['URL']))
    
    def jaccard_match(cleaned_url):
        """
        Trova il miglior match per un URL usando la similarità di Jaccard.
        """
        best_score = 0
        best_match_cleaned = None
        for live_cleaned_url in live_urls_dict.keys():
            score = jaccard_similarity(cleaned_url, live_cleaned_url)
            if score > best_score:
                best_score = score
                best_match_cleaned = live_cleaned_url
        # Recupera l'URL originale corrispondente
        best_match_original = live_urls_dict.get(best_match_cleaned, None)
        return best_match_original, best_score

    # Parallelizza il calcolo
    results = Parallel(n_jobs=num_jobs)(
        delayed(jaccard_match)(row['Cleaned URLs']) for _, row in mig_df_404.iterrows()
    )
    
    # Assegna i risultati al DataFrame
    mig_df_404[['Jaccard', 'Jaccard_Score']] = pd.DataFrame(results, index=mig_df_404.index)
    return mig_df_404

# Applicare la funzione
if use_jaccard == 'y':
    print("Esecuzione algoritmo Jaccard...")  # Per monitorare l'operazione
    start_time = time.time()  # Misura il tempo di esecuzione
    # Applica la parallelizzazione al calcolo di Jaccard
    final_mig_df = parallel_jaccard(final_mig_df, mig_df_live)
    # Stampa il tempo di esecuzione
    end_time = time.time()
    print(f"Algoritmo Jaccard completato in {end_time - start_time:.2f} secondi")





# %%
# Algoritmo di Hamming (Hamming Distance)
# Utilizzo: L'algoritmo di Hamming è comunemente utilizzato per misurare la distanza di Hamming, 
# ovvero il numero di posizioni in cui due stringhe di uguale lunghezza differiscono. Questo metodo 
# è spesso impiegato in contesti di correzione di errori e codici di rilevamento.
# Punto di forza: L'algoritmo di Hamming è particolarmente efficace e semplice da implementare per 
# confrontare due stringhe di uguale lunghezza, fornendo una misura chiara e diretta del numero di 
# differenze carattere per carattere tra di esse.
# Limitazione: Uno dei limiti principali è che l'algoritmo di Hamming funziona solo con stringhe 
# della stessa lunghezza. Questo lo rende meno flessibile rispetto ad altri metodi di confronto di 
# stringhe come Levenshtein o Jaccard, che possono confrontare stringhe di lunghezza diversa. Inoltre, 
# non tiene conto della posizione delle differenze all'interno della stringa, considerando ogni discrepanza allo stesso modo.

def hamming_distance(str1, str2):
    if len(str1) != len(str2):
        raise ValueError("Le stringhe devono avere la stessa lunghezza")
    return sum(el1 != el2 for el1, el2 in zip(str1, str2))

def find_most_similar_hamming(url, live_df):
    cleaned_url = clean_url(url)
    best_score = float('inf')
    best_match = None
    for index, row in live_df.iterrows():
        if len(cleaned_url) == len(row['Cleaned URLs']):
            score = hamming_distance(cleaned_url, row['Cleaned URLs'])
            if score < best_score:
                best_score = score
                best_match = row['URL']
    return best_match, best_score

if use_hamming == 'y':
    print("Esecuzione algoritmo Hamming...")
    start_time = time.time()  # Misura il tempo di esecuzione
    final_mig_df[['Hamming', 'Hamming_Score']] = final_mig_df['Cleaned URLs'].apply(lambda url: find_most_similar_hamming(url, mig_df_live)).apply(pd.Series)
    # Gestione dei casi NaN e conversione sicura
    def safe_len(x):
        return len(clean_url(x)) if isinstance(x, str) else 0
    max_len = final_mig_df.apply(lambda row: max(safe_len(row['Cleaned URLs']), 
                                                 safe_len(row['Hamming'])), axis=1)
    # Evita la divisione per zero
    final_mig_df['Hamming_Score'] = final_mig_df['Hamming_Score'].apply(lambda x: 1 - (x / max_len.max()) if pd.notna(x) else 0)
    # Stampa il tempo di esecuzione
    end_time = time.time()
    print(f"Algoritmo Hamming completato in {end_time - start_time:.2f} secondi")



# %%
# Ratcliff/Obershelp (Algoritmo Ratcliff/Obershelp)
# Punto di forza: Buono per rilevare somiglianze di pattern in stringhe, basandosi sulla 
# massima sottostringa comune. Utile per il rilevamento del plagio o la comparazione di testi.
# Limitazione: Può essere meno efficace con testi molto lunghi o con numerose differenze minori.


def ratcliff_similarity(cleaned_url, live_urls_dict):
    """
    Calcola la somiglianza Ratcliff/Obershelp e restituisce l'URL originale con il punteggio.
    """
    best_score = 0
    best_match_cleaned = None

    for live_cleaned_url in live_urls_dict.keys():
        score = SequenceMatcher(None, cleaned_url, live_cleaned_url).ratio()
        if score > best_score:
            best_score = score
            best_match_cleaned = live_cleaned_url

    # Recupera l'URL originale corrispondente
    best_match_original = live_urls_dict.get(best_match_cleaned, None)
    return best_match_original, best_score

def parallel_ratcliff(mig_df_404, live_df, num_jobs=-1):
    """
    Esegue il calcolo Ratcliff/Obershelp in parallelo.
    """
    # Creare un dizionario {Cleaned URL: Original URL}
    live_urls_dict = dict(zip(live_df['Cleaned URLs'], live_df['URL']))
    
    def process_row(row):
        cleaned_url = row['Cleaned URLs']
        return ratcliff_similarity(cleaned_url, live_urls_dict)

    # Parallelizza il calcolo
    results = Parallel(n_jobs=num_jobs)(
        delayed(process_row)(row) for _, row in mig_df_404.iterrows()
    )
    
    # Assegna i risultati al DataFrame
    mig_df_404[['Ratcliff', 'Ratcliff_Score']] = pd.DataFrame(results, index=mig_df_404.index)
    return mig_df_404

# Applicazione della funzione
if use_ratcliff == 'y':
    print("Esecuzione algoritmo Ratcliff...")
    start_time = time.time()
    # Calcolo parallelo Ratcliff
    final_mig_df = parallel_ratcliff(final_mig_df, mig_df_live)
    end_time = time.time()
    print(f"Algoritmo Ratcliff completato in {end_time - start_time:.2f} secondi")



# %%
# Tversky (Indice di Tversky)
# Punto di forza: Un'estensione dell'Indice di Jaccard, questo indice può essere regolato 
# per dare più peso a specifici tipi di differenze. È utile quando si vogliono ponderare in modo diverso le somiglianze e le differenze.
# Limitazione: Richiede una scelta accurata dei parametri per bilanciare adeguatamente le 
# somiglianze e le differenze, altrimenti può portare a risultati fuorvianti.
'''
def tversky_index(str1, str2, alpha=0.5, beta=0.5):
    set1 = set(str1)
    set2 = set(str2)
    common = set1.intersection(set2)
    unique_to_set1 = set1 - set2
    unique_to_set2 = set2 - set1
    score = len(common) / (len(common) + alpha * len(unique_to_set1) + beta * len(unique_to_set2))
    return score
'''

def tversky_index(str1, str2, alpha=0.5, beta=0.5):
    set1 = set(str1)
    set2 = set(str2)
    common = set1.intersection(set2)
    unique_to_set1 = set1 - set2
    unique_to_set2 = set2 - set1
    denominator = len(common) + alpha * len(unique_to_set1) + beta * len(unique_to_set2)
    if denominator == 0:
        return 0  # oppure un altro valore che abbia senso per la tua logica
    score = len(common) / denominator
    return score

def find_most_similar_tversky(url, live_df):
    cleaned_url = clean_url(url)
    best_score = 0
    best_match = None
    for index, row in live_df.iterrows():
        score = tversky_index(cleaned_url, row['Cleaned URLs'])
        if score > best_score:
            best_score = score
            best_match = row['URL']
    return best_match, best_score

if use_tversky == 'y':
    print("Esecuzione algoritmo Tversky...")
    start_time = time.time()
    #final_mig_df[['Tversky', 'Tversky_Score']] = final_mig_df['URL'].apply(lambda url: find_most_similar_tversky(url, mig_df_live)).apply(pd.Series)
    final_mig_df[['Tversky', 'Tversky_Score']] = final_mig_df['Cleaned URLs'].apply(lambda url: find_most_similar_tversky(url, mig_df_live)).apply(pd.Series)
    end_time = time.time()
    print(f"Algoritmo Tversky completato in {end_time - start_time:.2f} secondi")

# %%
# spaCy

# Spacy (Libreria Spacy per NLP)
# Punto di forza: Ottima per l'analisi semantica e sintattica del testo, utilizzando modelli 
# di linguaggio avanzati. È ideale per compiti di NLP che richiedono una comprensione del contesto e del significato.
# Limitazione: Richiede più risorse computazionali rispetto ad altri metodi più semplici e 
# può essere eccessivo per compiti di confronto testuale basilare.
# Carica il modello spaCy per l'italiano
#nlp = spacy.load("it_core_news_lg")

#nlp = spacy.load("en_core_web_lg")

# Preprocessing: crea un dizionario degli URL pre-elaborati
# Mappa gli URL puliti agli URL originali
cleaned_to_original_url = {clean_url(url): url for url in mig_df_live['URL']}

# Preprocessing: crea un dizionario degli URL pre-elaborati
preprocessed_docs = {clean_url(url): nlp(clean_url(url)) for url in mig_df_live['Cleaned URLs']}

def find_most_similar_spacy(url, preprocessed_docs, cleaned_to_original_url):
    cleaned_url = clean_url(url)
    query_doc = preprocessed_docs.get(cleaned_url, nlp(cleaned_url))
    best_score = 0
    best_match_cleaned = None

    for doc_url, doc in preprocessed_docs.items():
        score = query_doc.similarity(doc)
        if score > best_score:
            best_score = score
            best_match_cleaned = doc_url

    # Recupera l'URL originale corrispondente all'URL pulito
    best_match_original = cleaned_to_original_url.get(best_match_cleaned, None)
    return best_match_original, best_score


if use_spacy == 'y':
    print("Esecuzione algoritmo spaCy...")
    start_time = time.time()
    final_mig_df[['Spacy', 'Spacy_Score']] = final_mig_df['Cleaned URLs'].apply(
        lambda url: find_most_similar_spacy(url, preprocessed_docs, cleaned_to_original_url)
    ).apply(pd.Series)

    end_time = time.time()
    print(f"Algoritmo spaCy completato in {end_time - start_time:.2f} secondi")






# %%
# TF IDF Vectorizer







if use_vector == 'y':
    print("Esecuzione algoritmo Vector...")
    start_time = time.time()

    # Preprocessing: crea un dizionario degli URL pre-elaborati
    cleaned_to_original_url = {clean_url(url): url for url in mig_df_live['URL']}

    def find_best_match_vector(url_404, live_urls, vectorizer, live_vectors):
        # Preprocessa l'URL 404
        cleaned_url_404 = clean_url(url_404)
        query_vector = vectorizer.transform([cleaned_url_404])
        similarities = cosine_similarity(query_vector, live_vectors).flatten()
        
        # Trova l'indice del più simile
        best_match_idx = np.argmax(similarities)
        best_score = similarities[best_match_idx]
        
        # Trova l'URL pulito e poi l'URL originale
        best_match_cleaned = live_urls[best_match_idx]
        best_match_original = cleaned_to_original_url.get(best_match_cleaned, None)
        
        return best_match_original, best_score

    # Crea e adatta il vectorizer
    vectorizer = TfidfVectorizer()
    live_urls = mig_df_live['Cleaned URLs'].apply(clean_url)
    live_vectors = vectorizer.fit_transform(live_urls)

    # Applica la funzione al DataFrame
    final_mig_df[['Vector', 'Vector_Score']] = final_mig_df['Cleaned URLs'].apply(
        lambda x: pd.Series(find_best_match_vector(x, live_urls, vectorizer, live_vectors))
    )

    end_time = time.time()
    print(f"Algoritmo Vector completato in {end_time - start_time:.2f} secondi")


# %%
# JARO-WINKLER

def parallel_jaro_winkler(mig_df_404, live_df, num_jobs=-1):
    """
    Parallelizza il calcolo della somiglianza di Jaro-Winkler.
    """
    # Crea una mappatura tra Cleaned URLs e URL originali
    cleaned_to_original = dict(zip(live_df['Cleaned URLs'], live_df['URL']))
    
    live_urls = live_df['Cleaned URLs'].tolist()  # Lista degli URL live già puliti
    
    def jaro_winkler_match(cleaned_url):
        """
        Trova il miglior match per un URL 404 usando Jaro-Winkler.
        """
        best_score = 0
        best_match_cleaned = None
        for live_url in live_urls:
            score = jaro_winkler_similarity(cleaned_url, live_url)
            if score > best_score:
                best_score = score
                best_match_cleaned = live_url
        # Usa il dizionario per ottenere l'URL originale
        best_match_original = cleaned_to_original.get(best_match_cleaned, None)
        return best_match_original, best_score

    # Parallelizza il calcolo sui core disponibili
    results = Parallel(n_jobs=num_jobs)(
        delayed(jaro_winkler_match)(row['Cleaned URLs']) for _, row in mig_df_404.iterrows()
    )
    
    # Assegna i risultati al DataFrame
    mig_df_404[['Jaro_Winkler', 'Jaro_Winkler_Score']] = pd.DataFrame(results, index=mig_df_404.index)
    return mig_df_404



if use_jaro_winkler == 'y':
    print("Esecuzione algoritmo Jaro-Winkler...")  # Per monitorare il progresso
    start_time = time.time()  # Misura il tempo di esecuzione

    # Applica la parallelizzazione al calcolo di Jaro-Winkler
    final_mig_df = parallel_jaro_winkler(final_mig_df, mig_df_live)

    # Stampa il tempo di esecuzione
    end_time = time.time()
    print(f"Algoritmo Jaro-Winkler completato in {end_time - start_time:.2f} secondi")

# %%

# BERTopic

def apply_bertopic(final_mig_df, mig_df_live, num_jobs=-1):
    # Combina i dati di entrambe le tabelle per costruire i topic
    combined_urls = pd.concat([final_mig_df['URL'], mig_df_live['URL']])
    
    # Esegui BERTopic
    topic_model = BERTopic()
    topics, probs = topic_model.fit_transform(combined_urls)
    
    # Mappa gli URL ai rispettivi topic e probabilità
    url_to_topic = dict(zip(combined_urls, topics))
    url_to_prob = dict(zip(combined_urls, probs))
    
    def find_best_match_bertopic(url):
        """
        Trova il miglior match per un URL dato utilizzando i topic generati.
        """
        topic = url_to_topic.get(url, None)
        if topic is None:  # Se il topic non è presente, restituisci valori vuoti
            return None, 0
        best_match = None
        best_prob = 0
        for live_url in mig_df_live['URL']:
            if url_to_topic[live_url] == topic:
                prob = url_to_prob.get(live_url, 0)
                if prob > best_prob:
                    best_prob = prob
                    best_match = live_url
        return best_match, best_prob

    # Parallelizza la ricerca del miglior match
    results = Parallel(n_jobs=num_jobs)(
        delayed(find_best_match_bertopic)(url) for url in final_mig_df['URL']
    )
    
    # Assegna i risultati al DataFrame
    final_mig_df[['BERTopic', 'BERTopic_Score']] = pd.DataFrame(results, index=final_mig_df.index)
    
    # Normalizza il punteggio di probabilità per renderlo una percentuale corretta
    final_mig_df['BERTopic_Score'] = final_mig_df['BERTopic_Score'].apply(lambda x: round(x, 2) if x > 0 else 0)
    
    return final_mig_df


if use_bertopic == 'y':
    print("Esecuzione algoritmo BERTopic con parallelizzazione...")  # Per monitorare il progresso
    start_time = time.time()  # Misura il tempo di esecuzione
    final_mig_df = apply_bertopic(final_mig_df, mig_df_live, num_jobs=-1)  # Usa tutti i core disponibili
    # Stampa il tempo di esecuzione
    end_time = time.time()
    print(f"Algoritmo BERTopic completato in {end_time - start_time:.2f} secondi")



# %%
final_mig_df.head(4)

# %%

# SCORING

# Dopo aver generato il dataframe finale
selected_algorithms = []
if use_fuzzy == 'y':
    selected_algorithms.append('Fuzzy')
if use_levenshtein == 'y':
    selected_algorithms.append('Levenshtein')
if use_jaccard == 'y':
    selected_algorithms.append('Jaccard')
if use_hamming == 'y':
    selected_algorithms.append('Hamming')
if use_ratcliff == 'y':
    selected_algorithms.append('Ratcliff')
if use_tversky == 'y':
    selected_algorithms.append('Tversky')
if use_spacy == 'y':
    selected_algorithms.append('Spacy')
if use_vector == 'y':
    selected_algorithms.append('Vector')
if use_jaro_winkler == 'y':
    selected_algorithms.append('Jaro_Winkler')
if use_bertopic == 'y':
    selected_algorithms.append('BERTopic')

# %%
# Tscore - We first filter the columns that contain 'Score' in their names
print("TotScore")
score_columns = [col for col in final_mig_df.columns if '_Score' in col]
# Then, we calculate the sum of these columns for each row
final_mig_df['TotScore'] = final_mig_df[score_columns].sum(axis=1)     

# conta agreement
def count_agreement(row, selected_algorithms):
    # Estrai gli URL suggeriti da ciascun algoritmo, escludendo i valori NA
    suggested_urls = [row[algo] for algo in selected_algorithms if pd.notna(row[algo])]
    # Se non ci sono URL validi suggeriti, restituisci 0 e None
    if not suggested_urls:
        return 0, None
    # Conta il numero di volte che ciascun URL appare
    url_counts = {url: suggested_urls.count(url) for url in set(suggested_urls)}
    # Trova l'URL con il conteggio massimo
    best_redirect = max(url_counts, key=url_counts.get)
    # Restituisce il numero massimo di algoritmi in accordo su un URL e l'URL stesso
    max_count = url_counts[best_redirect]
    return max_count, best_redirect
    
# Aggiornamento del dataframe per includere la colonna 'Agreement' e 'Best redirect'
def update_dataframe_with_agreement_and_best_redirect(df, selected_algorithms):
    # Applica la funzione count_agreement e crea due nuove colonne
    agreements_best_redirects = df.apply(lambda row: count_agreement(row, selected_algorithms), axis=1)
    df['Agreement'], df['Best redirect'] = zip(*agreements_best_redirects)

print("Check agreements")
# Aggiungi la colonna 'agreement'
final_mig_df['Agreement'] = final_mig_df.apply(lambda row: count_agreement(row, selected_algorithms), axis=1)   

# %%
# best redirect
# Chiamata della funzione per aggiornare il dataframe
update_dataframe_with_agreement_and_best_redirect(final_mig_df, selected_algorithms)

# %%
score_columns = [col for col in final_mig_df.columns if '_Score' in col]
score_columns

# %%
# Total score dei best redirect
def calculate_conditional_tscore(row):
    tscore = 0
    for col in score_columns:
        base_col = col.replace('_Score', '')
        if base_col in row and row[base_col] == row['Best redirect']:
            try:
                tscore += row[col]
            except KeyError:
                pass  # Ignora se la colonna non esiste
    return tscore

final_mig_df['Best redirect TotScore'] = final_mig_df.apply(calculate_conditional_tscore, axis=1)

# %%
# rimuovi colonna Cleaned
#final_mig_df.drop(columns=['Cleaned URLs'], inplace=True)
# Verifica se la colonna 'Cleaned URLs' esiste nel DataFrame prima di rimuoverla
if 'Cleaned URLs' in final_mig_df.columns:
    final_mig_df.drop(columns=['Cleaned URLs'], inplace=True)

# rinomina prima colonna
final_mig_df.columns.values[0] = '404 URL'
final_mig_df.head(4)  


# %%
# Ordina il DataFrame in base alla colonna 'Agreement'
final_mig_df = final_mig_df.sort_values(by='Best redirect TotScore', ascending=False)
final_mig_df

# %%
# crea foglio del mapping redirect pulito
# Specifica delle colonne da mantenere
columns_to_keep = [
    '404 URL',
    'status_code',
    'TotScore',
    'Agreement',
    'Best redirect',
    'Best redirect TotScore'
]

# Creazione del nuovo DataFrame con le colonne specificate
redirect = final_mig_df[columns_to_keep]

# Stampa per conferma
print("Nuovo DataFrame 'redirect' creato con successo!")
print(redirect.head())


# %%
# EXPORT

#output_folder_path = "./output"
output_folder_path = os.path.join(script_directory, "output")

# Creazione della cartella se non esiste
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

current_date_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
output_filename = f"{current_date_time}_redirect_map.xlsx"
output_path = os.path.join(output_folder_path, output_filename)


with pd.ExcelWriter(output_path) as writer:
    print("Saving redirect maps to Excel...")
    # Salva il primo DataFrame nel primo foglio
    final_mig_df.to_excel(writer, sheet_name='Mapping', index=False)
    print(f"Mappatura creata con successo nel foglio 'Mapping'!")

    # Salva il secondo DataFrame in un altro foglio
    redirect.to_excel(writer, sheet_name='Redirects', index=False)
    print(f"Redirect aggiunti con successo nel foglio 'Redirects'! Nome del file: {output_filename}")

