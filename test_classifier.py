import pickle
from classifier.SimpleKeras import SimpleKeras
with open('objs1.pkl','rb') as f:  # Python 3: open(..., 'wb')
    Sdataset,Sdatalabel,func=pickle.load(f)
    sk=SimpleKeras()
    sk.epochs=10
    sk.createmodel(len(Sdataset[0]),20)
    sk.train(Sdataset, Sdatalabel) 
    print(Sdataset)