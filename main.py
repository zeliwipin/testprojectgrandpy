from flask import Flask, render_template, jsonify, request
import googlemaps
from flask_googlemaps import GoogleMaps
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import wikipedia


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processing', methods=['POST'])
def processing():
    newmessage = request.form['message_deux']

    if newmessage:


        # Je commence à m'occuper des cartes
        API_KEY = 'AIzaSyCFRB_ipsZztDSGoRwKOsnhXiWOKzi2YyU'

        map_client = googlemaps.Client(API_KEY)
        # Je specifie que les stopwords sont en français
        stopWords = set(stopwords.words("french"))

        # je tokenize la phrase, c'est à dire que je sépare une phrase
        # en de plus petits éléments
        wordTokens = word_tokenize(newmessage)

        # je crée une liste vide pour pouvoir stocker la phrase une fois que les stop words
        # auront étés enlevés de celle ci
        phrase_avec_filtre = []

        # Je crée une boucle avec la variable w pour repérer les éléments qu'il y  a dans
        # ma requête tokénisée qui ne sont pas dans les stop words en français
        # ce procédé permet de filtrer tous les stop words afin de recueuillir une requête
        # filtrée sous forme de liste

        for w in wordTokens:
            if w not in stopWords:
                phrase_avec_filtre.append(w)

        # je convertis cette liste alors tous juste créée en un élément string
        full_str = " ".join([str(elem) for elem in phrase_avec_filtre])

        # je commence à préparer mon opération de cherchage
        searchRequest = str(full_str)

        # j'initialise la librairie wikipedia pour des recherches en français
        wikipedia.set_lang("fr")

        input_user = str(searchRequest)

        response = map_client.find_place([input_user], input_type='textquery',
                                         fields=['formatted_address', 'photos', 'name', \
                                                 'place_id', 'geometry/location/lng', 'geometry/location/lat'])

        # placeid_response = response['candidates'][0]['place_id']
        pprint(response)

        # print(placeid_response)
        response_formatted_address = response['candidates'][0]['formatted_address']
        response_latitude = response['candidates'][0]['geometry']['location']['lat']
        response_longitude = response['candidates'][0]['geometry']['location']['lng']
        response_html_attributions = response['candidates'][0]['photos'][0]['html_attributions']

        print('new message is', newmessage)
        return jsonify({'retmessage': 'okokok', "latitude": response_latitude, "longitude": response_longitude})







if __name__ == '__main__':
    app.run(debug=True)