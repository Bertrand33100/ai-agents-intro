# Topic

Python decorators

## Simple Explanation

Un décorateur est une fonction qui permet de modifier la comportement d'une autre fonction. Il peut être utilisé pour ajouter des fonctionnalités à une fonction sans modifier sa source code.

## Key Concepts

Un décorateur est une fonction qui reçoit une fonction en argument et retourne une nouvelle fonction. Il est utilisé pour ajouter des fonctionnalités à une fonction existante, comme la mise en place de logging, de validation ou de métriques.

## Example

```python
def decorator_function(func):
    def wrapper():
        result = func()
        return result
    return wrapper

@decorator_function
def say_hello():
    return "Bonjour"

result = say_hello()
print(result)
```

**Explication :**  
1. La fonction `decorator_function` reçoit une fonction `func` en argument.
2. Elle définit une fonction `wrapper` qui appelle `func()` et retourne son résultat.
3. Elle retourne `wrapper`.
4. La fonction `say_hello` est décorée par `decorator_function`, ce qui fait que `say_hello()` appelle `wrapper`.
5. Le résultat final est `"Bonjour"`, qui est affiché à la fin.

## Practice Exercise

### Énoncé  
Créez un décorateur qui affiche un message d'information avant d'exécuter une fonction donnée. Utilisez ce décorateur pour décorer une fonction qui calcule la somme de deux nombres et affiche le résultat.

### Entrée attendue  
Une fonction nommée `add_numbers` qui calcule la somme de deux nombres entiers, par exemple :  
```python
def add_numbers(a, b):
    return a + b
```

### Sortie attendue  
Le résultat de l'appel de `add_numbers(5, 3)` est `8`, et une ligne de texte `"Calcul de somme : 8"` est affichée avant que la fonction soit exécutée.

### Indices  
- Utilisez la fonction `functools.wraps` pour conserver les informations de la fonction originale.  
- Le décorateur doit recevoir la fonction à décorer en argument.  
- Le décorateur doit retourner une fonction wrapper qui exécute la fonction cible.

## Common Mistakes

- **Erreurs de syntaxe :** Faire une erreur dans la définition du décorateur ou du wrapper.
- **Appels incorrects :** Appeler la fonction décorée depuis sa propre définition.
- **Redéfinition de la fonction originale :** Ne pas redéfinir la fonction originale avant ou après son application.
- **Ignorer le `functools.wraps` :** Ne pas utiliser `functools.wraps` pour conserver les informations de la fonction originale.

## Review Comments

### Informations manquantes  
Aucune.

### Explications ambiguës  
Aucune.

### Suggestions d'amélioration  
1. **Ajouter une explication sur le rôle exact de `functools.wraps`** : Il est recommandé de mentionner que `functools.wraps` permet de conserver les métadonnées de la fonction cible (comme le nom, la description, les paramètres) pour éviter des conflits lors de l'application du décorateur.
2. **Ajouter une explication sur le rôle de `@decorator_function`** : Il est utile de préciser que le décorateur est appliqué avec `@` et que cela permet de modifier le comportement de la fonction cible.

### Recommandation finale  
REVISION REQUIRED  
Le brouillon est satisfaisant, mais il manque une explication claire sur le rôle de `functools.wraps` et il serait utile de préciser comment le décorateur est appliqué.

## Final Summary

Un décorateur est une fonction qui permet de modifier la comportement d'une autre fonction. Il est utilisé pour ajouter des fonctionnalités sans modifier la source code de la fonction. Il est défini en premier, puis appliqué à la fonction cible, et il retourne une nouvelle fonction qui appelle la fonction cible.
