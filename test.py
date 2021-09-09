typ='one_event_eval_gen'

import datatool.seddata
dataset=datatool.seddata.SED(f'/workspace/sed2020/metadata/{typ}.tsv',typ,None)
dataset.load()
print('dataset loaded')
#