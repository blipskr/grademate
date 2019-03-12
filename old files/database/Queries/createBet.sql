CREATE TABLE Bet (
    bet_id char(10) NOT NULL,
    exam_id char(10) NOT NULL,
    user_id char(10) NOT NULL,
    target_id char(10) NOT NULL,
    guess_mark tinyint,
    win bit,
    PRIMARY KEY(bet_id)
);