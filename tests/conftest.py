def pytest_terminal_summary(terminalreporter, exitstatus, config):
    terminalreporter.section("Custom Test Summary")
    for test in terminalreporter.stats.get("passed", []):
        terminalreporter.write_line(f"PASSED: {test.nodeid}")
    for test in terminalreporter.stats.get("failed", []):
        terminalreporter.write_line(f"FAILED: {test.nodeid}")
    for test in terminalreporter.stats.get("skipped", []):
        terminalreporter.write_line(f"SKIPPED: {test.nodeid}")
    for test in terminalreporter.stats.get("error", []):
        terminalreporter.write_line(f"ERROR: {test.nodeid}")
