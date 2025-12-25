
---

# 📚 **BookVerse — Comunidad de Lectores y Reseñas**

Bienvenido a **BookVerse**, una API construida en Django/DRF diseñada para gestionar libros, autores, usuarios y reseñas.
Incluye lógica personalizada mediante **Managers**, **métodos de modelo**, **serializers específicos** y **APIViews** con endpoints flexibles.

---

## 🎯 **Descripción del Proyecto**

**BookVerse** permite a los usuarios:

* Registrar libros y autores.
* Asociar libros con autores.
* Crear reseñas entre usuarios y libros.
* Consultar promedios de calificaciones.
* Realizar filtrados avanzados con managers personalizados.

Cada entidad posee su propia lógica interna y consultas especializadas para un manejo eficiente de la información.

---

## 🧱 **Objetivos principales**

✔ Registrar libros y autores
✔ Asociar libros con sus autores
✔ Registrar reseñas de usuarios
✔ Calcular promedios de calificaciones
✔ Implementar managers personalizados
✔ Crear métodos de modelo y serializers a medida
✔ Usar APIViews para endpoints con lógica dedicada
✔ Aplicar buenas prácticas con `class Meta` (orden, restricciones, etc.)

---

## 🗂️ **Modelo de Datos**

### 1️⃣ **Author**

Representa un autor dentro del sistema.

| Campo       | Tipo          | Descripción                    |
| ----------- | ------------- | ------------------------------ |
| id          | AutoField     | Identificador único            |
| name        | CharField     | Nombre completo                |
| nationality | CharField     | Nacionalidad                   |
| birth_date  | DateField     | Fecha de nacimiento (opcional) |
| created_at  | DateTimeField | Fecha de creación del registro |

🔗 **Relaciones:**

* Un autor tiene muchos libros.

🧠 **Lógica esperada:**

* `AuthorManager.with_min_books(count)` → autores con al menos *count* libros.
* `total_books()` → retorna la cantidad de libros del autor.
* **Meta:** ordenado por `name`.

---

### 2️⃣ **Book**

Representa un libro registrado.

| Campo            | Tipo                                     | Descripción        |
| ---------------- | ---------------------------------------- | ------------------ |
| id               | AutoField                                | Identificador      |
| title            | CharField                                | Título del libro   |
| author           | ForeignKey(Author, related_name="books") | Autor del libro    |
| publication_year | IntegerField                             | Año de publicación |
| genre            | CharField                                | Género literario   |
| created_at       | DateTimeField                            | Fecha de creación  |

🔗 **Relaciones:**

* Un libro tiene un autor.
* Un libro puede tener muchas reseñas.

🧠 **Lógica esperada:**

* `BookManager.filter_by_genre(genre)` → libros por género.
* `BookManager.recent_books(years=5)` → libros recientes.
* `average_rating()` → promedio de calificaciones del libro.
* **Meta:** restricción única `(title, author)`.

---

### 3️⃣ **UserProfile**

Representa un usuario lector.

| Campo     | Tipo          | Descripción                |
| --------- | ------------- | -------------------------- |
| id        | AutoField     | Identificador              |
| username  | CharField     | Nombre de usuario (único)  |
| email     | EmailField    | Correo electrónico (único) |
| joined_at | DateTimeField | Fecha de registro          |

🔗 **Relaciones:**

* Un usuario puede escribir muchas reseñas.

🧠 **Lógica esperada:**

* `UserProfileManager.active_since(year)` → usuarios activos desde cierto año.
* `total_reviews()` → cantidad de reseñas del usuario.
* **Meta:** ordenado por `joined_at` (descendente).

---

### 4️⃣ **Review**

Representa la reseña creada por un usuario sobre un libro.

| Campo      | Tipo                                            | Descripción       |
| ---------- | ----------------------------------------------- | ----------------- |
| id         | AutoField                                       | Identificador     |
| user       | ForeignKey(UserProfile, related_name="reviews") | Usuario           |
| book       | ForeignKey(Book, related_name="reviews")        | Libro reseñado    |
| rating     | IntegerField                                    | Puntuación (1–5)  |
| comment    | TextField                                       | Comentario        |
| created_at | DateTimeField                                   | Fecha de creación |

🔗 **Relaciones:**

* Un usuario puede reseñar varios libros.
* Pero solo **una reseña por libro**.

🧠 **Lógica esperada:**

* `ReviewManager.by_book(book_id)` → reseñas de un libro.
* `ReviewManager.by_user(user_id)` → reseñas de un usuario.
* `short_comment()` → primeros 50 caracteres del comentario.
* **Meta:** restricción única `(user, book)`.
<!--  -->
---

## ⚙️ **Endpoints sugeridos**

| Método | URL                               | Descripción             |
| ------ | --------------------------------- | ----------------------- |
| GET    | `/api/books/`                     | Listar libros           |
| GET    | `/api/books/<id>/`                | Ver detalle de un libro |
| GET    | `/api/books/<id>/average-rating/` | Promedio del libro      |
| GET    | `/api/authors/`                   | Listar autores          |
| GET    | `/api/authors/<id>/books/`        | Libros de un autor      |
| POST   | `/api/reviews/`                   | Crear reseña            |
| GET    | `/api/users/<id>/reviews/`        | Reseñas de un usuario   |

---

## 💡 **Desafíos opcionales**

* Implementar filtros sin usar `django-filters` (género, nacionalidad, fechas, etc.).
* Crear un manager global de métricas (ej.: libros mejor calificados).
* Construir un serializer combinando datos (ej.: autor + promedio global).
* Validar que un usuario solo deje una reseña por libro (en el serializer).
* Añadir endpoints personalizados con APIView (ej.: `/api/books/top-rated/`).

---