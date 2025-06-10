from flask import Flask, render_template ,request , redirect , url_for , flash
from database.models import db, Usuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db' #Esta línea le dice a Flask dónde está la base de datos.
app.config['SECRET_KEY'] = 'Maristas1.' #Esta clave secreta se usa para funciones de seguridad en Flask, como proteger los formularios y las sesiones.
db.init_app(app)


@app.route('/')
def index():
    usuarios=Usuario.query.all() #almaceno toda la lista de usarios que me dio la query en una variable llamada usuarios
    return render_template('index.html', usuarios=usuarios) # el lado izquierdo es el nombre de mi variable en mi template ("jinja2") y el lado derecho es la variable en python 
#"Hola HTML, te paso esta lista de usuarios que acabo de consultar desde la base de datos, y tú la vas a conocer como usuarios."




@app.route('/crear', methods=['GET', 'POST'])
def crear():
    #en mi template no coloque el accion porque automaticamente envia el formulario a la misma URL 
    if request.method == 'POST':
        nombre = request.form['nombre'] # extraigo el valor del formulario y lo guardo en una variable temporal
        correo = request.form['correo']
        password = request.form['password']

        nuevo_usuario = Usuario(nombre=nombre, correo=correo) #creo una instancia de la clase usuario y paso los valores de las columnas nombre y correo lado izquiero es de la DB y derecho mi variable
        nuevo_usuario.set_password(password) #hasheo la contraseña que se envio del formulario en texto plano
        db.session.add(nuevo_usuario) #agrego un nuevo objeto a la clase usuario en la sesion de la db
        db.session.commit() #confirmo los cambios pendientes en la sesion
        flash('Usuario creado exitosamente.')
        return redirect(url_for('index'))
    #cuado accede la primera vez se mostrara el formulario en el template create
    return render_template('create.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST']) # la URL vendra con un numero entero que es el id y se enviara como argumento a la funccion
def editar(id):
    usuario = Usuario.query.get_or_404(id) # hago una query a DB que me dara los datos solo de ese id y si no los encuentra que me mande un 404

    if request.method == 'POST':
        usuario.nombre = request.form['nombre'] # actualizaremos cada uno de los campos del objeto usuario con los nuevos valores del formulario (columnas) (en memoria)
        usuario.correo = request.form['correo']
        password = request.form['password']    #contraseña en texto plano temporalmente 
        if password: #verifico que no este vacio el password
            usuario.set_password(password) #hasheamos el nuevo password
        db.session.commit() #guardamos los cambios en la DB de todos los datos que nos envío el formulario
        flash('Usuario actualizado correctamente.') #mensaje flash
        return redirect(url_for('index'))

    return render_template('edit.html', usuario=usuario)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
