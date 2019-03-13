# This file contains method to decide and reward the winner and method to predict the average grade

# Method: decideRewardWinner (targetMark, targetID, examID)
# it will figure out winner(s)
# reward them with equal ammount of credits from the pot
# set the bet as lost/won

# Method: predictAverage(userID, examID)
# it will return (int) average guessed mark from current bets given specific person and exam IDs

import mysql.connector
import math
from mysql.connector import Error
try:

  mydb = mysql.connector.connect(
    host = "dbhost.cs.man.ac.uk",
    user = "c71930by",
    passwd = "galaxy73",
    database = "2018_comp10120_x7"
  )
  mycursor = mydb.cursor()

  # predict average for exam of particular person
  def predictAverage(userID, examID):
    dbQuery = "SELECT `guess_mark` FROM `Game_bet` WHERE `exam_ID` = \'" + examID + "\' AND `user_id` = \'" + userID + "\'"
    mycursor.execute(dbQuery)
    currentBets = mycursor.fetchall()
    currentSum = 0
    currentGuesses = 0
    for bet in currentBets:
      currentSum += bet[0]
      currentGuesses += 1
    result = math.trunc(round(float(currentSum) / currentGuesses, 2))
    return result
    
  # take exam mark (arguments are passed to a function)
  def decideRewardWinner(targetMark, targetID, examID):
    smallestDifference = 100;
    creditsInPot = 0;
    noOfWinners = 0;
    # bets table: retrieve all rows with same examID, targetID
    dbQuery = "SELECT `bet_id`, `exam_id`, `user_id`, `target_id`, `guess_mark`, `win` FROM `Game_bet` WHERE `exam_ID` = \'" + examID + "\' AND `target_id` = \'" + targetID + "\'"
    mycursor.execute(dbQuery)
    currentBets = mycursor.fetchall()
    for bet in currentBets:
      # find the smallest difference between guessedMark and targetMark
        if smallestDifference > abs(bet[4] - targetMark):
          smallestDifference = abs(bet[4] - targetMark)
          noOfWinners = 1
        elif smallestDifference == abs(bet[4] - targetMark):
          noOfWinners+= 1
      # sum all credits on this exam
        creditsInPot += 5
    wonCredits = math.trunc(creditsInPot / noOfWinners)
    # get group id
    dbQuery = "SELECT `group_id` FROM `Game_exam` WHERE `exam_id` = \'" + examID + "\'"
    mycursor.execute(dbQuery)
    groupID = mycursor.fetchone()
    for bet in currentBets:
      # reward all winners
      if smallestDifference == abs(bet[4] - targetMark):
        # set the bet as "win": bets table
        dbQuery = "UPDATE `Game_bet` SET `win` = b'1' WHERE `bet_id` = \'" + bet[0] + "\'"
        mycursor.execute(dbQuery)
        mydb.commit()
        # reward with credits: groups table
        # get credits of the user
        dbQuery = "SELECT `credits` FROM `Game_groupmember` WHERE `group_id` = \'" + groupID[0] + "\' AND `user_id` = \'" + bet[2] + "\'"
        mycursor.execute(dbQuery)
        winnerHasCredits = mycursor.fetchone()
        # update credits of the user
        updateWithCredits = wonCredits + winnerHasCredits[0]
        dbQuery = "UPDATE `Game_groupmember` SET `credits` = \'" + str(updateWithCredits) + "\'WHERE `user_id` = \'" + bet[2] + "\'"
        mycursor.execute(dbQuery)
        mydb.commit()
      # set all loosers as loosers
      elif smallestDifference < abs(bet[4] - targetMark):
        dbQuery = "UPDATE `Game_bet` SET `win` = b'0' WHERE `bet_id` = \'" + bet[0] + "\'"

except Error as e:
  print ("Error while connecting to MySQL", e)

finally:
  if (mydb.is_connected()):
    #mydb.close()
    #print("MySQL connection is closed")
