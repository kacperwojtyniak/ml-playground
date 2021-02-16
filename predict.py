from fastai.learner import *

learner = load_learner('./export.pkl')
v = learner.dls.vocab
res = learner.predict('./cheetah.jpg')
print(res)