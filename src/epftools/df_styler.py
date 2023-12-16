import pandas as pd

class DataFrameStyler:

    def __init__(self, df):
        self.df = df

    def highlight_top3(self, color='darkorange'):
        """Highlights the top 3 values in a Series."""
        top3_values = self.df.nlargest(3).index
        is_top3 = self.df.index.isin(top3_values)
        return self.df.style.apply(lambda x: f"color: {color}; font-weight: bold;" if x in is_top3 else "", axis=1)

    def conditional_color(self, cutoff, color='red', subset=None):
        """Applies conditional color based on a cutoff value."""
        if subset is None:
            subset = pd.IndexSlice[:self.df.index.get_level_values(0).size, :]
        return self.df.style.map(lambda x: f"color: {color}" if x > cutoff else "", subset=subset)

    def color_quantile(self, quantile, color='khaki', subset=None):
        """Applies color based on quantile."""
        if subset is None:
            subset = pd.IndexSlice[:self.df.index.get_level_values(0).size, :]
        quantile_threshold = self.df.quantile(quantile)
        is_in_quantile = self.df >= quantile_threshold
        return self.df.style.apply(lambda x: f"background-color: {color}" if x >= quantile_threshold else "", subset=subset)

    def get_styled_default(self):
        """Applies default styling based on top 3 and quantile."""
        u = self.df.index.get_level_values(0)
        cols = self.df.columns
        styled_df = self.style.apply(highlight_top3,color='orangered',subset = pd.IndexSlice[u[:-1], cols[:-1]],axis=1) \
            .apply(color_quantile,color='khaki',subset = pd.IndexSlice[u[:-1], cols[:-1]],axis=1) 
        return styled_df

