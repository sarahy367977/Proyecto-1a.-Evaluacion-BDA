-- Insertar usuarios
INSERT INTO users (id, name, email) VALUES (1, 'Ana García', 'ana.garcia@email.com');
INSERT INTO users (id, name, email) VALUES (2, 'Carlos López', 'carlos.lopez@email.com');
INSERT INTO users (id, name, email) VALUES (3, 'María Rodríguez', 'maria.rodriguez@email.com');
INSERT INTO users (id, name, email) VALUES (4, 'Pedro Martínez', 'pedro.martinez@email.com');

--Insertar tags
INSERT INTO tags (id, name, url) VALUES (1, 'Viajes', 'viajes');
INSERT INTO tags (id, name, url) VALUES (2, 'Cocina', 'cocina');
INSERT INTO tags (id, name, url) VALUES (3, 'Deportes', 'deportes');
INSERT INTO tags (id, name, url) VALUES (4, 'Salud', 'salud');
INSERT INTO tags (id, name, url) VALUES (5, 'Música', 'musica');

-- Insertar categorías
INSERT INTO categories (id, name, url) VALUES (1, 'Viajes', 'viajes');
INSERT INTO categories (id, name, url) VALUES (2, 'Cocina', 'cocina');
INSERT INTO categories (id, name, url) VALUES (3, 'Deportes', 'deportes');
INSERT INTO categories (id, name, url) VALUES (4, 'Salud', 'salud');
INSERT INTO categories (id, name, url) VALUES (5, 'Entretenimiento', 'entretenimiento');

-- Insertar artículos
INSERT INTO articles (id, title, article_date, text, user_id) VALUES (
    1, 
    'Los 10 Mejores Destinos para Visitar en 2024', 
    DATE '2024-01-15', 
    'Descubre los lugares más impresionantes para tus próximas vacaciones. Desde playas paradisíacas hasta ciudades llenas de historia y cultura. Japón, Italia y Costa Rica se encuentran entre los destinos más populares este año.',
    1
);

INSERT INTO articles (id, title, article_date, text, user_id) VALUES (
    2, 
    'Recetas Saludables para el Desayuno', 
    DATE '2024-01-20', 
    'Comienza tu día con energía con estas deliciosas y nutritivas recetas de desayuno. Fáciles de preparar y llenas de sabor. Incluye opciones como avena con frutas, smoothies nutritivos y tostadas integrales.',
    2
);

INSERT INTO articles (id, title, article_date, text, user_id) VALUES (
    3, 
    'Beneficios del Ejercicio Diario', 
    DATE '2024-02-01', 
    'La actividad física regular no solo mejora tu salud física, sino también tu bienestar mental. Conoce todos sus beneficios, incluyendo mejor salud cardiovascular, mayor energía y reducción del estrés.',
    3
);

INSERT INTO articles (id, title, article_date, text, user_id) VALUES (
    4, 
    'Consejos para una Alimentación Balanceada', 
    DATE '2024-02-10', 
    'Aprende a combinar los diferentes grupos alimenticios para mantener una dieta equilibrada y saludable. Incluye recomendaciones sobre porciones, horarios y combinaciones ideales de alimentos.',
    1
);

INSERT INTO articles (id, title, article_date, text, user_id) VALUES (
    5, 
    'Cómo Mantener una Rutina de Ejercicios', 
    DATE '2024-02-15', 
    'La constancia es clave en cualquier programa de ejercicios. Te damos tips para mantener la motivación, establecer metas realistas y crear hábitos duraderos de actividad física.',
    4
);

-- Insertar comentarios
INSERT INTO comments (id, article_id, name, text, comment_date) VALUES (
    1, 1, 'Laura Méndez', '¡Excelentes recomendaciones! Ya estoy planeando mi próximo viaje a uno de estos destinos.', DATE '2024-01-16'
);

INSERT INTO comments (id, article_id, name, text, comment_date) VALUES (
    2, 1, 'Roberto Silva', 'Me encantó la lista, especialmente la recomendación de Japón. Es un destino increíble.', DATE '2024-01-17'
);

INSERT INTO comments (id, article_id, name, text, comment_date) VALUES (
    3, 2, 'Elena Torres', 'Probé la receta de avena con frutas y está deliciosa. ¡Gracias por compartir!', DATE '2024-01-22'
);

INSERT INTO comments (id, article_id, name, text, comment_date) VALUES (
    4, 3, 'Dr. Sánchez', 'Muy buen artículo. Es importante recordar los beneficios del ejercicio regular para la salud.', DATE '2024-02-02'
);

INSERT INTO comments (id, article_id, name, text, comment_date) VALUES (
    5, 4, 'Carmen Ruiz', 'Los consejos sobre porciones fueron muy útiles. Estoy mejorando mis hábitos alimenticios.', DATE '2024-02-11'
);

INSERT INTO comments (id, article_id, name, text, comment_date) VALUES (
    6, 5, 'Javier López', 'Justo lo que necesitaba para mantener mi rutina de ejercicios. Muy motivador.', DATE '2024-02-16'
);

-- 6. Relacionar artículos con tags
INSERT INTO article_tags (article_id, tag_id) VALUES (1, 1);
INSERT INTO article_tags (article_id, tag_id) VALUES (2, 2);
INSERT INTO article_tags (article_id, tag_id) VALUES (2, 4);
INSERT INTO article_tags (article_id, tag_id) VALUES (3, 3);
INSERT INTO article_tags (article_id, tag_id) VALUES (3, 4);
INSERT INTO article_tags (article_id, tag_id) VALUES (4, 4);
INSERT INTO article_tags (article_id, tag_id) VALUES (4, 2);
INSERT INTO article_tags (article_id, tag_id) VALUES (5, 3);
INSERT INTO article_tags (article_id, tag_id) VALUES (5, 4);

INSERT INTO article_categories (article_id, category_id) VALUES (1, 1);
INSERT INTO article_categories (article_id, category_id) VALUES (2, 2);
INSERT INTO article_categories (article_id, category_id) VALUES (2, 4);
INSERT INTO article_categories (article_id, category_id) VALUES (3, 3);
INSERT INTO article_categories (article_id, category_id) VALUES (3, 4);
INSERT INTO article_categories (article_id, category_id) VALUES (4, 4);
INSERT INTO article_categories (article_id, category_id) VALUES (4, 2);
INSERT INTO article_categories (article_id, category_id) VALUES (5, 3);
INSERT INTO article_categories (article_id, category_id) VALUES (5, 4);

COMMIT;



select * from users;
