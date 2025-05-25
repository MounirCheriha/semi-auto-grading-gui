import pandas as pd
import string
from unidecode import unidecode
import numpy as np


class Table():
    """
    A class for processing and analyzing text data from a DataFrame.
    
    Processes text data according to specified options and provides methods to:
    - Get processed table with frequencies
    - Get column indices
    - Get relations between original and processed texts
    - Calculate text frequencies
    
    Attributes:
        options (dict): Text processing options
        textsCol (str): Name of column containing texts to process
        respostesCol (str): Name of column containing corrections/responses
        df_original (pd.DataFrame): Original input DataFrame
    """

    def __init__(self, df_original: pd.DataFrame , options: dict, textsCol: str, respostesCol:str):
        """
        Initialize the Table processor.
        
        Args:
            df_original: Input DataFrame containing text data
            options: Dictionary of text processing options
                - lowercase: Convert to lowercase if True
                - punctuations: Remove punctuation if True
                - normalize: Normalize accents/unicode if True
            textsCol: Name of column containing texts to process
            respostesCol: Name of column containing corrections
        """
        self.options = options
        self.textsCol = textsCol
        self.respostesCol = respostesCol
        self.df_original = df_original

    def getTableProcessed(self) -> pd.DataFrame:
        """
        Process texts and return a DataFrame with responses, grades, frequencies, and percentages.
        
        Returns:
            DataFrame with columns:
            - Respuesta: Processed text responses
            - Nota: Corresponding grades/corrections
            - Freq: Frequency of each response
            - %: Percentage frequency of each response
        """
        df_filtered = self._process_texts(self.options, self.df_original)
        df_filtered = df_filtered.drop_duplicates(subset=[self.textsCol])
        df_filtered = df_filtered.reset_index()
        
        freq_texts, freq_percent = self._getFrequencies(df_filtered[self.textsCol])
        
        df_final = pd.DataFrame({'Respuesta': df_filtered[self.textsCol], 'Nota': df_filtered[self.respostesCol], 'Freq': freq_texts, '%': freq_percent})
        return df_final
    
    def getIdxCols(self) -> tuple:
        """
        Get the column indices for the text and correction columns.
        
        Returns:
            Tuple of (text_column_index, correction_column_index)
        """
        idxTexts = self.df_original.columns.get_loc(self.textsCol)
        idxCorr = self.df_original.columns.get_loc(self.respostesCol)
        return idxTexts, idxCorr
    
    def getRelationDict(self) -> dict:
        """
        Create a mapping between processed texts and their original text indices.
        
        Returns:
            Dictionary where:
            - Key: Processed text
            - Value: List of indices of original texts that map to this processed text
        """
        df_processed = self._process_texts(self.options, self.df_original)
        return self._makeRelations(self.df_original, df_processed)
    
    def getTotalTexts(self):
        return len(self.df_original) - 1
    
    def _process_texts(self, options: dict, df_original: pd.DataFrame) -> pd.DataFrame:
        """
        Process texts according to the specified options.
        
        Args:
            options: Dictionary of processing options
            df_original: DataFrame containing texts to process
            
        Returns:
            DataFrame with processed texts
        """
        df_filtered = df_original.copy()

        df_filtered[self.textsCol] = df_filtered[self.textsCol].astype(str)

        if options['lowercase']:
            df_filtered[self.textsCol] = df_filtered[self.textsCol].str.lower().str.strip()

        if options['punctuations']:
            df_filtered[self.textsCol] = df_filtered[self.textsCol].str.replace('[{}]'.format(string.punctuation), '', regex=True).str.strip()

        if options['normalize']:
            df_filtered[self.textsCol] = df_filtered[self.textsCol].apply(unidecode).str.strip()


        return df_filtered
    
    def _makeRelations(self, df_original: pd.DataFrame, df_processed: pd.DataFrame) -> dict:
        """
        Create a relation dictionary mapping processed texts to original text indices.
        
        Args:
            df_original: Original DataFrame
            df_processed: Processed DataFrame
            
        Returns:
            Dictionary mapping processed texts to lists of original indices
        """
        
        relationDict = {}
        original_texts = df_original[self.textsCol].tolist()
        processed_texts = df_processed[self.textsCol].tolist()

        for idOriginal in range(len(original_texts)):
            
            original = original_texts[idOriginal]
            processed = processed_texts[idOriginal]

            if processed in relationDict:  
                relationDict[processed].append(idOriginal)
            else:
                relationDict[processed] = [idOriginal]            
            

        return relationDict
    
    def _getFrequencies(self, processed_texts: pd.Series) -> tuple:
        """
        Calculate frequencies and percentages for processed texts.
        
        Args:
            processed_texts: Series of processed texts
            
        Returns:
            Tuple of (frequency_list, percentage_list)
        """
        relationDict = self.getRelationDict()
        freq_texts = []
        freq_percent = []  
        total_texts = self.getTotalTexts()

        for idProcessed in range(len(processed_texts)):
            processed = processed_texts[idProcessed]

            freq = len(relationDict[processed])

            freq_texts.append(freq)
            freq_percent.append('{0:.2f}'.format((freq/total_texts) * 100))

        return freq_texts, freq_percent