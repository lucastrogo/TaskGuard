'''Código para as páginas referentes ao login e cadastro de usuários'''

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    '''Função para login de usuários já cadastrados'''

    if request.method == 'POST':
        usuario = request.form.get('usuario') #o campo usuario deve ter id = usuario
        senha = request.form.get('senha') #o campo senha deve ter id = senha

        user = Usuario.query.filter_by(usuario=usuario).first()
        if user != None:
            if check_password_hash(user.senha, senha):
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.logado')) #trocar 'logado' pelo nome da função da página depois de se logar
            else:
                flash('Senha incorreta, tente de novo.', category='error')
        else:
            flash('Esse usuário não existe.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    flash('Deslogado com sucesso.', category='success')
    '''Função para logout do usuário'''

    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    '''Função para cadastro de novos usuários'''

    if request.method == 'POST':
        usuario = request.form.get('usuario') #campo usuario deve ter id = usuario
        nome = request.form.get('nome').title() #campo nome deve ter id = nome
        senha1 = request.form.get('senha1') #campo senha deve ter id = senha1
        senha2 = request.form.get('senha2') #cxampo confirmação da senha deve ter id = senha2

        user = Usuario.query.filter_by(usuario=usuario).first()
        if user != None:
            flash('Esse usuário já existe.', category='error')
        elif len(usuario) < 4:
            flash('O nome de usuário deve ter mais de 3 caracteres.', category='error')
        elif len(nome) < 2:
            flash('O nome deve ter mais de 1 caracter.', category='error')
        elif senha1 != senha2:
            flash('As senhas não são iguais.', category='error')
        elif len(senha1) < 4:
            flash('A senha deve ter pelo menos 4 caracteres.', category='error')
        else:
            new_user = Usuario(usuario=usuario, 
                               nome=nome, 
                               senha=generate_password_hash(
                               senha1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada!', category='success')
            return redirect(url_for('views.logado')) #trocar 'logado' pelo nome da função da página depois de se logar

    return render_template("cadastro.html", user=current_user)