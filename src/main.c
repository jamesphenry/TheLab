#include <stdio.h>
#include <stdlib.h>
#include "main.h"

int greet(char *message)
{
	return puts(message);
}

/*
 * Exclude the normal program entry point when building tests.
 * The test runner provides its own main(), while functions such
 * as greet() remain available to be compiled and tested separately.
 */
#ifndef TEST

/* Marks a parameter or expression as intentionally unused.
 * Casting to void discards its value and can suppress unused-value warnings.
 */
#define UNUSED(x) (void)(x)

int main(int argc, char *argv[], char *env[]) {
	UNUSED(argc);
	UNUSED(argv);
	UNUSED(env);

	greet("Hello, World!");

	return EXIT_SUCCESS;
}

#endif
