# Anmerkungen
## Datenbank
Mein erster Impuls war es eine Datenbank wie z.B. PostgreSQL zu verwenden. Da in meinen Augen aber der Fokus der Aufgabenstellung auf der Implementierung der REST-API liegt, habe ich mich dazu entschieden eine einfaches Dictionary zu verwenden. Dieses ist natürlich nicht persistent, aber für die Aufgabe ausreichend.

## Authentifizierung
Ich fand die Aufgabestellung hier ein wenig ungenau. Für mich gab es zwei Möglichkeiten:
1. Über den /login Endpoint wird ein Secret generiert, was genutzt wird um sensible Daten zu verschlüsseln. So müssen Client und Server bei jeder Anfrage verschlüsseln und entschlüsseln. Das Secret wird in der Datenbank gespeichert und kann so bei jeder Anfrage abgefragt werden.
2. Über den /login Endpoint wird ein Token generiert, welches bei jeder Anfrage mitgeschickt wird. Der Server kann so das Token überprüfen und die Anfrage entweder akzeptieren oder ablehnen.

Ich habe mich für die zweite Variante entschieden, da dies für mich leichter zu testen war. Ich habe mit JWT Tokens noch nicht gearbeitet und war mir nicht sicher, ob ich das in der Zeit schaffe. Ich habe mich für die Bibliothek [PyJWT](https://pypi.org/project/PyJWT/) entschieden, da diese sehr einfach zu verwenden ist.

## Tests
Aufgrund der Zeit habe ich mich dazu entschieden nur die wichtigsten Tests zu implementieren. In der Realität würde ich natürlich alle möglichen Testfälle abdecken inklusive aller Parameter und die Testabdeckung überprüfen. Auch die Integrationstests mit einer Datenbank und einem Frontend würde ich noch hinzufügen.