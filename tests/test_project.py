from pathlib import Path
import ast,hashlib,unittest
from beer_timeseries.paths import ROOT,RAW,TABLES
class ProjectTests(unittest.TestCase):
    def test_retained_inputs_and_forecasts_exist(self):
        self.assertEqual(ROOT,Path(__file__).resolve().parents[1])
        self.assertTrue((RAW/'Beer_to_2010.csv').is_file())
        self.assertTrue((TABLES/'forecast_output_sarima.csv').is_file())
        self.assertTrue((TABLES/'prediction_ar4.csv').is_file())

    def test_active_scripts_compile_without_execution(self):
        for file in (ROOT/'scripts').glob('*.py'):compile(file.read_text(encoding='utf-8-sig'),str(file),'exec')
if __name__ == '__main__':unittest.main()
