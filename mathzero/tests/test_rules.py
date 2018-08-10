from ..core.tree_node import BinaryTreeNode
from ..core.parser import ExpressionParser
from ..core.expressions import (
    ConstantExpression,
    VariableExpression,
    AddExpression,
    MultiplyExpression,
    DivideExpression,
)
from ..core.util import getTerms, termsAreLike
from ..core.rules import (
    AssociativeSwapRule,
    CommutativeSwapRule,
    DistributiveFactorOutRule,
    DistributiveMultiplyRule,
    ConstantsSimplifyRule,
    CombineLikeTermsRule,
    SimplifyComplexTermRule,
)


def test_commutative_property():
    left = ConstantExpression(4)
    right = ConstantExpression(17)
    expr = AddExpression(left, right)
    assert str(expr) == "4 + 17"
    rule = CommutativeSwapRule()

    # can find the root-level nodes
    nodes = rule.findNodes(expr)
    assert len(nodes) == 1

    # This expression is commutative compatible
    assert rule.canApplyTo(expr) == True

    # Applying swaps the left/right position of the Const nodes in the Add expression
    result = rule.applyTo(expr).end.getRoot()
    assert result.left.value == right.value
    assert result.right.value == left.value
    assert str(expr) == "17 + 4"


def test_commutative_property_cannot_apply():
    left = ConstantExpression(4)
    right = ConstantExpression(17)
    expr = DivideExpression(left, right)
    rule = CommutativeSwapRule()
    # This expression is NOT commutative compatible because 4 / 3 != 3 / 4
    assert rule.canApplyTo(expr) == False
    # Nope
    assert len(rule.findNodes(expr)) == 0


def test_commutative_property_truncate():
    parser = ExpressionParser()
    expr = parser.parse("(7 + x) + 2")
    rule = CommutativeSwapRule()

    change = rule.applyTo(expr)
    assert str(change.end) == "2 + (7 + x)"


def test_constants_simplify_rule():
    parser = ExpressionParser()
    expectations = [("7 + 4", 11), ("1 - 2", -1), ("4 / 2", 2), ("5 * 5", 25)]
    for input, output in expectations:
        expression = parser.parse(input)
        rule = ConstantsSimplifyRule()
        assert rule.canApplyTo(expression) == True
        assert rule.applyTo(expression).end.getRoot().value == output


def test_distributive_factoring():
    parser = ExpressionParser()
    expression = parser.parse("7 + 7")
    rule = DistributiveFactorOutRule()
    assert rule.canApplyTo(expression) == True
    out = rule.applyTo(expression).end.getRoot()
    assert str(out) == "7 * (1 + 1)"


def test_distributive_factoring_with_variables():
    parser = ExpressionParser()
    expression = parser.parse("14x + 7x")
    rule = DistributiveFactorOutRule()
    assert rule.canApplyTo(expression) == True
    out = rule.applyTo(expression).end.getRoot()
    assert str(out) == "7x * (2 + 1)"


def test_distributive_factoring_factors():
    pass
    parser = ExpressionParser()
    expression = parser.parse("4 + (z + 4)")
    rule = DistributiveFactorOutRule()
    assert rule.canApplyTo(expression) == False


def test_common_properties_can_apply_to():
    parser = ExpressionParser()
    expression = parser.parse("7 + 4x - 2")

    available_actions = [
        CommutativeSwapRule(),
        DistributiveFactorOutRule(),
        DistributiveMultiplyRule(),
        AssociativeSwapRule(),
    ]
    for action in available_actions:
        assert type(action.canApplyTo(expression)) == bool


def test_associative_swap():
    parser = ExpressionParser()
    exp = parser.parse("(2 + x) + 9")
    rule = AssociativeSwapRule()
    nodes = rule.findNodes(exp)
    assert len(nodes) == 1
    change = rule.applyTo(nodes[0])
    assert str(change.end.getRoot()).strip() == "2 + (x + 9)"


def test_combine_like_terms():
    parser = ExpressionParser()
    rule = CombineLikeTermsRule()
    expr = parser.parse("(x * 14 + 7x) + 2")
    node = rule.findNode(expr)
    change = rule.applyTo(node)
    assert str(change.end.getRoot()) == "21x + 2"

    expr = parser.parse("4x + 7x + 2")
    node = rule.findNode(expr)
    change = rule.applyTo(node)
    assert str(change.end.getRoot()) == "11x + 2"

    expr = parser.parse("6x + 120x")
    node = rule.findNode(expr)
    change = rule.applyTo(node)
    assert str(change.end.getRoot()) == "126x"

    expr = parser.parse("3x + 72x")
    node = rule.findNode(expr)
    change = rule.applyTo(node)
    assert str(change.end.getRoot()) == "75x"


def test_combine_like_terms_fail():
    examples = ["29y + (8 + 144y)", "10z + (8 + 44z)"]
    parser = ExpressionParser()
    rule = CombineLikeTermsRule()
    for input in examples:
        expr = parser.parse(input)
        assert rule.findNode(expr) is None


def test_like_terms_compare():
    parser = ExpressionParser()
    expr = parser.parse("10 + (7x + 6x)")
    terms = getTerms(expr)
    assert len(terms) == 3
    assert not termsAreLike(terms[0], terms[1])
    assert termsAreLike(terms[1], terms[2])

    expr = parser.parse("10 + 7x + 6")
    terms = getTerms(expr)
    assert len(terms) == 3
    assert not termsAreLike(terms[0], terms[1])
    assert termsAreLike(terms[0], terms[2])

    expr = parser.parse("6x + 6 * 5")
    terms = getTerms(expr)
    assert len(terms) == 2
    assert not termsAreLike(terms[0], terms[1])

    expr = parser.parse("360y^1")
    terms = getTerms(expr)
    assert len(terms) == 1

    expr = parser.parse("4z")
    terms = getTerms(expr)
    assert len(terms) == 1


def test_simplify_complex_term():
    parser = ExpressionParser()
    rule = SimplifyComplexTermRule()
    expr = parser.parse("60 * 6y")
    node = rule.findNode(expr)
    change = rule.applyTo(node)
    assert str(change.end.getRoot()) == "360y"

    left = parser.parse("4x")
    right = parser.parse("7x")
    expr = MultiplyExpression(left, right)
    change = rule.applyTo(expr)
    assert str(change.end) == "28x^2"

