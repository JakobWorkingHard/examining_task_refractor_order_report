1. Input/output ligger i samma fil 
 Blir annars svårt att läsa av koden, blir rörigt, 
 flytta till io.py

2. a) Validate ligger även den i samma fil, kan flyttas till en validate.py fil exempelvis, så det blir enklare att felsöka, enklare att få en överblick över koden, samt följa Separation of Concerns. 
b) raise exception är extremt vag, behöver ändras till mer specifik felkod, annars kastar den fel för vadsom.

3. Behöver ha en requirement.txt fil så man enkelt kan importera nödvändiga paket

4. Finns ingen readme.md i projektet som beskriver vad detta ens är och vad man får ut.

5. TRANSFORM: Lägg i egen fil
a) i transformeringen och att göra om data quantity till fillna(1) känns helt weird, för först gör man bara om alla värden pandas ej strikt kan göra om från sträng till siffra till NaN, och sedan lägger man en 1a på den, helt utan datatvätt. Det saknas med andra ord en ordentlig datatvätt här, så det behöver vi lägga till först
b) Behöver vid nogrannare granskning lägga till datatvätt på samtliga kolumner istället för denna enkla versionen där man bara struntar i allt. Om vi nu gärna vill ha ett automatiskt flöde helt utan egen granskning och städning av datan så kan vi ha en flaggning där vår funktion flaggar ifall det är för många NaN värden, men så kan vi fylla i NaN värden på detta sätt som redan står i koden, så IFALL det blivit för många NaN värden så får vi iaf veta det istället för detta sätt som är nu.
c) Lägg till datetime på order_date i processing
d) Sätta to_csv i io fil

e) Finns ingen loggning när det gäller ens output, vilket jag tycker bör finnas.

f) Hela kodblocket har en try except, vilket gör att när koden kraschar så säger den bara att något gick fel, och vi står här helt oförstående utan att förstå vad som gick fel.

Plan: src -> Skapa klass i reporting.py och funktioner i de övriga filerna, där vi har en io.py, en processing.py, en validation.py och en reporting.py som orkestrerar allt. Även en config.py där man kan tweaka ens inställnignar. Lägger även till test funktioner i en egen test fil, samt en pyproject.toml istället för en requirement.txt, och även en logger samt en logger.py i src som skickar loggningsinfo till loggfil, lägger till logg-info i io.py och validation, samt i reporting, och även i processing men ha där re-raise så koden både kraschar hårt men även loggar.



**Checklista - vad som är gjort**
- Lagt in threshhold för NaN värden vi ska flagga för samt path för output och input i config.toml, där config.py hämtar info från config.toml
- io.py hämtar path från config.py och skapar funktion därefter, som sedan importeras i main.py som blir själva "huvudfilen" samt order_report.py för att testa om samma funktionalitet fungerar osv osv blabblabla
- Skapat tester för config.py som testar happy-test, edge-case och error
- Skapat validate.py , lagt till så vi först kollar om alla våra columner finns med i vår df, sedan kollar om vi har för många NaN värden (och då gör jag först om mitt column-innehåll så jag får NaN värden där det inte stämmer överens (liten enkel datatvätt)). 
Räknar NaN-värden och markerar ifall det överstiger threshhold satt av användaren i config.toml.



Note to self:
1. Behöver lägga till error logging för validate funktioner
2. Behöver lägga till tester för validate
