import pandas as pd

import pandas as pd

class DataFrameStyler:
    def __init__(self, df):
        self.df = df

    def highlight_min(self, color='green'):
        is_min = self.df == self.df.min()
        attr = 'background-color: {}'.format(color)
        return pd.DataFrame(np.where(is_min, attr, ''), index=self.df.index, columns=self.df.columns)

    def highlight_max(self, color='yellow'):
        is_max = self.df == self.df.max()
        attr = 'background-color: {}'.format(color)
        return pd.DataFrame(np.where(is_max, attr, ''), index=self.df.index, columns=self.df.columns)

    def highlight_top3(self, color='darkorange'):
        top3_values = self.df.stack().nlargest(3).index
        is_top3 = self.df.index.isin(top3_values.get_level_values(0))
        attr = 'color: {};font-weight: bold;'.format(color)
        return pd.DataFrame(np.where(is_top3[:, None], attr, ''), index=self.df.index, columns=self.df.columns)

    def conditional_color(self, cutoff=100, color='red'):
        is_above_cutoff = self.df > cutoff
        color = 'color: {};'.format(color)
        return pd.DataFrame(np.where(is_above_cutoff, color, ''), index=self.df.index, columns=self.df.columns)

    def color_quantile(self, color='red'):
        quantile_4_threshold = self.df.quantile(0.75)
        is_in_quantile_4 = self.df >= quantile_4_threshold
        attr = 'background-color: {}'.format(color)
        return pd.DataFrame(np.where(is_in_quantile_4, attr, ''), index=self.df.index, columns=self.df.columns)

    def get_styled_default(self):
        return (
            self.highlight_top3(color='orangered')
            .combine_first(self.color_quantile(color='khaki'))
        )



