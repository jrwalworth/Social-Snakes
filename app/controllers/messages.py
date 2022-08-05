from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
import re
from app.models.user import User
from app.models.message import Message
from app import app


@app.route('/message/new', methods=['POST'])
def newMsg():
    if 'user_id' not in session:
        flash('You must be logged in.')
        return redirect('/')
    data = {
        'sender_id' : request.form['sender_id'],
        'recipient_id' : request.form['recipient_id'],
        'text' : request.form['text'],
    }
    Message.insert(data)
    return redirect('/dashboard/')


@app.route('/delete/message/<int:id>')
def deleteMsg(id):
    data = {
        'id' : id,
    }
    Message.delete(data)
    return redirect('/dashboard/')


