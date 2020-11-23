import website

class SearchEngine():
    def make_relation_search_results(self):
        return [website.models.RelationResult.objects.create(
            kp1="Key_Phrase_1",
            kp2="Key_Phrase_2",
            kp3="Key_Phrase_3",
            document='Document1',
            agenda_item_file="893853.pdf",
            agenda_item="Agenda Item 354/07",
            description="Description of agenda item ..."
        )] * 100

    def make_document_search_results(self):
        return [website.models.DocumentResult.objects.create(
            document='Document1',
            occurs_total=42,
            occurs_agenda_items=6,
            normalised_score=18
        )] * 100
    
    def create_search(self, searchObject):
        outSearch = []
        ii = 0
        if(searchObject.key_phrase1 != ""):
           outSearch.append([searchObject.key_phrase1, float(searchObject.key_phrase_importance1), searchObject.key_phrase_type1])
        if(searchObject.key_phrase2 != ""):
            outSearch.append([searchObject.key_phrase2, float(searchObject.key_phrase_importance2), searchObject.key_phrase_type2])
        if(searchObject.key_phrase3 != ""):
            outSearch.append([searchObject.key_phrase3, float(searchObject.key_phrase_importance3), searchObject.key_phrase_type3])
        if(searchObject.key_phrase4 != ""):
            outSearch.append([searchObject.key_phrase4, float(searchObject.key_phrase_importance4), searchObject.key_phrase_type4])
        if(searchObject.key_phrase5 != ""):
            outSearch.append([searchObject.key_phrase5, float(searchObject.key_phrase_importance5), searchObject.key_phrase_type5])
        return outSearch
    def create_results_minute(self, searchResults):
        outResults = []
        for result in searchResults:
            keyPhrase1 = ""
            keyPhrase2 = ""
            keyPhrase3 = ""
            keyPhrase4 = ""
            keyPhrase5 = ""
            ii = 0
            for phrase in result[2]:
                if(ii == 0):
                    keyPhrase1 = phrase
                if(ii == 1):
                    keyPhrase2 = phrase
                if(ii == 2):
                    keyPhrase3 = phrase
                if(ii == 3):
                    keyPhrase4 = phrase
                if(ii == 4):
                    keyPhrase5 = phrase
                ii = ii +1
            
            a = website.models.RelationResult.objects.create(
                kp1=keyPhrase1,
                kp2=keyPhrase2,
                kp3=keyPhrase3,
                kp4=keyPhrase4,
                kp5=keyPhrase5,
            document=result[1],
            agenda_item_file="not_working.pdf",
            agenda_item=result[0],
            description="Description of agenda item ...",
            search_type=0
            )
            outResults.append(a)
        return outResults
    def create_results_non_minute(self, searchResults):
        outResults = []
        for result in searchResults:
            keyPhrase1 = ""
            keyPhrase2 = ""
            keyPhrase3 = ""
            keyPhrase4 = ""
            keyPhrase5 = ""
            ii = 0
            for phrase in result[1]:
                if(ii == 0):
                    keyPhrase1 = phrase
                if(ii == 1):
                    keyPhrase2 = phrase
                if(ii == 2):
                    keyPhrase3 = phrase
                if(ii == 3):
                    keyPhrase4 = phrase
                if(ii == 4):
                    keyPhrase5 = phrase
                ii = ii +1
            
            a = website.models.RelationResult.objects.create(
                kp1=keyPhrase1,
                kp2=keyPhrase2,
                kp3=keyPhrase3,
                kp4=keyPhrase4,
                kp5=keyPhrase5,
            document=result[0],
            agenda_item_file="not_working.pdf",
            agenda_item="no agenda",
            description="Description of agenda item ...",
            search_type=1
            )
            outResults.append(a)
        return outResults
    def relation_search(self, model):
        
        return self.make_relation_search_results()

    def document_search(self, model):
        # TODO Implemented in another task.
        return self.make_document_search_results()
