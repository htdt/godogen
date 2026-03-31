## TextServerDummy <- TextServerExtension

A dummy TextServer interface that doesn't do anything. Useful for freeing up memory when rendering text is not needed, as text servers are resource-intensive. It can also be used for performance comparisons in complex GUIs to check the impact of text rendering. A dummy text server is always available at the start of a project. Here's how to access it: The command line argument `--text-driver Dummy` (case-sensitive) can be used to force the "Dummy" TextServer on any project.

