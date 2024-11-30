import pytest
import requests

URL="http://108.143.193.45:8080/api/v1/students/"

# Metoda GET
def is_student_in_database(id):
    response=requests.get(f"{URL}{id}")
    if response.status_code==200:
        return True
    else:
        return False

# Metoda POST
def create_student(firstName, lastName, email, age):
    body={
    "firstName":firstName,
    "lastName": lastName,
    "email": email,
    "age": age,
    }
    response=requests.post(URL,json=body)
    return response.json()

# Metoda DELETE
def delete_student(id):
    response=requests.delete(f"{URL}{id}")
    return response.text

# GET - korektní vstup
@pytest.mark.parametrize(
    "name, lastname, email, age",
    [
        ("Monika","KUBAŘOVÁ","mc@gmail.com",35),
        ("Ondřej","NOVÁK","on@gmail.com",88),
        ],
)
def test_get_correct_input(name,lastname,email,age):
    student=create_student(name,lastname,email,age)
    response=requests.get(f"{URL}{student["id"]}")
    delete_student(student["id"])
    assert response.status_code==200
    assert student["firstName"]==name
    assert student["lastName"]==lastname
    assert student["email"]==email
    assert student["age"]==age


# GET - nekorektní vstup - neexistující id
# Odhalení bugu - server vrací status kód 500 místo očekávaného 404
@pytest.mark.parametrize(
    "id",
    [0,-500,100000,300],
)
def test_get_incorrect_input(id):
    response=requests.get(f"{URL}{id}")
    assert response.status_code==404

# POST - korektní, duplicitní i nekorektní vstupy
# Odhalení bugu - server vrací chybné status kód oproti očekávaným status kódům
@pytest.mark.parametrize(
    "name,lastname,email,age,expected_code",
    [("Alžběta","Zedníčková","az@seznam.cz",55,201), #validní vstup
     ("Alžběta","Zedníčková","az@seznam.cz",55,409), #duplicita
     ("Marek","Kohout","",15,400), #chybějící parametr
     ("23567","Zedníčková", "az@centrum.cz",42,400), #name = čísla ve stringu
     (123456,"Zedníčková","az@gmail.com",82,400),#name - type int
     ("?/*!","Ostrý","az@email.cz",55,400), #name - speciální znaky
     ("rOmAnA","Přecechtělová","rp@gmail.com",88,400), #name - střídání velkých a malých písmen
     ("Lorem ipsum dolor sit amet, consectetur adipiscing elit.","Sametová","ls@gmail.com",48,400), #name - příliš dlouhé neexistující jméno
     ("Barbora","23567","bc@gmail.com",45,400), #lastname - čísla ve stringu
     ("Barbora",123,"a@gmail.com",65,400), #lastname - type int
     ("Barbora","?/*!","b@gmail.com",45,400), # lastname - speciální znaky
     ("Emil","sTuDnIčKa","es@gmail.com",10,400), #lastname - střídání velkých a malých písmen
     ("Lolek","Lorem ipsum dolor sit amet, consectetur adipiscing elit.","ls@gmail.com",45,400), # lastname - příliš dlouhé neexistující příjmení
     ("Emil","Okurka","123456789",30,400), #email - string
     ("Ondřej","Listonoš","#@%^%#$@#$@#.com",55,400), #email - speciální znaky
     ("Laura","Studená","email@example@example.com",45,400), #email - dvojitý @
     ("Roman","Zima","email@example.web",56,400), #email - neexistující přípona
     ("Denisa","Muchová","dm@seznam.cz","abcd",400), #age - type string místo int
     ("Aneta","Malá","am@seznam.cz",123456,400), #age- příliš velký int
     ("Adéla","Velká","av@seznam.cz",-5,400), #age- záporný int
     ("Petra","Puntíková","pp@seznam.cz",55.5,400), #age- float
    ],    
)
def test_post(name,lastname,email,age,expected_code):
     response=requests.post(URL,json={"firstName":name, "lastName":lastname,"email":email,"age":age})
     code=response.status_code
     body=response.text
     db_student={}
     assert code==expected_code


     if code//100 == 2:
         body=response.json()
         db_student=requests.get(f"{URL}{body['id']}").json()
         delete_student(body["id"])
     
     if expected_code//100==2:
         assert db_student["firstName"]==name
         assert db_student["lastName"]==lastname
         assert db_student["email"]==email
         assert db_student["age"]==age


# DELETE - korektnÍ i nekorektní vstupy
# Odhalení bugu - server vrací chybné status kódy oproti očekávaným status kódům
@pytest.mark.parametrize(
    "name,lastname,email,age",
    [
        ("Eleanor","STUDENÁ","es@gmail.com",77),
        ("Emil","HOUŽVIČKA","eh@gamil.com",55),
    ]
)
def test_delete_correct_input(name,lastname,email,age):
    student=create_student(name,lastname,email,age)
    response=requests.delete(f"{URL}{student['id']}")
    assert response.status_code==204
    assert is_student_in_database==False

def test_delete_incorrect_input():
    student=create_student("Josef","Malina","jm@gmail.com",45)
    delete_student(student["id"])
    response=requests.delete(f"{URL}{student['id']}")
    assert response.status_code==404

@pytest.mark.parametrize(
    "id", [0,-45,-9856]
    )
def test_delete_negative_id(id):
    response=requests.delete(f"{URL}{id}")
    assert response.status_code==404









    
