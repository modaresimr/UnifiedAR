
class GEM:
    classical=False
    def eval(self,real_a_event, pred_a_event, acts,debug=0):
        import metric.MyMetric as mymetric
        return mymetric.eval(real_a_event, pred_a_event, acts,debug)
    def __str__():
        return 'GEM'

class Classical:
    classical=True
    def eval(self,rlabel,plabel,acts):
        import metric.MyClassical as myclassical
        return myclassical.eval(rlabel,plabel, acts)
    def __str__(self):
        return 'Classical'
        
class Tatbul:
    classical=False
    def eval(self,real_a_event, pred_a_event, acts,debug=0):
        import metric.TatbulMetric as mytatbul
        return mytatbul.eval(real_a_event, pred_a_event, acts,debug)
    def __str__(self):
        return 'Tatbul'