import pandas as pd

class Baseline_Model:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.results = None
    
    def inference(self, start_season: str="2012-13", end_season: str="2023-24"):
        df_data = self.data.copy()

        df_data = df_data[(df_data["season_year"] >= start_season) & (df_data["season_year"] <= end_season)]
        df_data["predicted_home_win"] = df_data["h_elo_rating"] >= df_data["a_elo_rating"]

        self.results = df_data
        return self.results
    
    def get_inference_results(self):
        return self.results
    
    def get_stats(self):
        num_correct = len(self.results[self.results['predicted_home_win'] == self.results['home_wins']])
        total_rows = len(self.results)
        accuracy = num_correct / total_rows

        num_true_positives = len(self.results[(self.results['predicted_home_win'] == self.results['home_wins']) & (self.results['home_wins'] == True)])
        num_false_positives = len(self.results[(self.results['predicted_home_win'] == self.results['home_wins']) & (self.results['home_wins'] == False)])
        precision = num_true_positives / (num_true_positives + num_false_positives)

        num_positives = len(self.results[self.results['home_wins'] == True])
        recall = num_true_positives / num_positives

        f1_score = 2 * precision * recall / (precision + recall)

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
        }

