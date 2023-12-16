import pandas as pd

class DataFrameStyler:
    def __init__(self, df):
        self.df = df

    def highlight_min(self, s, color='green'):
        is_max = s == s.min()
        attr = 'background-color: {}'.format(color)
        return [attr if v else '' for v in is_max]

    def highlight_max(self, s, color='yellow'):
        is_max = s == s.max()
        attr = 'background-color: {}'.format(color)
        return [attr if v else '' for v in is_max]

    def highlight_top3(self, s, color='darkorange'):
        top3_values = s.nlargest(3).index
        is_top3 = s.index.isin(top3_values)
        attr = 'color: {};font-weight: bold;'.format(color)
        return [attr if v else '' for v in is_top3]

    def conditional_color(self, val, cutoff=100, color='red'):
        color = color if val > cutoff else "black"
        return f"color: {color}"

    def color_quantile(self, s, color='red'):
        quantile_4_threshold = s.quantile(0.75)
        is_in_quantile_4 = s >= quantile_4_threshold
        attr = 'background-color: {}'.format(color)
        return [attr if v else '' for v in is_in_quantile_4]

    def get_styled_default(self):
        u = self.df.index.get_level_values(0)
        cols = self.df.columns
        df_styled = self.df.style.apply(
            self.highlight_top3, color='orangered', subset=pd.IndexSlice[u[:-1], cols[:-1]], axis=1
        ).apply(
            self.color_quantile, color='khaki', subset=pd.IndexSlice[u[:-1], cols[:-1]], axis=1
        )
        return df_styled

