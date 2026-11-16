from pathlib import Path
import ast,hashlib,unittest
from beer_timeseries.paths import ROOT,RAW,TABLES
class MigrationChecks(unittest.TestCase):
    def test_retained_inputs_and_forecasts_exist(self):
        self.assertEqual(ROOT,Path(__file__).resolve().parents[1])
        self.assertTrue((RAW/'Beer_to_2010.csv').is_file())
        self.assertTrue((TABLES/'forecast_output_sarima.csv').is_file())
        self.assertTrue((TABLES/'prediction_ar4.csv').is_file())
    def test_forecast_variants_not_collapsed(self):
        scripts=[ROOT/'scripts/forecast.py',ROOT/'archive/submitted/ProjektPredykcja.py']
        args=[]
        for file in scripts:
            tree=ast.parse(file.read_text(encoding='utf-8-sig'))
            args.append([ast.literal_eval(n.args[1]) for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='pipeline' and n.func.attr=='predict'])
        self.assertEqual(args,[[20],[1]])
    def test_active_scripts_compile_without_execution(self):
        for file in (ROOT/'scripts').glob('*.py'):compile(file.read_text(encoding='utf-8-sig'),str(file),'exec')
if __name__ == '__main__':unittest.main()
