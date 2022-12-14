from flask import render_template,request,redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.score import Score
import random

@app.route('/')
def index():
  if 'id' not in session:
    return redirect('/login')
  user_id = session['id']
  data = { 'id': user_id }
  this_user = User.get_user(data)
  high_scores = Score.get_high_scores()
  todays_high_score = Score.get_todays_high_score()
  return render_template('index.html', user = this_user, high_scores = high_scores, todays_high_score = todays_high_score)

# this was to prevent someone from changing the HTML and passing any number into the POST request
possible_dice_sides = {'six': 6, 'thirteen': 13, 'twenty': 20}
@app.route('/score/insert', methods=["POST"])
def roll_dice():
  dice_sides = 6
  if request.form['sides'] in possible_dice_sides:
    dice_sides = possible_dice_sides[(request.form['sides'])] 
  score_value = random.randint(1, dice_sides)
  data = { 'user_id': session['id'], 'score_value': score_value, 'dice_sides': dice_sides }

  Score.insert_score(data)
  return redirect('/')
