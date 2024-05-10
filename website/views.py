'''Arquivo para as outras funções'''
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Usuario, Materia, Topico, Anotacao
from . import db
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@login_required
@views.route('/logado')
def logado():
    materias = Materia.query.filter(Materia.id_usuario==current_user.id).all()
    return render_template('logado.html', materias=materias)

@login_required
@views.route('/adicionar_materia', methods=['POST'])
def adicionar_materia():
    nome = request.form['nome']
    if nome == '':
        flash('A matéria precisa ter um nome.', category='error')
        return redirect(url_for('views.logado'))
    materia = Materia(nome=nome, id_usuario=current_user.id)
    db.session.add(materia)
    db.session.commit()
    flash('Matéria adicionada com sucesso!', 'success')
    return redirect(url_for('views.logado'))

@login_required
@views.route('/materia/<int:id_materia>')
def materia(id_materia):
    materia = Materia.query.get(id_materia)
    return render_template('materia.html', materia=materia)

@login_required
@views.route('/topico/<int:id_topico>')
def topico(id_topico):
    topico = Topico.query.get(id_topico)
    # Calcula a diferença de dias entre o prazo e a data de criação
    diferenca = None  # Inicialmente definimos a diferença como None
    if topico.prazo:
        hoje = datetime.utcnow().date()
        prazo = datetime.strptime(topico.prazo, '%Y-%m-%d').date()
        diferenca = (prazo - hoje).days
    return render_template('topico.html', topico=topico, diferenca=diferenca)

@login_required
@views.route('/adicionar_topico/<int:id_materia>', methods=['POST'])
def adicionar_topico(id_materia):
    nome = request.form['nome']
    prazo_str = request.form['prazo']
    if nome == '':
        flash('O tópico precisa ter um nome.', category='error')
        return redirect(url_for('views.materia', id_materia=id_materia))
    topico = Topico(nome=nome, id_materia=id_materia, prazo=prazo_str)
    db.session.add(topico)
    db.session.commit()

    flash('Tópico e prazo adicionados com sucesso!', 'success')
    return redirect(url_for('views.materia', id_materia=id_materia))

@login_required
@views.route('/marcar_completo/<int:id_topico>/<int:finalizado>', methods=['POST','GET'])
def marcar_completo(id_topico, finalizado):
    topico = Topico.query.get(id_topico)
    if finalizado == 1:
        topico.completo = True
        flash('Tópico marcado como concluído!', 'success')
    else:
        topico.completo = False
        flash('Tópico marcado como não concluído!', 'danger')
    db.session.commit()
    return redirect(url_for('views.topico', id_topico=topico.id))

@login_required
@views.route('/adicionar_anotacao/<int:id_topico>', methods=['POST'])
def adicionar_anotacao(id_topico):
    texto = request.form['texto']
    if texto == '':
        flash('A anotação não pode estar vazia.', category='error')
        return redirect(url_for('views.topico', id_topico=id_topico))
    anotacao = Anotacao(texto=texto, id_topico=id_topico)
    db.session.add(anotacao)
    db.session.commit()
    flash('Anotação adicionada com sucesso!', 'success')
    return redirect(url_for('views.topico', id_topico=id_topico))

@login_required
@views.route('/excluir_topico/<int:id_topico>', methods=['POST'])
def excluir_topico(id_topico):
    topico = Topico.query.get(id_topico)
    
    if topico:
        # Exclua o tópico do banco de dados
        db.session.delete(topico)
        db.session.commit()
        flash('Tópico excluído com sucesso!', 'success')
    else:
        flash('Tópico não encontrado', 'danger')
    
    # Redirecione de volta para a página de detalhes da matéria
    return redirect(url_for('views.materia', id_materia=topico.id_materia))

@login_required
@views.route('/excluir_anotacao/<int:id_anotacao>', methods=['POST'])
def excluir_anotacao(id_anotacao):
    anotacao = Anotacao.query.get(id_anotacao)
    
    if anotacao:
        # Exclua o tópico do banco de dados
        db.session.delete(anotacao)
        db.session.commit()
        flash('Anotação excluída com sucesso!', 'success')
    else:
        flash('Anotação não encontrada', 'danger')
    
    # Redirecione de volta para a página de detalhes da matéria
    return redirect(url_for('views.topico', id_topico=anotacao.id_topico))

@login_required
@views.route('/excluir_materia/<int:id_materia>', methods=['POST'])
def excluir_materia(id_materia):
    materia = Materia.query.get(id_materia)
    
    if materia:
        # Exclua o tópico do banco de dados
        db.session.delete(materia)
        db.session.commit()
        flash('Matéria excluída com sucesso!', 'success')
    else:
        flash('Matéria não encontrada', 'danger')
    
    # Redirecione de volta para a página de detalhes da matéria
    return redirect(url_for('views.logado'))