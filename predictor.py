''' forumulate prediction message based on categories and outputs from learner '''

import settings

def PredictMsg(categories, outputs):
	#global petcount
	def TopTwo(categories, outputs):
		predicts = outputs / sum(outputs)
		predicts = predicts.tolist()
		predicts = [ round((x*100),2) for x in predicts ]
		categories = [ x.replace("guineapig", "guinea pig") for x in categories ]
		newpred, newcats = (list(x) for x in zip(*sorted(zip(predicts, categories), reverse=True)))
		return newcats[0:2], newpred[0:2]
	Twocats, TwoPred = TopTwo(categories, outputs)
	Topcat = Twocats[0]        #top category, most likely match
	Secondcat = Twocats[1]
	conf1 = TwoPred[0]
	conf2 = TwoPred[1]
	IsCapy = Topcat=="capybara"
	IsCapy2 = Secondcat=="capybara"
	IsPet = Topcat=="cat" or Topcat=="dog"
	mmsg = "Don't know."
	if IsCapy:
		if conf1>90:
			mmsg = "<b>It's a capybara!</b>  Confidence: " + str(conf1) + "%."
		elif conf1>70:
			mmsg = "<b>Might be a capybara.</b> Probability: " + str(conf1) + "%."
		else:
			mmsg = "Hard to tell. Capybara probability: " + str(conf1) + "%, " \
				+ Secondcat + " probability: " + str(conf2) + "%"
	else: #not capy
		if conf1>90:
			if IsPet:            # probably a cat or dog, show special messages
				settings.petcount +=1
				if settings.petcount == 1:   # first-time pet message
					if Topcat=="cat": mmsg="<b>NOT a capybara.</b> Looks more like a <b>catty-bara!</b> Confidence: " + str(conf1) + "%"
					else: mmsg="<b>Not a capybara.</b>  Looks more like a <b>doggy-bara!</b>  Confidence: " + str(conf1) + "%"
				elif settings.petcount == 2: #second-time pet message
					if Topcat=="cat":  mmsg= "Meow! That's a <b>cat</b>. Confidence: " + str(conf1) + "%"
					else: mmsg= "Woof! That's a <b>dog</b>. Confidence: " + str(conf1) + "%"
				else:               #regular message
					mmsg="<b>NOT a capybara</b>, looks like a <b>" + Topcat + "</b>, confidence: "+ str(conf1) + "%"	
			else:                    # regular message
				mmsg="<b>NOT a capybara</b>, looks like a <b>" + Topcat + "</b>, confidence: "+ str(conf1) + "%"	
		else:
			if IsCapy2:      # capy is still possible (it's second category)
				mmsg="Hard to tell. Looks like a <b>" + Topcat + "</b>, probability: " + str(conf1) + \
					"%, or maybe a <b>capybara</b>, probability: " + str(conf2) + "%"
			elif conf1>70:
				mmsg = "<b>NOT a capybara</b>.  Might be a <b>"+Topcat+"</b> (probability: " + str(conf1) + "%)."
			else:
				mmsg = "<b>NOT a capybara</b>.  Maybe a <b>"+Topcat+"</b> (probability " + str(conf1) + "%), or <b>" \
					+ Secondcat + "</b> (probability " + str(conf2) + "%)"
	return mmsg


