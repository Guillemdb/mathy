# coding: utf8
import random

from ....game_modes import MODE_SIMPLIFY_POLYNOMIAL
from ...training.lessons import LessonExercise, LessonPlan, build_lesson_plan
from ..problems import (
    get_rand_vars,
    maybe_int,
    maybe_power,
    rand_bool,
    rand_var,
    simplify_multiple_terms,
    combine_terms_after_commuting,
    combine_terms_in_place,
    move_around_blockers_one,
    move_around_blockers_two,
)

moves_per_complexity = 4

green_belt_practice = build_lesson_plan(
    "green_belt_practice",
    [
        LessonExercise(
            lesson_name="five_terms",
            problem_count=4,
            problem_fn=lambda: simplify_multiple_terms(5),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=500,
            num_observations=64,
        ),
        LessonExercise(
            lesson_name="six_terms_with_exponents",
            problem_count=4,
            problem_fn=lambda: simplify_multiple_terms(6, powers=True),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=500,
            num_observations=64,
        ),
        LessonExercise(
            lesson_name="eight_terms_with_exponents",
            problem_count=4,
            problem_fn=lambda: simplify_multiple_terms(8, powers=True),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=500,
            num_observations=64,
        ),
        LessonExercise(
            lesson_name="ten_terms_with_exponents",
            problem_fn=lambda: simplify_multiple_terms(10, powers=True),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            problem_count=4,
            mcts_sims=500,
            num_observations=64,
        ),
    ],
)


green_belt = build_lesson_plan(
    "green_belt",
    [
        LessonExercise(
            lesson_name="six_terms_with_exponents",
            problem_count=4,
            problem_fn=lambda: simplify_multiple_terms(6, powers=True),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=50,
            num_observations=32,
        ),
        LessonExercise(
            lesson_name="eight_terms_with_exponents",
            problem_count=4,
            problem_fn=lambda: simplify_multiple_terms(8, powers=True),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=50,
            num_observations=32,
        ),
        LessonExercise(
            lesson_name="commute_blockers_1_7",
            problem_fn=lambda: move_around_blockers_one(7),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            problem_count=4,
            mcts_sims=50,
            num_observations=32,
        ),
        LessonExercise(
            lesson_name="ten_terms_with_exponents",
            problem_fn=lambda: simplify_multiple_terms(10, powers=True),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            problem_count=4,
            mcts_sims=50,
            num_observations=32,
        ),
        LessonExercise(
            lesson_name="commute_blockers_2_7",
            problem_fn=lambda: move_around_blockers_two(7),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            problem_count=4,
            mcts_sims=50,
            num_observations=32,
        ),
    ],
)