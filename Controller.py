from Model import TruyTimKhoBauModel
class TruyTimKhoBauContronller():

    def __init__(self, view):
        self.view = view
        self.model = TruyTimKhoBauModel(self)

    def getMap(self):
        return self.model.getMap()
    def getSoHang(self):
        return self.model.getSoHang()
    def getSoCot(self):
        return self.model.getSoCot()
