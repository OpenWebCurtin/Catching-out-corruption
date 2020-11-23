class CouncilExtractorFactory(object):
    """
        This interface is implemented so that the AgendaItemExtractor class can 
        use the Factory Pattern to load in which ever type of Council Extractor 
        it needs. (Perth Extractor, Stirling Extractor, and Vincent Extractor).
    """
    def createSentences(self, xml_data): pass
    def formTableData(self, potential_table_data): pass
    def check_for_repeated_phrase(self, data): pass
                                        
