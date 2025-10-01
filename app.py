from flask import Flask, jsonify, request
from flask_cors import CORS
import oracledb

app = Flask(__name__)
CORS(app)

def get_connection():
    try:
        dsn = oracledb.makedsn("localhost", 1521, service_name="xepdb1")
        conn = oracledb.connect(user="BLOG1", password="blog1", dsn=dsn)
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM DUAL")
            result = cur.fetchone()
            conn.close()
            return jsonify({"success": True, "message": "✅ Conexión a BD exitosa"})
        else:
            return jsonify({"success": False, "error": "❌ No se pudo conectar a la BD"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Usuarios
@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        conn = get_connection()
        cur = conn.cursor()
        usuarios = cur.execute("SELECT id, name, email FROM users ORDER BY name").fetchall()
        conn.close()
        
        usuarios_list = [{"id": u[0], "nombre": u[1], "email": u[2]} for u in usuarios]
        
        return jsonify({"success": True, "usuarios": usuarios_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    try:
        data = request.json
        nombre = data.get('nombre')
        email = data.get('email')
        
        if not nombre or not email:
            return jsonify({"success": False, "error": "Nombre y email son requeridos"}), 400
        
        conn = get_connection()
        cur = conn.cursor()
        user_id = cur.callfunc("register_user", int, [nombre, email])
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "mensaje": "Usuario creado exitosamente", "id": user_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# articulos
@app.route('/api/articulos', methods=['GET'])
def obtener_articulos():
    try:
        conn = get_connection()
        cur = conn.cursor()
        articulos_cursor = cur.callfunc("get_articles", oracledb.CURSOR, [])
        articulos = list(articulos_cursor)
        
        articulos_list = []
        for art in articulos:
            # Obtener tags 
            tags = cur.execute("""
                SELECT t.id, t.name, t.url 
                FROM tags t
                JOIN article_tags at ON t.id = at.tag_id
                WHERE at.article_id = :articulo_id
            """, articulo_id=art[0]).fetchall()
            
            # Obtener categorías del artículo
            categorias = cur.execute("""
                SELECT c.id, c.name, c.url 
                FROM categories c
                JOIN article_categories ac ON c.id = ac.category_id
                WHERE ac.article_id = :articulo_id
            """, articulo_id=art[0]).fetchall()
            
            # Contar comentarios
            count_comentarios = cur.callfunc("count_comments", int, [art[0]])
            
            articulos_list.append({
                "id": art[0],
                "titulo": art[1],
                "fecha": art[2].strftime('%d/%m/%Y') if art[2] else None,
                "autor": art[3],
                "tags": [{"id": t[0], "nombre": t[1], "url": t[2]} for t in tags],
                "categorias": [{"id": c[0], "nombre": c[1], "url": c[2]} for c in categorias],
                "total_comentarios": count_comentarios
            })
        
        conn.close()
        return jsonify({"success": True, "articulos": articulos_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/articulos', methods=['POST'])
def crear_articulo():
    try:
        data = request.json
        titulo = data.get('titulo')
        contenido = data.get('contenido')
        usuario_id = data.get('usuario_id', 1) 
        tags_ids = data.get('tags_ids', [])        
        categories_ids = data.get('categories_ids', []) 
        
        if not titulo or not contenido:
            return jsonify({"success": False, "error": "Título y contenido son requeridos"}), 400
        
        conn = get_connection()
        cur = conn.cursor()
        
        art_id = cur.callfunc("add_article", int, [titulo, contenido, usuario_id])

        for tag_id in tags_ids:
            cur.callproc("add_tag_to_article", [art_id, tag_id])

        for cat_id in categories_ids:
            cur.callproc("add_category_to_article", [art_id, cat_id])
            
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "mensaje": "Artículo creado y asociado exitosamente", "id": art_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

#comentarios
@app.route('/api/comentarios', methods=['GET'])
def obtener_comentarios():
    try:
        conn = get_connection()
        cur = conn.cursor()
        comentarios = cur.execute("""
            SELECT c.id, c.text, a.title, c.name, c.comment_date 
            FROM comments c 
            LEFT JOIN articles a ON c.article_id = a.id 
            ORDER BY c.comment_date DESC
        """).fetchall()
        
        comentarios_list = []
        for comentario in comentarios:
            texto_clob = comentario[1]
            if texto_clob:
                if hasattr(texto_clob, 'read'):
                    texto_str = texto_clob.read()
                else:
                    texto_str = str(texto_clob)
            else:
                texto_str = ""
                
            comentarios_list.append({
                "id": comentario[0],
                "texto": texto_str,
                "articulo_titulo": comentario[2],
                "autor": comentario[3],
                "fecha": comentario[4].strftime('%d/%m/%Y %H:%M') if comentario[4] else None
            })
        
        conn.close()
        return jsonify({"success": True, "comentarios": comentarios_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/comentarios', methods=['POST'])
def crear_comentario():
    try:
        data = request.json
        articulo_id = data.get('articulo_id')
        usuario_id = data.get('usuario_id')
        texto = data.get('texto')
        
        if not articulo_id or not texto:
            return jsonify({"success": False, "error": "Artículo ID y texto son requeridos"}), 400
        
        conn = get_connection()
        cur = conn.cursor()
        cur.callproc("add_comment", [articulo_id, usuario_id, texto])
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "mensaje": "Comentario agregado exitosamente"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

#tags
@app.route('/api/tags', methods=['GET'])
def obtener_tags():
    try:
        conn = get_connection()
        cur = conn.cursor()
        tags = cur.execute("SELECT id, name, url FROM tags ORDER BY name").fetchall()
        conn.close()
        
        tags_list = [{"id": tag[0], "nombre": tag[1], "url": tag[2]} for tag in tags]
        
        return jsonify({"success": True, "tags": tags_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/tags', methods=['POST'])
def crear_tag():
    try:
        data = request.json
        nombre = data.get('nombre')
        url = data.get('url', '')
        
        if not nombre:
            return jsonify({"success": False, "error": "Nombre del tag es requerido"}), 400
        
        conn = get_connection()
        cur = conn.cursor()
        tag_id = cur.callfunc("create_tag", int, [nombre, url])
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "mensaje": "Tag creado exitosamente", "id": tag_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# categorias
@app.route('/api/categorias', methods=['GET'])
def obtener_categorias():
    try:
        conn = get_connection()
        cur = conn.cursor()
        categorias = cur.execute("SELECT id, name, url FROM categories ORDER BY name").fetchall()
        conn.close()
        
        categorias_list = [{"id": cat[0], "nombre": cat[1], "url": cat[2]} for cat in categorias]
        
        return jsonify({"success": True, "categorias": categorias_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/categorias', methods=['POST'])
def crear_categoria():
    try:
        data = request.json
        nombre = data.get('nombre')
        url = data.get('url', '')
        
        if not nombre:
            return jsonify({"success": False, "error": "Nombre de categoría es requerido"}), 400
        
        conn = get_connection()
        cur = conn.cursor()
        cat_id = cur.callfunc("create_category", int, [nombre, url])
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "mensaje": "Categoría creada exitosamente", "id": cat_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Obtener tags de un artículo
@app.route('/api/articulos/<int:articulo_id>/tags', methods=['GET'])
def obtener_tags_articulo(articulo_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        tags = cur.execute("""
            SELECT t.id, t.name, t.url 
            FROM tags t
            JOIN article_tags at ON t.id = at.tag_id
            WHERE at.article_id = :articulo_id
            ORDER BY t.name
        """, articulo_id=articulo_id).fetchall()
        conn.close()
        
        tags_list = [{"id": tag[0], "nombre": tag[1], "url": tag[2]} for tag in tags]
        
        return jsonify({"success": True, "tags": tags_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Obtener categorías de un artículo 
@app.route('/api/articulos/<int:articulo_id>/categorias', methods=['GET'])
def obtener_categorias_articulo(articulo_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        categorias = cur.execute("""
            SELECT c.id, c.name, c.url 
            FROM categories c
            JOIN article_categories ac ON c.id = ac.category_id
            WHERE ac.article_id = :articulo_id
            ORDER BY c.name
        """, articulo_id=articulo_id).fetchall()
        conn.close()
        
        categorias_list = [{"id": cat[0], "nombre": cat[1], "url": cat[2]} for cat in categorias]
        
        return jsonify({"success": True, "categorias": categorias_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Asignar tag a artículo
@app.route('/api/articulos/<int:articulo_id>/tags', methods=['POST'])
def asignar_tag_articulo(articulo_id):
    try:
        data = request.json
        tag_id = data.get('tag_id')
        
        if not tag_id:
            return jsonify({"success": False, "error": "Tag ID es requerido"}), 400
        
        conn = get_connection()
        cur = conn.cursor()
        cur.callproc("add_tag_to_article", [articulo_id, tag_id])
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "mensaje": "Tag asignado al artículo exitosamente"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Asignar categoría a artículo
@app.route('/api/articulos/<int:articulo_id>/categorias', methods=['POST'])
def asignar_categoria_articulo(articulo_id):
    try:
        data = request.json
        categoria_id = data.get('categoria_id')
        
        if not categoria_id:
            return jsonify({"success": False, "error": "Categoría ID es requerido"}), 400
        
        conn = get_connection()
        cur = conn.cursor()
        cur.callproc("add_category_to_article", [articulo_id, categoria_id])
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "mensaje": "Categoría asignada al artículo exitosamente"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Contar comentarios de un artículo
@app.route('/api/articulos/<int:articulo_id>/comentarios/count', methods=['GET'])
def contar_comentarios_articulo(articulo_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        count = cur.callfunc("count_comments", int, [articulo_id])
        conn.close()
        
        return jsonify({
            "success": True, 
            "articulo_id": articulo_id,
            "total_comentarios": count
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Eliminar artículo
@app.route('/api/articulos/<int:articulo_id>', methods=['DELETE'])
def eliminar_articulo(articulo_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.callproc("delete_article_complete", [articulo_id])
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "mensaje": "Artículo eliminado exitosamente"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor Blog Manager en http://localhost:5000")
    print("📊 Funcionalidades implementadas:")
    print("   ✅ Gestión de usuarios")
    print("   ✅ Gestión de artículos (con tags, categorías y conteo de comentarios)")
    print("   ✅ Gestión de comentarios")
    print("   ✅ Gestión de tags y categorías")
    print("   ✅ Relaciones muchos a muchos")
    print("   ✅ Conteo de comentarios")
    print("   ✅ Eliminación de artículos")
    app.run(debug=True, port=5000)