from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Score:
  def __init__(self,data):
    self.id = data['id']
    self.score_value = data['scre_value']
    self.user_id = data['user_id']
    self.created_at = data['created_at']
    self.dice_sides = data['sides']


  @classmethod
  def insert_score(cls, data):
    query = "INSERT INTO  scores (score_value, user_id, dice_sides) VALUES (%(score_value)s, %(user_id)s, %(dice_sides)s)"
    return connectToMySQL('mydb').query_db(query, data)

  @classmethod
  def get_high_scores(cls):
    query = """
    SELECT users.id, users.user_name, SUM(scores.score_value) AS high_score
    FROM scores 
    JOIN users
      ON users.id = scores.user_id
    GROUP BY users.id
    ORDER BY high_score DESC
    """
    result = connectToMySQL("mydb").query_db(query)

    return result

  @classmethod
  def get_todays_high_score(cls):
    query = """
    SELECT users.id, users.user_name, sum(scores.score_value) as todays_high_score, DATE(scores.created_at) AS score_date
    FROM scores
    JOIN users
      ON scores.user_id = users.id
    WHERE CURDATE() = DATE(scores.created_at)
    GROUP BY users.id
    ORDER BY todays_high_score DESC
    LIMIT 1;
    """
    result = connectToMySQL("mydb").query_db(query)

    print(result)

    return result
