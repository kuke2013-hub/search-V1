import csv
import tempfile
import unittest
from pathlib import Path
from scripts.import_companies_house import convert, london_district, sector_match

class CompanyImportTests(unittest.TestCase):
    def test_postcodes(self):
        self.assertEqual(london_district("EC2M 7AN"), "EC2M")
        self.assertEqual(london_district("SW1Y 6QY"), "SW1Y")
        self.assertEqual(london_district("GU1 1AB"), "")
        self.assertEqual(london_district("nonsense"), "")

    def test_sic(self):
        self.assertEqual(sector_match({"SICCode.SicText_1": "70229 - Management consultancy activities"}),
                         ("70229", "Consulting & head offices"))
        self.assertIsNone(sector_match({"SICCode.SicText_1": "99999 - none"}))

    def test_import(self):
        with tempfile.TemporaryDirectory() as temp:
            source, target = Path(temp) / "source.csv", Path(temp) / "output.csv"
            fields = ["CompanyName", "CompanyNumber", "CompanyStatus", "RegAddress.PostCode",
                      "SICCode.SicText_1", "Accounts.AccountCategory"]
            with source.open("w", newline="") as fp:
                writer = csv.DictWriter(fp, fieldnames=fields)
                writer.writeheader()
                writer.writerows([
                    {"CompanyName": "London Advisory", "CompanyNumber": "0001", "CompanyStatus": "Active", "RegAddress.PostCode": "EC1A 1BB", "SICCode.SicText_1": "70229 - Consultancy"},
                    {"CompanyName": "Dissolved", "CompanyNumber": "0002", "CompanyStatus": "Dissolved", "RegAddress.PostCode": "EC1A 1BB", "SICCode.SicText_1": "70229 - Consultancy"},
                    {"CompanyName": "Non London", "CompanyNumber": "0003", "CompanyStatus": "Active", "RegAddress.PostCode": "GU1 1AB", "SICCode.SicText_1": "70229 - Consultancy"}
                ])
            self.assertEqual(convert([source], target), (3, 1))
            with target.open(encoding="utf-8-sig", newline="") as fp:
                row = next(csv.DictReader(fp))
            self.assertEqual(row["company_name"], "London Advisory")
            self.assertEqual(row["headcount"], "")
            self.assertEqual(row["workplace_verified"], "no")

if __name__ == "__main__":
    unittest.main()
