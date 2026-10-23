/*
 * Tests for src/main.c using jonruttan/test-runner.
 *
 * These tests include the implementation directly so that greet()
 * can be tested without linking a separate production executable.
 */

#include <stdio.h>
#include <stdlib.h>
#include "test-runner.h"

/*
 * Test doubles for puts():
 *
 * _retval stores the value our fake puts() should return.
 * _greet captures the string passed to puts().
 *
 * The macro below replaces calls to puts(s) in the included
 * implementation. The comma operator evaluates both expressions:
 *
 *   1. Save the supplied string pointer in _greet.
 *   2. Return the configured value in _retval.
 *
 * This lets us test greet() without printing to the terminal.
 */
static int _retval = 0;
static const char *_greet = NULL;

#define puts(s) (_greet = (s), _retval)

/*
 * Include the implementation under test.
 *
 * Because the puts macro is defined first, the puts() call inside
 * greet() is replaced by our test double.
 *
 * main() is excluded when TEST is defined, allowing the test runner
 * to provide its own entry point.
 */
#include "../src/main.c"

/*
 * Test: greet() passes the message to puts() and returns its result.
 *
 * Test structure:
 *   1. Arrange: configure inputs and expected behavior.
 *   2. Act: call the function being tested.
 *   3. Assert: check the observed results with _it_should().
 *
 * Each _it_should(description, condition) checks one assertion.
 */
static char *test_greet(void)
{
    const char *message = "hello";

    /* Arrange: make our fake puts() return 0. */
    _retval = 0;
    _greet = NULL;

    /* Act: call the function under test. */
    int result = greet((char *)message);

    /* Assert: greet() returns the value supplied by fake puts(). */
    _it_should("return the puts result", result == 0);

    /* Assert: greet() passes the expected message to puts(). */
    _it_should("pass the greeting to puts", _greet == message);

    return NULL;
}

/*
 * Additional assertion examples
 * -----------------------------
 *
 * Compare integer results:
 *
 *   _it_should("add two numbers", add(2, 3) == 5);
 *
 * Check a pointer:
 *
 *   _it_should("return a valid pointer", ptr != NULL);
 *
 * Check a condition:
 *
 *   _it_should("value is positive", value > 0);
 *
 * Test a nonzero puts() result:
 *
 *   _retval = 7;
 *   _it_should("return a nonzero puts result", greet("hello") == 7);
 *
 * The last example assumes the fake puts() macro above is active.
 * Reset shared test state when needed so one test does not depend
 * on values left behind by another test.
 */

/*
 * Test registration:
 *
 * Add one _run_test(function_name) call for each test function.
 * The runner invokes the registered tests and reports their
 * assertions.
 */
static char *run_tests(void)
{
    _run_test(test_greet);

    return NULL;
}