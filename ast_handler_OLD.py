from fluent.runtime import FluentBundle

import fluent.syntax as fs

import pprint, json


def main():
	# resource = open("abtest.ftl").read()
	resource = open("sample_en.ftl").read()

	pp = pprint.PrettyPrinter(indent=0)
	pp.pprint(getStruct(resource))

def getStruct(resource):
	pp = pprint.PrettyPrinter(indent=0)

	bundle = FluentBundle(["en-US"])
	bundle.add_messages(resource)
	parser = fs.FluentParser()
	resource = parser.parse(resource)

	thing = fs.ast.to_json(resource)



	# json.loads(thing)
	# pp.pprint(thing)
	# pp.pprint(thing['body'])

	template_data = {}


	for m in thing['body']:
		if 'id' in m:
			# print(m['id']['name'])
			template_id = m['id']['name']
			# pp.pprint(m['value']['elements'])

			new_entry = indvPieces(m, pp)

			template_data[template_id] = new_entry

	# print("FIRST OUTPUT")
	# pp.pprint(template_data)


	for k in template_data.keys():
		# print(k)
		passedVars = passUpVars(template_data, k)

		for v in passedVars:
			if v not in template_data[k]['variables']:
				template_data[k]['variables'].append(v)

		passedVariants = passUpVariants(template_data, k)

		for v in passedVariants.keys():
			if v not in template_data[k]['variants']:
				template_data[k]['variants'][v] = passedVariants[v]

	# print("SECOND OUTPUT")
	# pp.pprint(template_data)

	return template_data



def indvPieces(items, pp):

	template_entry = {
		'variables': [],
		'references': [],
		'variants': {}
	}

	for item in items['value']['elements']:
		# print(item['type'])
			
			
		# if item['type'] == 'TextElement':
		# 	print("\'" + item['value'] + "\'")

		if item['type'] == 'Placeable':
			if item['expression']['type'] == 'VariableReference':
				# print(item['expression']['type'])
				# print("{$" + item['expression']['id']['name'] + "}")
				template_entry['variables'].append(item['expression']['id']['name'])

			elif item['expression']['type'] == 'MessageReference':
				# print(item['expression']['type'])
				# print(item['expression']['id']['name'])
				template_entry['references'].append(item['expression']['id']['name'])

			elif item['expression']['type'] == 'SelectExpression':
				# print(item['expression']['type'])
				# print("$" + item['expression']['selector']['id']['name'])
				if item['expression']['selector']['id']['name'] not in template_entry['variants']:
					template_entry['variants'][item['expression']['selector']['id']['name']] = []
				else:
					"variant variable already in dictionary"

				for variant in item['expression']['variants']:
					# print("Key")
					# print(variant['key']['name'])
					template_entry['variants'][item['expression']['selector']['id']['name']].append(variant['key']['name'])
					# pp.pprint(variant)
					variant_data = indvPieces(variant, pp)

					# print("VARIANT_DATA")
					# pp.pprint(variant_data)

					for variable in variant_data['variables']:
						# print("ITERATIVE VARIABLES:",variable)
						if variable not in template_entry['variables']:
							template_entry['variables'].append(variable)
					for reference in variant_data['references']:
						# print("ITERATIVE VARIABLES:", reference)
						if reference not in template_entry['references']:
							template_entry['references'].append(reference)

			else:
				print("something wrong")

	return template_entry


def passUpVars(data, r):
	my_vars = []

	# print(r)

	for ref in data[r]['references']:
		temp_vars = passUpVars(data, ref)
		for var in temp_vars:
			if var not in my_vars:
				my_vars.append(var)

	for var in data[r]['variables']:
		if var not in my_vars:
			my_vars.append(var)

	return my_vars


def passUpVariants(data, r):
	my_vars = {}

	for ref in data[r]['references']:

		temp_vars = passUpVariants(data, ref)
		for vnt in temp_vars.keys():
			if vnt not in my_vars:
				my_vars[vnt] = temp_vars[vnt]
			else:
				for key in temp_vars[vnt]:
					if key not in my_vars[vnt]:
						my_vars[vnt].append(key)

	for key in data[r]['variants'].keys():
		if key not in my_vars:
			my_vars[key] = data[r]['variants'][key]

	return my_vars




if __name__ == '__main__':
	main()