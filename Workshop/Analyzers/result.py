import WorkshopMetadataExtract as WME

class AnalyzerResult:
    def __init__(self, map_item: WME.WorkshopItem, upload_type, find_type, desired) -> None:
        self.item = map_item
        self.upload_type = upload_type
        self.find_type = find_type
        self.desired_list = desired
        
    def create_description(self):
        return (f"{self.upload_type} with {self.find_type} found:\n"
                f"Name: {self.item.get_title()}\n"
                f"Author: {self.item.get_creator_name()}\n"
                f"[Map Link]({self.item.map_link})\n"
                f"Desired Words: {', '.join(self.desired_list)}")