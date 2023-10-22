---producer.py
    Dupa initializarea din constructor, cand se porneste threadul, se 
intra in metoda run. Aici inregistram producerul (threadul), care primeste un id. 
Intr-o bucla infinita, pentru fiecare produs din lista
producer-ului, adaugam in lista sa de available_products cantitatea
de produse oferita. Daca este plina coada sa de produse, se asteapta
cu sleep. Altfel, se asteapta dupa adaugarea fiecarui produs. Daca
toti consumerii au apelat metoda place_order, atunci vor fi opriti
toti producerii.


---consumer.py
    In metoda run, cream un cart nou. Pentru fiecare operatie de add 
si remove din lista consumerului, adaugam/stergem din cart cantitatea
dorita. Asteptam cu sleep cat timp nu este disponibil in available_products 
produsul pe care dorim sa il adaugam. Apelam metoda place_order si 
afisam fiecare produs din cart.


---marketplace.py
    In constructor initializam variabilele, lock-ul pentru a permite 
intrarea unui singur thread intr-o zona critica si fisierul de logging. 
In register_producers,  incrementam numarul de producers, pe care il si returnam 
ca string deoarece acesta este id-ul fiecarui producator. Am folosit in implementare 
2 dictionare (unul care are cheia producer_id si valoarea numarul de produse adaugate 
de producator - pentru a se compara cu lungimea maxima a cozii), (iar al doilea dictionar 
are cheia product si valoarea id-ul producatorului care l-a produs - ca sa gasesc 
repede daca mai exista obiect de tip product disponibil in marketplace). In publish, 
daca producatorul nu a mai adaugat niciun produs in available_products_by_type, atunci 
initializam intrarea sa din dictionar. La fel si pentru no_of_products_per_producer. Daca 
no_of_products_per_producer[producer_id] e egal cu maximul cozii, atunci returnam False si producatorul
trebuie sa astepte sa se elibereze lista (practic sa consume cineva produse de la el). Altfel, 
adaugam id-ul producatorului in dictionar la cheia product. In new_cart este acelasi mecanism 
ca la register_producer,  incrementam si returnam id-ul. In add_to_cart, verificam daca exista 
product in dictionar, apoi adaugam in cart-ul cumparatorului, scadem numarul de produse disponibile 
ale producerului (primul dictionar) si eliminam si din al doilea dictionar id-ul producerului de 
la cheia product. In remove_from_cart, stergem din cart produsul si il punem inapoi in available 
products pentru a fi achizitionat de alti consumeri. La place_order, daca nu mai exista elementul 
0 in lista de consumeri (toti au apelat place_order), atunci oprim si producerii. Returnam lista 
de produse din cart.
    La TestMarketplace, instantiem in setUp un marketplace, apoi
testam fiecare metoda din clasa Marketplace. 