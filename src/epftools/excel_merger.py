import os
import pandas as pd

class ExcelMerger:
    def __init__(self, folder_path, ext=".xlsx", sheetnum=0):
        self.folder_path = folder_path
        self.ext    = ext
        self.excel_names = self.get_excel_files()
        self.excels = self.load_excels()
        self.frames = self.extract_frames()
        
        self.sheet_num = 0

    def get_excel_files(self):
        excel_names = [filename for filename in os.listdir(self.folder_path) if filename.endswith(self.ext)]
        return excel_names

    def load_excels(self):
        excels = []
        for name in self.excel_names:
            try:
                excels.append(pd.ExcelFile(os.path.join(self.folder_path, name)))
            except IndexError:
                print(name)
        return excels

    def extract_frames(self):
        frames = [x.parse(x.sheet_names[self.sheet_num], header=None, index_col=None) for x in self.excels]
        # Delete the first row for all frames except the first
        # i.e. remove the header row -- assumes it's the first
        frames[1:] = [df[1:] for df in frames[1:]]

        return frames

    def merge_and_save(self, output_filename="merged.xlsx"):
        # Concatenate the frames
        combined = pd.concat(self.frames)
        # Write it out to Excel
        combined.to_excel(output_filename, header=False, index=False)
        print(f"Merged Excel files saved to {output_filename}")

"""
# Example usage:
if __name__ == "__main__":
    folder_path = '<Dir path>'
    merger = ExcelMerger(folder_path)
    merger.merge_and_save()
"""