# phython-projects
## <a href="fehler.py" id="fehler">fehler.py</a>
Funktionen zur Berechnung von Messunsicherheiten mit der Gauß'schen Fehlerfortpflanzungsformel und der Methode der oberen und unteren Grenze

## <a href="tv2.ipynb">tv2.ipynb</a>
Nutzung der Funktionen aus <a href="#fehler">fehler.py</a> zur Berechnung der Unsicherheiten bei der Bestimmung von Wärmekapazitäten

## <a href="tv5.ipynb">tv5.ipynb</a>
Bestimmung und Plotten einer optimalen Gerade durch <a href="tv5_messwerte.txt">Messwerte</a> mit numpy, scipy und matplotlib

## <a href="matrix.py">matrix.py</a>
Definition einer Klasse Matrix(), die Addition, Subtraktion und (Skalar-) Multiplikation von beliebigen Matrizen ermöglicht

## <a href="spotify.py">spotify.py</a>
Nutzung der <a href="https://developer.spotify.com/documentation/web-api/">Spotify Web API</a> in Verbindung mit dem Python-Modul 'Requests'. <br><br> Funktionen:
<ul>
    <li>
        Automatisches Erneuern des Access-Tokens für die Spotify-API
    </li>
    <li>
        Erstellen von JSON-Backups von Playlists und den gespeicherten Songs in folgender Form:
    </li><br>

~~~json 
{
    "description": "",
    "id": "0TTAWykuwNdKY6R8bZxqHo",
    "name": "idk",
    "owner": "philipobichu",
    "tracks_no": 2,
    "tracks": [
        {
            "added_at": "2021-08-14T18:31:26Z",
            "added_by": "philipobichu",
            "uri": "spotify:track:0gQ12zQF2M5yLpUqnPb6hI",
            "name": "Friday Morning",
            "album": "Con Todo El Mundo",
            "artists": [
                "Khruangbin"
            ]
        },
        {
            "added_at": "2022-05-03T14:45:02Z",
            "added_by": "philipobichu",
            "uri": "spotify:track:4NGG9OBS86xX09ciDdpMN1",
            "name": "Midnite Oil - Sparkzzz",
            "album": "Idiom",
            "artists": [
                "Joe Armon-Jones",
                "Maxwell Owin"
            ]
        }
    ]
}
~~~

<br>
<li>
    Kopieren von Playlists von anderen Nutzern (Erstellung einer eigenen Playlist mit allen Songs aus der zu kopierenden Playlist)
</li>

</ul>


<ul>
   
</ul>

