import csv
import tempfile
import unittest
from pathlib import Path
from scripts.build_people_queries import build, ROLE_GROUPS

class PeopleResearchTests(unittest.TestCase):
    def test_empty_employee_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            source, target = Path(temp) / "companies.csv", Path(temp) / "people.csv"
            with source.open("w", newline="") as fp:
                writer = csv.DictWriter(fp, fieldnames=["company_name","company_number"])
                writer.writeheader()
                writer.writerow({"company_name": "A Test Consulting Ltd", "company_number": "0001"})
            companies, queries = build(source, target, 1)
            self.assertEqual((companies, queries), (1, len(ROLE_GROUPS)))
            with target.open(encoding="utf-8-sig") as fp:
                rows = list(csv.DictReader(fp))
            self.assertTrue(all(not row["person_name"] and not row["profile_url"] and row["confidence"] == "not_checked" for row in rows))
            self.assertTrue(all("linkedin.com%2Fin" in row["linkedin_search"] for row in rows))

if __name__ == "__main__":
    unittest.main()
