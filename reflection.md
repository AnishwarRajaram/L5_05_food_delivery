# Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The invalid status and the made-up price were easiest. The code showed the cause clearly, and each had a small fix. Replacing pickle with JSON took the most care because the backup format changed, and I needed to keep order IDs as integers when restoring data.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

I did not find a clear false positive in the refreshed reports. Bandit's pickle warnings pointed to a real risk if someone changed the backup file before it was loaded. The original saved reports also listed issues that were not in the current code, so I treated them as stale reports rather than false positives and ran the tools again.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would run Flake8, Pylint, and Bandit before each commit and in continuous integration for every pull request. I would fix clear issues early, review security findings carefully, and keep the reports current with the code.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The program now rejects unknown menu items and incomplete orders instead of creating misleading records. JSON backups avoid executing saved data during restore. The demo uses a valid status, the functions explain their purpose, and the code passes Flake8 with a Pylint score of 10.00/10. Bandit reports no issues.
