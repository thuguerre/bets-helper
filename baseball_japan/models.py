class Converter:

    references = [
        {"nbp_letter": "B", "winamax_name": "Orix Buffaloes", "winamax_id": 67116},
        {"nbp_letter": "C", "winamax_name": "Hiroshima Toyo Carp", "winamax_id": 67106},
        {"nbp_letter": "D", "winamax_name": "Chunichi Dragons", "winamax_id": 67104},
        {"nbp_letter": "DB", "winamax_name": "Yokohama Baystars", "winamax_id": 67110},
        {"nbp_letter": "E", "winamax_name": "Rakuten Gold. Eagles", "winamax_id": 67118},
        {"nbp_letter": "F", "winamax_name": "Hokkaido Nippon-Ham Fighters", "winamax_id": 67114},
        {"nbp_letter": "G", "winamax_name": "Yomiuri Giants", "winamax_id": 34374},
        {"nbp_letter": "H", "winamax_name": "Fukuoka Softbank Hawks", "winamax_id": 67122},
        {"nbp_letter": "L", "winamax_name": "Saitama Seibu Lions", "winamax_id": 67120},
        {"nbp_letter": "M", "winamax_name": "Chiba Lotte Marines", "winamax_id": 67112},
        {"nbp_letter": "S", "winamax_name": "Tokyo Yakult Swallows", "winamax_id": 67108},
        {"nbp_letter": "T", "winamax_name": "Hanshin Tigers", "winamax_id": 22108}
    ]

    def get_winamax_name(self, npb_letter: str) -> str:
        for reference in self.references:
            if reference["nbp_letter"] == npb_letter:
                return reference["winamax_name"]

        raise Exception

    def get_winamax_id(self, npb_letter: str) -> int:
        for reference in self.references:
            if reference["nbp_letter"] == npb_letter:
                return reference["winamax_id"]

        raise Exception
        