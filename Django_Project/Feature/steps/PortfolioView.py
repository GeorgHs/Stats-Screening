from behave import *

use_step_matcher("re")


@when("I press Export CSV")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When I press Export CSV')


@given("I am on the PortfolioView Page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given  I am on the PortfolioView Page')


@then("It should output CSV-File")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then It should output CSV-File')


@then("show Errordialog")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then show Errordialog')