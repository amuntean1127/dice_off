from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re, math

class User:
    
  def __init__(self,data):
      self.id = data['id']
      self.user_name = data['user_name']
      self.created_at = data['password']


  @classmethod
  def to_session(cls, data):
      session['id'] = data['id']

  @classmethod
  def insert_user(cls,data):
      query = "INSERT INTO  users (user_name, password) VALUES (%(user_name)s, %(password)s)"
      return connectToMySQL('mydb').query_db(query, data)

  # not in use, but could be
  @classmethod
  def update_user(cls, data):
      query = "UPDATE users SET user_name = %(user_name)s WHERE id = %(id)s"
      return connectToMySQL('mydb').query_db(query, data)

  # not in use, but could be
  @classmethod
  def delete_user(cls, data):
    query = "DELETE FROM users WHERE id = %(id)s"
    return connectToMySQL('mydb').query_db(query, data)

  @classmethod
  def verify_user(cls, data):
      query = "SELECT * FROM users WHERE user_name = %(user_name)s"
      result = connectToMySQL('mydb').query_db(query, data)
      if len(result):
          return result[0]
      return False

  @classmethod
  def get_user(cls, data):
    query = "SELECT * FROM users LEFT JOIN scores ON users.id = scores.user_id WHERE users.id = %(id)s"
    results = connectToMySQL('mydb').query_db(query, data)
    
    scores = []
    high_score = 0
    last_roll = 0
    last_roll_sides = 6
    this_user = cls(results[0])
    if len(results) > 0:
      for result in results:
        if result['score_value'] != None:
          scores.append(result['score_value'])
          high_score += result['score_value']
      if results[-1]['score_value'] != None:
        last_roll = results[-1]['score_value']
      if results[-1]['dice_sides'] != None:
        last_roll_sides = results[-1]['dice_sides']
    this_user.scores = scores
    this_user.high_score = high_score
    this_user.last_roll = last_roll
    this_user.last_roll_sides = last_roll_sides

    return this_user
    
  @staticmethod
  def validate_registration(data):
      is_valid = True
      if len(data['user_name']) < 4:
          flash("Must enter a username at least 5 character long.")
          is_valid = False
      password_regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
      if not password_regex.match(data['password']):
          flash("Must enter a valid password. At least 8 characters and contain 1 number.")
          is_valid = False
      if data['password'] != data['password2']:
          flash("Your passwords do not match.")
          is_valid = False
      if is_valid == True:
          flash("User successfully created. Please login.")
      return is_valid

  # not in use, but could be
  @staticmethod
  def validate_user_edit(data):
      is_valid = True
      if len(data['user_name']) < 4:
          flash("Must enter a username at least 5 character long.")
          is_valid = False
      return is_valid