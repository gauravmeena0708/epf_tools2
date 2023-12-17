import pandas as pd

class DataFrameStyler:
    @staticmethod
    def highlight_min(s, color='green'):
        is_max = s == s.min()
        attr = 'background-color: {}'.format(color)
        return [attr if v else '' for v in is_max]

    @staticmethod
    def highlight_max(s, color='yellow'):
        is_max = s == s.max()
        attr = 'background-color: {}'.format(color)
        return [attr if v else '' for v in is_max]

    @staticmethod
    def highlight_top3(s, color='darkorange'):
        top3_values = s.nlargest(3).index
        is_top3 = s.index.isin(top3_values)
        attr = 'color: {};font-weight: bold;'.format(color)
        return [attr if v else '' for v in is_top3]

    @staticmethod
    def conditional_color(val, cutoff=100, color='red'):
        color = color if val > cutoff else "black"
        return f"color: {color}"

    @staticmethod
    def color_quantile(s, color='red'):
        quantile_4_threshold = s.quantile(0.75)
        is_in_quantile_4 = (s >= quantile_4_threshold) & (s > 0)
        attr = 'background-color: {}'.format(color)
        return [attr if v else '' for v in is_in_quantile_4]

    @staticmethod
    def get_styled_default(df,axis=1):
        u = df.index.get_level_values(0)
        cols = df.columns
        df_styled = df.style.apply(
            DataFrameStyler.highlight_top3, color='orangered', subset=pd.IndexSlice[u[:-1], cols[:-1]], axis=axis
        ).apply(
            DataFrameStyler.color_quantile, color='khaki', subset=pd.IndexSlice[u[:-1], cols[:-1]], axis=axis
        )
        return df_styled


