# AST FROM JSON, Pretty Printer
import json, pprint

# Fluent System
from fluent.runtime import FluentBundle
# from fluent.syntax import parse

# Custom Fluent AST Reader
import ast_handler as asth 

# Establish Pretty Print Object
pp = pprint.PrettyPrinter()

# Print strings in packet
def printTDev(packet):
	if 'zero' in packet:
		print('zero\t' + packet['zero'])

	if 'one' in packet:
		print('one\t' + packet['one'])

	if 'two' in packet:
		print('two\t' + packet['two'])

	if 'few' in packet:
		print('few\t' + packet['few'])

	if 'many' in packet:
		print('many\t' + packet['many'])

	if 'other' in packet:
		print('other\t' + packet['other'])

	print()

# Create Fluent bundle for composing Fluent objects
bundle = FluentBundle(["en-US"])

# Test String
emailTestString = """
unread-emails = { $unreadEmailsCount -> 
    [one] You have {$unreadEmailsCount} unread email.
   *[other] You have {$unreadEmailsCount} unread emails.	
}"""

print("FLUENT MESSAGE:" + emailTestString + "\n")

# Add String to bundle
bundle.add_messages(emailTestString)

# Add another test string straight to bundle
# bundle.add_messages("""
# shared-photos =
#     {$userName} {$photoCount ->
#         [one] added a new photo
#        *[other] added {$photoCount} new photos
#     } to {$userGender ->
#         [male] his stream
#         [female] her stream
#        *[other] their stream
#     }.""")

# Get compiled fluent message
# translated, errs = bundle.format('shared-photos')

# Plural example value
unreadEmailsCount = 11

# Compiled plurals example
translated, errs = bundle.format('unread-emails', 
	{"unreadEmailsCount": unreadEmailsCount})
print("RENDERED MESSAGE:\n" + translated + "\n")

# Testing AST of example
# ast = parse(emailTestString)
# pp.pprint(ast.to_json())

# Get ast of example
myAst = asth.getStruct(emailTestString)
# pp.pprint(myAst)

# pp.pprint(myAst['unread-emails'])

# for key in myAst.keys():
# 	print(key)
# 	pp.pprint(myAst[key]['delivery'])

print("TRANSLATION DELIVERIES:")

print('en')
printTDev(myAst['unread-emails']['delivery'])


# TODO
# Select target languages
# Pull target plural values
# Pair source plural strings with target plural strings (if no target, fill with other)


def fillTranslations(source, target):
	filledTranslations = {}

	for key in source.keys():
		# print(key)
		for pluralCategory in target:
		# for pluralCategory in source[key]['delivery'].keys():
			# print(pluralCategory)
			if pluralCategory in source[key]['delivery'].keys():
				filledTranslations[pluralCategory] = source[key]['delivery'][pluralCategory]
			else:
				filledTranslations[pluralCategory] = source[key]['delivery']['other']

	return filledTranslations

# GEt just plural categories from CLDR for specified language
def getPluralCats(pluralRules, lang):
	raw = pluralRules[lang]
	pluralCats = []

	for key in raw.keys():
		parts = key.split("-")
		cat = parts[-1]
		pluralCats.append(cat)

	return pluralCats




cldr_raw_data = json.loads(open("plurals.json").read())
pluralRules = cldr_raw_data["supplemental"]["plurals-type-cardinal"]
# pp.pprint(cldr_data["supplemental"]["plurals-type-cardinal"])


espr = getPluralCats(pluralRules, 'es')

zhpr = getPluralCats(pluralRules, 'zh')

plpr = getPluralCats(pluralRules, 'pl')

arpr = getPluralCats(pluralRules, 'ar')

# print('es')
# estdev = fillTranslations(myAst, espr)
# printTDev(estdev)

# print('zh')
# zhtdev = fillTranslations(myAst, zhpr)
# printTDev(zhtdev)

# print('pl')
# pltdev = fillTranslations(myAst, plpr)
# printTDev(pltdev)

print('ar')
artdev = fillTranslations(myAst, arpr)
printTDev(artdev)


#TODO
# Wrap new messages in ftl format

def composeFTLMessage(messageData, translatedPacket):
	ftlMessage = "unread-emails = "

	variant = messageData['variables'][0]

	ftlMessage += '{ $' + variant + " -> "

	if 'zero' in translatedPacket:
		ftlMessage += '\n    [zero] ' + translatedPacket['zero']

	if 'one' in translatedPacket:
		ftlMessage += '\n    [one] ' + translatedPacket['one']

	if 'two' in translatedPacket:
		ftlMessage += '\n    [two] ' + translatedPacket['two']

	if 'few' in translatedPacket:
		ftlMessage += '\n    [few] ' + translatedPacket['few']

	if 'many' in translatedPacket:
		ftlMessage += '\n    [many] ' + translatedPacket['many']

	if 'other' in translatedPacket:
		ftlMessage += '\n   *[other] ' + translatedPacket['other']

	ftlMessage += "\n}"


	return ftlMessage


final = composeFTLMessage(myAst['unread-emails'], artdev)


print(final + "\n")


newEmailMessage = """
unread-emails = { $unreadEmailsCount -> 
    [zero] (ZERO) You have $unreadEmailsCount unread emails.
    [one] (ONE) You have $unreadEmailsCount unread email.
    [two] (TWO) You have $unreadEmailsCount unread emails.
    [few] (FEW) You have $unreadEmailsCount unread emails.
    [many] (MANY) You have $unreadEmailsCount unread emails.
   *[other] (OTHER) You have $unreadEmailsCount unread emails.
}"""

# Plural example value
unreadEmailsCount = 101

newBundle = FluentBundle(["ar-AE"])
newBundle.add_messages(newEmailMessage)

# Compiled plurals example
translated, errs = newBundle.format('unread-emails', 
	{"unreadEmailsCount": unreadEmailsCount})
print("RENDERED MESSAGE:\n" + translated + "\n")


