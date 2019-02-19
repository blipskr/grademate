CREATE TABLE Exams (
    group_id char(10) NOT NULL,
    exam_id char(10) NOT NULL,
    deadline_exam date NOT NULL,
    deadline_results date NOT NULL,
    PRIMARY KEY(exam_id)
);