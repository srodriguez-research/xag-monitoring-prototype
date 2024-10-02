# This is meant only to test the monitoring can run behave as a subprocess.
@given("I believe staffCardAvailable is true")
def step_impl(context):
    pass


@when("I adopt the GetCoffee goal")
def step_impl(context):
    pass


@then("plan KitchenCoffee is applicable")
def step_impl(context):
    assert True
