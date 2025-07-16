#include <iostream>

using namespace std;

int main(){

    bool isadmin = 1;
    /*
    qualquer valor diferente de false ou zero atribuido ao tipo bool 
    será considerado como true, valor 1, caso contrário,
    será considerado como false, valor 0.
    */
   char symvol = '#';
   char simbol('#'); // outra forma de declarar um char

   /*
   o tipo char é usado apenas para armazenar um único caractere, 
   ele é um tipo primitivo, ou seja, ele não tem métodos ou atributos,
   */

   int age;
   
   /*
   Uma coisa é definir o tipo, outra coisa é definir alguns modificadores.
   Os modificadores são usados para alterar o comportamento do tipo primitivo.
   Ex: short int, long int, long long int, unsigned int, signed int.
   */

   //Modificadores do tipo float:

   float pi = 3.14;
   const double pi1 = 3.141592653589; // constante de ponto flutuante de precisão dupla
   long double pi2 = 3.14159265358979323846L; // constante de ponto flutuante de precisão estendida
   const float pi3 = 3.14159265358979323846F; // constante de ponto flutuante de precisão simples

   cout << sizeof(isadmin) <<" bytes"<< endl; // tamanho do tipo bool
    cout << sizeof(symvol) <<" bytes"<< endl; // tamanho do tipo char
    cout << sizeof(age) <<" bytes"<< endl; // tamanho do tipo int
    cout << sizeof(pi) <<" bytes"<< endl; // tamanho do tipo float
    cout << sizeof(pi2) <<" bytes"<< endl; // tamanho do tipo double
    cout << sizeof(pi3) <<" bytes"<< endl; // tamanho do tipo float constante
    cout << sizeof(long double) <<" bytes"<< endl; // tamanho do tipo long double
   return 0;
}