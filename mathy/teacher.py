from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class StudentEvaluation(BaseModel):
    env: str
    total: int
    solved: int
    failed: int


class Topic(BaseModel):
    # The topic name used to interpolate the env name
    name: str
    # The current topic difficulty
    difficulty: str = "easy"
    # The number of observations for the current eval window
    count: int = 0
    # The current positives count
    positives: int = 0
    # The current negatives count
    negatives: int = 0

    def reset_counts(self):
        self.positives = 0
        self.negatives = 0
        self.count = 0


class Student(BaseModel):
    # The index of the student in the students list
    id: int
    # Current topic of study
    topic: str
    # The current difficulty settings for each env
    topics: Dict[str, Topic]
    # How many problems between each evaluation?
    eval_window: int = 10
    # Reported results
    evaluations: List[StudentEvaluation] = []


class Teacher:
    students: List[Student]

    def __init__(
        self,
        topic_names: List[str],
        num_students: int = 1,
        eval_window: int = 4,
        win_threshold: float = 0.90,
        lose_threshold: float = 0.40,
    ):
        self.topic_names = topic_names
        self.eval_window = eval_window
        self.win_threshold = win_threshold
        self.lose_threshold = lose_threshold
        self.initialize_students(num_students)

    def initialize_students(self, num_students: int):
        self.num_students = num_students
        self.students = []
        for i in range(self.num_students):
            student_topics = {}
            for topic in self.topic_names:
                student_topics[topic] = Topic(name=topic)
            self.students.append(Student(id=i, topic=topic, topics=student_topics))

    def get_student(self, student_id: int) -> Student:
        return self.students[student_id]

    def previous_difficulty(self, difficulty: str) -> str:
        if difficulty == "hard":
            return "normal"
        elif difficulty == "normal":
            return "easy"
        return "easy"

    def next_difficulty(self, difficulty: str) -> str:
        if difficulty == "easy":
            return "normal"
        elif difficulty == "normal":
            return "hard"
        return "hard"

    def report_result(
        self, student_id: int, reward: float, data: Any = None
    ) -> Optional[float]:
        student = self.get_student(student_id)
        topic: Topic = student.topics[student.topic]
        if reward > 0.0:
            topic.positives += 1
        else:
            topic.negatives += 1
        topic.count += 1

        if topic.count >= self.eval_window:
            win_ratio = topic.positives / self.eval_window

            def truncate(value):
                return float("%.3f" % (float(value)))

            print(f"{topic.name} evaluation... {truncate(win_ratio)}")
            if win_ratio >= self.win_threshold:
                topic.difficulty = self.next_difficulty(topic.difficulty)
            elif win_ratio <= self.lose_threshold:
                topic.difficulty = self.previous_difficulty(topic.difficulty)
            else:
                pass
            topic.reset_counts()
            return win_ratio
        return None

    def get_env(self, student_id: int, iteration: int) -> str:
        student = self.get_student(student_id)
        student.topic = self.topic_names[iteration % len(self.topic_names)]
        topic = student.topics[student.topic]
        return f"mathy-{topic.name}-{topic.difficulty}-v0"
