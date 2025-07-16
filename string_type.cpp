#include <iostream>

using namespace std;

int main(){

    string title = "Mr. ";
    string name = ("John ");
    string end(10, '@');
    /*
    Strings são objetos que representam sequências de caracteres.
    Eles podem ser manipulados de várias maneiras, como concatenação, comparação e busca.
    A classe string é parte da biblioteca padrão do C++ e oferece uma interface rica para trabalhar
    */

    /*
    A partir do momento em que temos uma classe, uma classe ela é mais rica em termos de funcionalidade 
    do que um tipo primitivo, um tipo primitivo ele é m tipo básico, a única coisa que se
    pode fazer com um tipo primitivo é armazenar um valor, já uma classe ela tem métodos, atributos
    */

    cout << title << name << end<<endl;
    return 0;
}