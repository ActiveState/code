/* Alumno: Guillermo López Leal 2IM1
 * 
 * Karatsuba algorith: fast multiplication of large integers.
 * 
 * Sorry for the comments in Spanish, but I think the code is very legible ;)
 */
#include <iostream>
#include <math .h>
 
using namespace std;
 
/*
 * Función Power(double x, int y)
 * calcula el número que resulta de calcular
 * x elevado a y. Se realiza por recursión.
 * Devuelve un tipo T, que se supone será
 * un número: int, double, float...
 *
 */
int Power(int x, int y) {
	if (y == 0)
		return (1);
	else if (y == 1)
		return(x);
	else
		return(x * Power(x, y-1));
}
 
/*
 * Función Digitos (T n, int &dig)
 * calcula el número de dígitos (dig) que tiene el número n, que
 * podría ser cualquier tipo de número: int, float, double...
 * Devuelve el número de dígitos (int).
 * He preferido cambiar la función para que devuelva el número
 * de dígitos en vez de mostrarlo por pantalla ya que en el algoritmo de
 * Karatsuba es necesario saber el número de dígitos de un número.
 *
 */
 
int Digitos (int n, int &dig) {
	if (n < 10)	return (dig+1);
	else {
		dig++;
		return(Digitos(n/10, dig));
	}
}
 
/*
 * Recibimos el número de dígitos que queremos ver como últimos
 * y el número, claro
 * Devolvemos el módulo de dividir el número entre la potencia de 10
 * elevado al número de dígitos:
 * e.g. sacar los últimos 3 dígitos de 3454567:
 * 3454567 % power(10, 3) -> 3454567 % 1000 -> 567
 *
 */
int ultimos(int digitos, int &numero) {
	return numero % Power(10, digitos);
}
 
/*
 * Al igual que con los últimos, devolvemos los n primeros "digitos" de "numero".
 * para ello usamos algo simple: dividimos el número entre la potencia de 10 elevado
 * al número de dígitos que queremos sacar.
 *
 */
int primeros(int digitos, int &numero) {
	return numero/Power(10, digitos);
}
 
/*
 * Algoritmo de Karatsuba. Multiplicación rápida de enteros largos
 * @param: int &u -> pasamos por referencia uno de los números a multiplicar.
 * @param: int &v -> pasamos por referencia el segundo número.
 */
int multiplica (int &u, int &v) {
	int dig1=0, dig2=0;
	//División en trozos iguales de los números. Tenemos que dividir según
	//el mayor de ambos entre 2: 3457689 -> 345 y 7689
	//							 3455 -> 0 y 3455
	int numDigitos = max(Digitos(u, dig1), Digitos(v, dig2));
	//Caso base, cuando se puede hacer una multiplicación directa (1 cifra)
	//En teoría si se lograba beneficio con números de más de 300 bits, se podría
	//sustituir ese 1 por 300.
	if (numDigitos < = 1) return u*v;
	//Número de dígitos redondeados HACIA ARRIBA para sacar la división.
	//e.g -> 9 dígitos de máximo -> sacamos los 5 últimos y después los 4 primeros
	//NO podemos sacar los 4.5 mayores y los 4.5 menores
	numDigitos = (numDigitos / 2) + (numDigitos % 2);
	//Vamos calculando los diferentes w, x, y, z…
	int w = primeros(numDigitos, u);
	int x = ultimos(numDigitos, u);
	int y = primeros(numDigitos, v);
	int z = ultimos(numDigitos, v);
	//Operaciones intermedias
	int p=multiplica(w, y);
	int q=multiplica(x, z);
	int wMasx = w + x;
	int zMasy = z + y;
	//Volvemos a llamar al algoritmo hasta que (como se ve arriba en el if) lleguemos al
	//caso base de n=numDigitos=1. Llamada recursiva
	int r=multiplica(wMasx, zMasy);
	// Salida final, usamos la función Power implementada arriba
	return Power(10, 2*numDigitos)*p+Power(10, numDigitos)*(r-p-q)+q;
}
 
//Funcion aleatoria para sacar números aleatorios menores que el parámetro x
int MiRandom(int x)
{
	int Numero=0;
	Numero=(rand()%x);
	return Numero;
}
 
int main () {
	//Inicializamos la semilla apuntando al tiempo
	srand(time(NULL));
	int numero=0;
	//Menor que 46340 -> raiz(max_int)=raiz(2147483647)...
	//Obviamente podría funcionar con más de 46340, pero podría producirse overflow.
	//Sólo ocurriría en el caso de que la semilla hiciera dos 46341 -> bum!!
	// Se podría poner hasta semilla 2147483647 si se tuviera la suerte que el random
	// fuera 1 y 2147483647
	//Además es que hemos limitado a "int", si hubiéramos puesto un valor más grande, como
	//unsigned long long int, tendríamos valores perfectos y muy grandes
	cout < < "Número máximo a multiplicar (menor que 46341, leer código fuente) :";
	cin >> numero;
	//Creamos dos enteros aleatorios máximo "numero"
	int num1 = MiRandom(numero);
	int num2 = MiRandom(numero);
	//Les mostramos
	cout < < "\nnum1=" << num1;
	cout << "\nnum2=" << num2;
	//Les multiplicamos!
	cout << "\nEl resultado del producto es: " << multiplica(num1, num2);
	return EXIT_SUCCESS;
}
