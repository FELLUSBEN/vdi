from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required,  current_user
from .models import Pc
from . import db
import json
import webbrowser
from .dcoker_manager import manager


views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        pc = request.form.get('pc')
        if len(pc) < 1:
            flash('pc is too short!', category='error')
        else:
            new_pc = Pc(data=pc, user_id=current_user.id)
            db.session.add(new_pc)
            db.session.commit()
            flash('Computer created successfully!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/start-pc', methods=['POST'])
def startPc():
    pc = json.loads(request.data)
    PcId = pc['PcId']
    pc = Pc.query.get(PcId)

    if pc:
        if pc.user_id == current_user.id:
            #db.session.delete(pc)
            #db.session.commit()
            m = manager()
            m.create(pc.id)
    return redirect("http://192.168.1.40:"+str(pc.id + 8080))

@views.route('/stop-pc', methods=['POST'])
def stopPc():
    pc = json.loads(request.data)
    PcId = pc['PcId']
    pc = Pc.query.get(PcId)
    if pc:
        if pc.user_id == current_user.id:
            m = manager()
            m.stop(pc)
    return jsonify({})




