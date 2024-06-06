from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect
from datetime import datetime

from app import db
from app.forms import CommentForm
from app.models import Question, Answer, Comment
from .auth_views import login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/create/answer/<int:answer_id>', methods = ['GET', 'POST'])
@login_required
def create_answer(answer_id):
   form = CommentForm()
   answer = Answer.query.get_or_404(answer_id)
   if request.method == 'POST' and form.validate_on_submit():
      content = request.form['content']     
      if (g.user):
         comment = Comment(content=content, create_date=datetime.now(), user=g.user, answer=answer)
      else:
         comment = Comment(content=content, create_date=datetime.now(), answer=answer)
      db.session.add(comment)
      db.session.commit()
      return redirect(url_for('question.detail', question_id=answer.question_id, answer_id=answer.id))
   return render_template('comment_form.html', form=form)
	
@bp.route('/modify/answer/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_answer(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=comment.answer.id))
    if request.method == "POST":
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=comment.answer.question.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment_form.html', form=form)
    
@bp.route('/delete/answer/<int:comment_id>')
@login_required
def delete_answer(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    question_id = comment.answer.question.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
