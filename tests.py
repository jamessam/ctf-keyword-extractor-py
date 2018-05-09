import os
from unittest import main, TestCase

from extractor import get_keywords

class UnitTests(TestCase):
    def setUp(self):
        pass

    def test_get_keywords(self):
        expected = ["african","african american","agenda","agreement","american","black","business","businessman","businesswoman","cafe","coffee shop","congratulating","corporate","corporate business","deal","development","employee","greeting","handshake","man","marketing","mature","meeting","notebook","notes","optimistic","partnership","plan","planning","positive","positivity","research","restaurant",
            "shaking hands","strategy","success","suit","tanned","team","teamwork","technology","white","woman","worker","People"]
        keywords = get_keywords(os.path.join('test_files','StockSnap_ICUFI7PZGT.jpg'))
        self.assertEqual(expected, keywords)
        expected = []
        keywords = get_keywords(os.path.join('test_files','StockSnap_PPBG50NAWP.jpg'))
        self.assertEqual(expected, keywords)
        expected = ['baseball', 'striking image', 'ball']
        keywords = get_keywords(os.path.join('test_files','StockSnap_TXQJEEV01S.jpg'))
        self.assertEqual(expected, keywords)


main()
