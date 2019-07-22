
# Automatically generated unittests for grammar

import unittest
import coloredlogs
coloredlogs.install()
import logging
logging.getLogger().setLevel(logging.INFO)        

def test_rule (text, match_dict, rule):

    logging.info("testing 'rule_%s'" % rule)
    import pprint

    from token_parsing import prepare_text, prepare_labels
    from probsyntgreed_parsing import probsyntgreed_parser

    tokens = prepare_text(text)
    match_dict = prepare_labels([match_dict])

    parser = probsyntgreed_parser()
    solution = parser.match(tokens=tokens, match_dict=match_dict, rule=rule)

    if rule == 'differential_sentence':
        solution = parser.best_of(solution[0])

    logging.info("\n" + text)
    logging.info("\n" + pprint.pformat(solution, indent=4))

    return solution
    
class TestGrammar(unittest.TestCase):

	# good annotation
	def testPsychologistSocialWorker0(self):		
		text = """While a psychologist will only incorporate knowledge from clinical psychology, a social worker will implement theories and information from several areas, including sociology, psychology, law, economics, political sciences, etc...
While a psychologist is required to have a Ph.D. or a doctorate, a social worker can become a professional with bachelor’s or master’s degree.
The pay rates varies depending on the areas of work, area of specialization and number of years of experience.  Social worker’s salary varies anywhere from USD $ 40,000- 70,000 whereas psychologist earn anywhere from USD  $50,000- 110,000.
While a social worker will focus on “outward” problems, such job, housing, living condition, and medical care. A psychologist will focus on the mental and emotional issues that a client might have."""
		match_dict = (   {   'aspect': None,
        'contrast': [   'implements',
                        'knowledge',
                        'and',
                        'information',
                        'from',
                        'clinical',
                        'psychology',
                        'in',
                        'order',
                        'to',
                        'help',
                        'the',
                        'client',
                        ','],
        'subject': ['Psychologist']},
    {   'aspect': None,
        'contrast': [   'incorporates',
                        'knowledge',
                        'and',
                        'information',
                        'from',
                        'psychology',
                        ',',
                        'sociology',
                        ',',
                        'law',
                        ',',
                        'economics',
                        ',',
                        'political',
                        'sciences',
                        ',',
                        'and',
                        'other',
                        'areas',
                        'in',
                        'order',
                        'to',
                        'help',
                        'the',
                        'client',
                        ','],
        'subject': ['Social', 'Worker']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testPsychologistSocialWorker1(self):		
		text = """While a psychologist will only incorporate knowledge from clinical psychology, a social worker will implement theories and information from several areas, including sociology, psychology, law, economics, political sciences, etc...
While a psychologist is required to have a Ph.D. or a doctorate, a social worker can become a professional with bachelor’s or master’s degree.
The pay rates varies depending on the areas of work, area of specialization and number of years of experience.  Social worker’s salary varies anywhere from USD $ 40,000- 70,000 whereas psychologist earn anywhere from USD  $50,000- 110,000.
While a social worker will focus on “outward” problems, such job, housing, living condition, and medical care. A psychologist will focus on the mental and emotional issues that a client might have."""
		match_dict = (   {   'aspect': None,
        'contrast': [   'has',
                        'a',
                        'ph',
                        ',',
                        'd',
                        ',',
                        'or',
                        'a',
                        'doctorate',
                        ',',
                        'and',
                        'at',
                        'least',
                        'one',
                        'year',
                        'of',
                        'experience'],
        'subject': ['Psychologist']},
    {   'aspect': None,
        'contrast': [   'has',
                        'a',
                        'bachelor',
                        '’s',
                        'or',
                        'master',
                        '’s',
                        'degree'],
        'subject': ['Social', 'Worker']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# annotation is not safe enough
	def testPsychologistSocialWorker2(self):		
		text = """While a psychologist will only incorporate knowledge from clinical psychology, a social worker will implement theories and information from several areas, including sociology, psychology, law, economics, political sciences, etc...
While a psychologist is required to have a Ph.D. or a doctorate, a social worker can become a professional with bachelor’s or master’s degree.
The pay rates varies depending on the areas of work, area of specialization and number of years of experience.  Social worker’s salary varies anywhere from USD $ 40,000- 70,000 whereas psychologist earn anywhere from USD  $50,000- 110,000.
While a social worker will focus on “outward” problems, such job, housing, living condition, and medical care. A psychologist will focus on the mental and emotional issues that a client might have."""
		match_dict = (   {   'aspect': None,
        'contrast': [   'pay',
                        'rates',
                        'range',
                        'between',
                        '$',
                        '50,000',
                        '110,000'],
        'subject': ['Psychologist']},
    {   'aspect': None,
        'contrast': [   'pay',
                        'rates',
                        'range',
                        'between',
                        '$',
                        '$',
                        '40,000',
                        '70,000'],
        'subject': ['Social', 'Worker']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testPsychologistSocialWorker3(self):		
		text = """While a psychologist will only incorporate knowledge from clinical psychology, a social worker will implement theories and information from several areas, including sociology, psychology, law, economics, political sciences, etc...
While a psychologist is required to have a Ph.D. or a doctorate, a social worker can become a professional with bachelor’s or master’s degree.
The pay rates varies depending on the areas of work, area of specialization and number of years of experience.  Social worker’s salary varies anywhere from USD $ 40,000- 70,000 whereas psychologist earn anywhere from USD  $50,000- 110,000.
While a social worker will focus on “outward” problems, such job, housing, living condition, and medical care. A psychologist will focus on the mental and emotional issues that a client might have."""
		match_dict = (   {   'aspect': None,
        'contrast': [   'focuses',
                        'on',
                        'the',
                        '“',
                        'inner',
                        '”',
                        'side',
                        'of',
                        'the',
                        'client',
                        '–',
                        'emotions',
                        'and',
                        'subconscious'],
        'subject': ['Psychologist']},
    {   'aspect': None,
        'contrast': [   'focuses',
                        'on',
                        'the',
                        '“',
                        'outer',
                        '”',
                        'side',
                        'of',
                        'the',
                        'client',
                        '–',
                        'communication',
                        ',',
                        'career',
                        'planning',
                        ',',
                        'job',
                        ',',
                        'housing',
                        ',',
                        'family',
                        'support',
                        'and',
                        'etc',
                        '…'],
        'subject': ['Social', 'Worker']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		

	# good annotation
	def testNeedlepointEmbroidery0(self):		
		text = """While needlepoint designs are created with tapestry wool which is stitched on a mesh canvas, embroidery uses floss to create a picture or a design.
While the canvas used in needlepoint may either be pre-printed or pained with the preferred design or remain blank, embroidery involves pre-printed the desired design and stitching over the lines, hence filling the spaces.
The most commonly used fabric in needlepoint is open weave canvas while embroidery uses fabrics such as satin, silk, cotton, Aida, and velvet.
While the concept used in needlepoint is stitching over the design area and covering it with yarn or thread, embroidery involves stitching over the lines and filling in the shapes.
While needlepoint is stitched by hand, embroidery can either be done by hand or machinery.
"""
		match_dict = (   {   'aspect': ['design', 'creation'],
        'contrast': [   'designs',
                        'are',
                        'created',
                        'with',
                        'tapestry',
                        'wool',
                        'which',
                        'is',
                        'stitched',
                        'on',
                        'a',
                        'mesh',
                        'canvas'],
        'subject': ['Needlepoint']},
    {   'aspect': ['design', 'creation'],
        'contrast': [   'uses',
                        'floss',
                        'to',
                        'create',
                        'a',
                        'picture',
                        'or',
                        'a',
                        'design'],
        'subject': ['Embroidery']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testNeedlepointEmbroidery1(self):		
		text = """While needlepoint designs are created with tapestry wool which is stitched on a mesh canvas, embroidery uses floss to create a picture or a design.
While the canvas used in needlepoint may either be pre-printed or pained with the preferred design or remain blank, embroidery involves pre-printed the desired design and stitching over the lines, hence filling the spaces.
The most commonly used fabric in needlepoint is open weave canvas while embroidery uses fabrics such as satin, silk, cotton, Aida, and velvet.
While the concept used in needlepoint is stitching over the design area and covering it with yarn or thread, embroidery involves stitching over the lines and filling in the shapes.
While needlepoint is stitched by hand, embroidery can either be done by hand or machinery.
"""
		match_dict = (   {   'aspect': ['predesign', 'painting'],
        'contrast': [   'the',
                        'canvas',
                        'used',
                        'may',
                        'either',
                        'be',
                        'preprinted',
                        'or',
                        'pained',
                        'with',
                        'the',
                        'preferred',
                        'design',
                        'or',
                        'remain',
                        'blank'],
        'subject': ['Needlepoint']},
    {   'aspect': ['predesign', 'painting'],
        'contrast': [   'involves',
                        'preprinted',
                        'the',
                        'desired',
                        'design',
                        'and',
                        'stitching',
                        'over',
                        'the',
                        'lines',
                        ',',
                        'hence',
                        'filling',
                        'the',
                        'spaces',
                        ','],
        'subject': ['Embroidery']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testNeedlepointEmbroidery2(self):		
		text = """While needlepoint designs are created with tapestry wool which is stitched on a mesh canvas, embroidery uses floss to create a picture or a design.
While the canvas used in needlepoint may either be pre-printed or pained with the preferred design or remain blank, embroidery involves pre-printed the desired design and stitching over the lines, hence filling the spaces.
The most commonly used fabric in needlepoint is open weave canvas while embroidery uses fabrics such as satin, silk, cotton, Aida, and velvet.
While the concept used in needlepoint is stitching over the design area and covering it with yarn or thread, embroidery involves stitching over the lines and filling in the shapes.
While needlepoint is stitched by hand, embroidery can either be done by hand or machinery.
"""
		match_dict = (   {   'aspect': ['fabric', 'used'],
        'contrast': [   'the',
                        'most',
                        'commonly',
                        'used',
                        'fabric',
                        'is',
                        'open',
                        'weave',
                        'canvas'],
        'subject': ['Needlepoint']},
    {   'aspect': ['fabric', 'used'],
        'contrast': [   'uses',
                        'fabrics',
                        'such',
                        'as',
                        'satin',
                        ',',
                        'silk',
                        ',',
                        'cotton',
                        ',',
                        'aida',
                        ',',
                        'and',
                        'velvet',
                        ','],
        'subject': ['Embroidery']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testNeedlepointEmbroidery3(self):		
		text = """While needlepoint designs are created with tapestry wool which is stitched on a mesh canvas, embroidery uses floss to create a picture or a design.
While the canvas used in needlepoint may either be pre-printed or pained with the preferred design or remain blank, embroidery involves pre-printed the desired design and stitching over the lines, hence filling the spaces.
The most commonly used fabric in needlepoint is open weave canvas while embroidery uses fabrics such as satin, silk, cotton, Aida, and velvet.
While the concept used in needlepoint is stitching over the design area and covering it with yarn or thread, embroidery involves stitching over the lines and filling in the shapes.
While needlepoint is stitched by hand, embroidery can either be done by hand or machinery.
"""
		match_dict = (   {   'aspect': ['technique'],
        'contrast': [   'the',
                        'concept',
                        'used',
                        'is',
                        'stitching',
                        'over',
                        'the',
                        'design',
                        'area',
                        'and',
                        'covering',
                        'it',
                        'with',
                        'yarn',
                        'or',
                        'thread'],
        'subject': ['Needlepoint']},
    {   'aspect': ['technique'],
        'contrast': [   'involves',
                        'stitching',
                        'over',
                        'the',
                        'lines',
                        'and',
                        'filling',
                        'in',
                        'the',
                        'shapes'],
        'subject': ['Embroidery']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testNeedlepointEmbroidery4(self):		
		text = """While needlepoint designs are created with tapestry wool which is stitched on a mesh canvas, embroidery uses floss to create a picture or a design.
While the canvas used in needlepoint may either be pre-printed or pained with the preferred design or remain blank, embroidery involves pre-printed the desired design and stitching over the lines, hence filling the spaces.
The most commonly used fabric in needlepoint is open weave canvas while embroidery uses fabrics such as satin, silk, cotton, Aida, and velvet.
While the concept used in needlepoint is stitching over the design area and covering it with yarn or thread, embroidery involves stitching over the lines and filling in the shapes.
While needlepoint is stitched by hand, embroidery can either be done by hand or machinery.
"""
		match_dict = (   {   'aspect': ['mode', 'of', 'stitching'],
        'contrast': ['is', 'stitched', 'by', 'hand'],
        'subject': ['Needlepoint']},
    {   'aspect': ['mode', 'of', 'stitching'],
        'contrast': [   'can',
                        'either',
                        'be',
                        'done',
                        'by',
                        'hand',
                        'or',
                        'machinery',
                        'difference',
                        'da]ifterence'],
        'subject': ['Embroidery']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		

	# good annotation
	def testMicronutrientsMacronutrients0(self):		
		text = """Macronutrients are required in large quantities to ensure optimum health and body performance. These are usually found in large quantities in different types of food hence the reason why they are also required in large quantities.
In contrast, micronutrients are usually required in small quantities in human bodies. They often exist in small quantities in different types of food."""
		match_dict = (   {   'aspect': None,
        'contrast': ['required', 'in', 'large', 'quantities'],
        'subject': ['Micronutrients']},
    {   'aspect': None,
        'contrast': ['required', 'in', 'small', 'quantities'],
        'subject': ['Macronutrients']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testMicronutrientsMacronutrients1(self):		
		text = """Macronutrients are required in large quantities to ensure optimum health and body performance. These are usually found in large quantities in different types of food hence the reason why they are also required in large quantities.
In contrast, micronutrients are usually required in small quantities in human bodies. They often exist in small quantities in different types of food."""
		match_dict = (   {   'aspect': None,
        'contrast': ['provide', 'body', 'with', 'energy'],
        'subject': ['Micronutrients']},
    {   'aspect': None,
        'contrast': [   'play',
                        'a',
                        'pivotal',
                        'role',
                        'in',
                        'disease',
                        'prevention'],
        'subject': ['Macronutrients']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testMicronutrientsMacronutrients2(self):		
		text = """Macronutrients are required in large quantities to ensure optimum health and body performance. These are usually found in large quantities in different types of food hence the reason why they are also required in large quantities.
In contrast, micronutrients are usually required in small quantities in human bodies. They often exist in small quantities in different types of food."""
		match_dict = (   {   'aspect': None,
        'contrast': [   'examples',
                        'of',
                        'micronutrients',
                        'include',
                        'proteins',
                        ',',
                        'carbohydrates',
                        'and',
                        'fats'],
        'subject': ['Micronutrients']},
    {   'aspect': None,
        'contrast': [   'examples',
                        'of',
                        'micronutrients',
                        'include',
                        'minerals',
                        'and',
                        'vitamins'],
        'subject': ['Macronutrients']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testMicronutrientsMacronutrients3(self):		
		text = """Macronutrients are required in large quantities to ensure optimum health and body performance. These are usually found in large quantities in different types of food hence the reason why they are also required in large quantities.
In contrast, micronutrients are usually required in small quantities in human bodies. They often exist in small quantities in different types of food."""
		match_dict = (   {   'aspect': None,
        'contrast': [   'excessive',
                        'consumption',
                        'of',
                        'macronutrients',
                        'lead',
                        'to',
                        'obesity',
                        'and',
                        'diabetes'],
        'subject': ['Micronutrients']},
    {   'aspect': None,
        'contrast': [   'the',
                        'is',
                        'no',
                        'data',
                        'that',
                        'shows',
                        'the',
                        'impact',
                        'of',
                        'excessive',
                        'consumption',
                        'of',
                        'micronutrients'],
        'subject': ['Macronutrients']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testMicronutrientsMacronutrients4(self):		
		text = """Macronutrients are required in large quantities to ensure optimum health and body performance. These are usually found in large quantities in different types of food hence the reason why they are also required in large quantities.
In contrast, micronutrients are usually required in small quantities in human bodies. They often exist in small quantities in different types of food."""
		match_dict = (   {   'aspect': None,
        'contrast': [   'macronutrients',
                        'are',
                        'mainly',
                        'obtained',
                        'from',
                        'the',
                        'following',
                        'foods',
                        ':',
                        'potatoes',
                        ',',
                        'cereals',
                        ',',
                        'fish',
                        'as',
                        'well',
                        'as',
                        'nuts',
                        'among',
                        'others'],
        'subject': ['Micronutrients']},
    {   'aspect': None,
        'contrast': [   'micronutrients',
                        'are',
                        'mainly',
                        'obtained',
                        'from',
                        'vegetables',
                        ',',
                        'fruits',
                        'as',
                        'well',
                        'as',
                        'eggs'],
        'subject': ['Macronutrients']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		

	# annotation spans more than two sentences
	def testCarbonTaxAndCapTrade0(self):		
		text = """Revenue vs environment:    While both carbon tax and cap-and-trade system aim at reducing greenhouse emissions, they use a different approach and yield slightly different results. In the case of the carbon tax, there is a fixed revenue – as firms are expected to pay the tax on each unit of emissions – while the level of pollution is determined by market forces as there is no actual limit on emissions. Conversely, in the case of a cap-and-trade system, a limited on emissions is imposed by the government, but there is no fixed revenue as the price of permits and quotas is determined by market fundamentals (supply and demand); and
 Role of the firm:   In both cases, firms and households enjoy a certain flexibility. In the case of the carbon tax, firms can decide how much they are willing to pay and reduce or regulate their emissions accordingly. Some firms may decide that paying a carbon tax is economically more convenient than reducing emissions, while – in the case of a cap-and-trade system – firms may decide to trade the majority of their quotas or to take advantage of market trends to get higher returns for their unused emissions’ permits.
The impact of the carbon tax and cap-and-trade on a country’s economy is significant. At the same time, the economy’s performance affects the way in which firms comply with their obligations. The carbon tax and the cap-and-trade system cannot be understood without analyzing them within a broader context and without evaluating their success rate.
"""
		match_dict = (   {   'aspect': ['economic', 'context'],
        'contrast': [   'the',
                        'carbon',
                        'tax',
                        'is',
                        'not',
                        'selfadjusting',
                        'and',
                        'needs',
                        'to',
                        'be',
                        'raised',
                        'or',
                        'reduced',
                        'by',
                        'the',
                        'government',
                        'following',
                        'the',
                        'economy',
                        ''s',
                        'trend',
                        ',',
                        'this',
                        'means',
                        'that',
                        'authorities',
                        'need',
                        'to',
                        'monitor',
                        'the',
                        'tax',
                        '’s',
                        'level',
                        'at',
                        'all',
                        'times',
                        'and',
                        'make',
                        'sure',
                        'to',
                        'implement',
                        'the',
                        'necessary',
                        'adjustments',
                        'not',
                        'only',
                        'to',
                        'maximize',
                        'revenue',
                        'but',
                        'also',
                        'to',
                        'ensure',
                        'economic',
                        'prosperity',
                        'in',
                        'the',
                        'country',
                        ',',
                        'without',
                        'causing',
                        'an',
                        'excessive',
                        'burden',
                        'on',
                        'suffering',
                        'economies',
                        ','],
        'subject': ['Carbon', 'Tax', 'And', 'Cap']},
    {   'aspect': ['economic', 'context'],
        'contrast': [   'in',
                        'a',
                        'capandtrade',
                        'system',
                        ',',
                        'the',
                        'price',
                        'of',
                        'quotasis',
                        'selfadjusting',
                        ',',
                        'the',
                        'price',
                        'of',
                        'permits',
                        'depends',
                        'on',
                        'the',
                        'demand',
                        'and',
                        'supply',
                        'balance',
                        ',',
                        'this',
                        'means',
                        'that',
                        'when',
                        'the',
                        'economy',
                        'is',
                        'performing',
                        'well',
                        'and',
                        'thereisa',
                        'limited',
                        'supply',
                        'of',
                        'quotas',
                        ',',
                        'their',
                        'price',
                        'is',
                        'likely',
                        'to',
                        'grow',
                        'sharply',
                        ',',
                        'while',
                        'when',
                        'the',
                        'economy',
                        'is',
                        'underperforming',
                        'and',
                        'availability',
                        'is',
                        'abundant',
                        ',',
                        'prices',
                        'are',
                        'likely',
                        'to',
                        'drop',
                        ','],
        'subject': ['Trade']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# annotation spans more than two sentences
	def testCarbonTaxAndCapTrade1(self):		
		text = """Revenue vs environment:    While both carbon tax and cap-and-trade system aim at reducing greenhouse emissions, they use a different approach and yield slightly different results. In the case of the carbon tax, there is a fixed revenue – as firms are expected to pay the tax on each unit of emissions – while the level of pollution is determined by market forces as there is no actual limit on emissions. Conversely, in the case of a cap-and-trade system, a limited on emissions is imposed by the government, but there is no fixed revenue as the price of permits and quotas is determined by market fundamentals (supply and demand); and
 Role of the firm:   In both cases, firms and households enjoy a certain flexibility. In the case of the carbon tax, firms can decide how much they are willing to pay and reduce or regulate their emissions accordingly. Some firms may decide that paying a carbon tax is economically more convenient than reducing emissions, while – in the case of a cap-and-trade system – firms may decide to trade the majority of their quotas or to take advantage of market trends to get higher returns for their unused emissions’ permits.
The impact of the carbon tax and cap-and-trade on a country’s economy is significant. At the same time, the economy’s performance affects the way in which firms comply with their obligations. The carbon tax and the cap-and-trade system cannot be understood without analyzing them within a broader context and without evaluating their success rate.
"""
		match_dict = (   {   'aspect': ['success', 'rate'],
        'contrast': [   'the',
                        'carbon',
                        'tax',
                        'has',
                        'been',
                        'used',
                        'ina',
                        'number',
                        'of',
                        'countries',
                        'and',
                        'has',
                        'had',
                        'positive',
                        'outcomes',
                        'in',
                        'most',
                        'cases',
                        ',',
                        'one',
                        'of',
                        'the',
                        'most',
                        'notable',
                        'examples',
                        'is',
                        'sweden',
                        ',',
                        'the',
                        'tax',
                        'was',
                        'introduces',
                        'in',
                        'the',
                        'country',
                        'in',
                        '1991',
                        'and',
                        'led',
                        'to',
                        'an',
                        'approximately',
                        '20pc',
                        'drop',
                        'in',
                        'pollution',
                        ',',
                        'although',
                        'other',
                        'policies',
                        'were',
                        'already',
                        'in',
                        'place',
                        ',',
                        'the',
                        'tax',
                        'was',
                        'also',
                        'used',
                        'for',
                        'a',
                        'brief',
                        'period',
                        'in',
                        'local',
                        'governments',
                        'in',
                        'the',
                        'united',
                        'states',
                        'and',
                        'canada',
                        ','],
        'subject': ['Carbon', 'Tax', 'And', 'Cap']},
    {   'aspect': ['success', 'rate'],
        'contrast': [   'the',
                        'capandtrade',
                        'system',
                        'has',
                        'been',
                        'adopted',
                        'successfully',
                        'by',
                        'a',
                        'number',
                        'of',
                        'countries',
                        ',',
                        'including',
                        'the',
                        'world',
                        ''s',
                        'major',
                        'polluters',
                        ',',
                        'the',
                        'system',
                        'is',
                        'being',
                        'used',
                        'in',
                        'the',
                        'united',
                        'states',
                        ',',
                        'in',
                        'the',
                        'european',
                        'union',
                        '(',
                        'since',
                        '2005',
                        ')',
                        'and',
                        'in',
                        'tokyo',
                        '(',
                        'since',
                        '2010',
                        ')',
                        ',',
                        'pa|ditterence',
                        'between',
                        ',',
                        'net'],
        'subject': ['Trade']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		

	# annotation spans more than two sentences
	def testAnointingHolySpirit0(self):		
		text = """The term anointing means smearing or applying oil on an individual’s head or body usually to mark a religious ceremony or belief. To be anointed by the Holy Spirit means sanctifying the individual’s ways to be in line with the teachings of Jesus Christ and the ways of the Holy Spirit.
Holy Spirit, on the other hand, means an individual that makes up the Holy Trinity. This means the third part used to refer to God’s Trinity, that is Father, the Son, and the Holy Spirit.
Anointing is a verb where an individual gets anointment oil applied on their head or body while Holy Spirit is a proper noun referring to one of the parts representing the Holy Trinity.
Also, anointing is exclusive while the Holy Spirit is inclusive.
"""
		match_dict = (   {   'aspect': ['meaning'],
        'contrast': [   'anointing',
                        'means',
                        'smearing',
                        'oilon',
                        'a',
                        'person',
                        'body',
                        'to',
                        'mark',
                        'a',
                        'religious',
                        'belief',
                        ',',
                        'it',
                        'also',
                        'means',
                        'being',
                        'sanctified',
                        'by',
                        'the',
                        'holy',
                        'spirit',
                        'to',
                        'live',
                        'in',
                        'the',
                        'ways',
                        'of',
                        'the',
                        'holy',
                        'spirit'],
        'subject': ['Anointing']},
    {   'aspect': ['meaning'],
        'contrast': [   'one',
                        'of',
                        'the',
                        'parts',
                        'making',
                        'up',
                        'the',
                        'trinity',
                        '(',
                        'the',
                        'father',
                        ',',
                        'son',
                        ',',
                        'holy',
                        'spirit',
                        ')'],
        'subject': ['Holy', 'Spirit']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# annotation missing a side
	def testAnointingHolySpirit1(self):		
		text = """The term anointing means smearing or applying oil on an individual’s head or body usually to mark a religious ceremony or belief. To be anointed by the Holy Spirit means sanctifying the individual’s ways to be in line with the teachings of Jesus Christ and the ways of the Holy Spirit.
Holy Spirit, on the other hand, means an individual that makes up the Holy Trinity. This means the third part used to refer to God’s Trinity, that is Father, the Son, and the Holy Spirit.
Anointing is a verb where an individual gets anointment oil applied on their head or body while Holy Spirit is a proper noun referring to one of the parts representing the Holy Trinity.
Also, anointing is exclusive while the Holy Spirit is inclusive.
"""
		match_dict = (   {   'aspect': ['nature'],
        'contrast': [   'averb',
                        'referring',
                        'to',
                        'the',
                        'process',
                        'of',
                        'getting',
                        'someone',
                        'to',
                        'follow',
                        'the',
                        'ways',
                        'of',
                        'cod',
                        'through',
                        'the',
                        'holy',
                        'spirit',
                        '+',
                        'anointing',
                        'is',
                        'also',
                        'exclusive'],
        'subject': ['Anointing']},
    {   'aspect': ['nature'],
        'contrast': [   '+',
                        'a',
                        'person',
                        'making',
                        'the',
                        'holy',
                        'trinity',
                        '+',
                        'holy',
                        'spirit',
                        'is',
                        'also',
                        'inclusive',
                        'pa|difference',
                        'between',
                        ',',
                        'net'],
        'subject': ['Holy', 'Spirit']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		

	# good annotation
	def testThemeTopic0(self):		
		text = """A theme is the main messaged passed on through writing while a topic is the major subject explained in writing.
A theme explains the trail of thoughts while a topic explains characters
A theme clarifies why a certain script has been written while a topic explains what the script is all about.
A theme is not clearly described in the piece of writing but a topic is written at the beginning of every piece of writing
A theme reflects opinion while a topic reflects the subject matter
A theme is general while a topic is very specific
A theme is not stated; it is implied, while a topic is clearly stated. On very few occasions, will writers state the themes.
"""
		match_dict = (   {   'aspect': ['definition'],
        'contrast': ['main', 'message', 'passed', 'on', 'through', 'writing'],
        'subject': ['Theme']},
    {   'aspect': ['definition'],
        'contrast': ['major', 'subject', 'explained', 'in', 'writing'],
        'subject': ['Topic']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testThemeTopic1(self):		
		text = """A theme is the main messaged passed on through writing while a topic is the major subject explained in writing.
A theme explains the trail of thoughts while a topic explains characters
A theme clarifies why a certain script has been written while a topic explains what the script is all about.
A theme is not clearly described in the piece of writing but a topic is written at the beginning of every piece of writing
A theme reflects opinion while a topic reflects the subject matter
A theme is general while a topic is very specific
A theme is not stated; it is implied, while a topic is clearly stated. On very few occasions, will writers state the themes.
"""
		match_dict = (   {   'aspect': ['explanation'],
        'contrast': ['explains', 'trail', 'of', 'thoughts'],
        'subject': ['Theme']},
    {   'aspect': ['explanation'],
        'contrast': ['explains', 'characters'],
        'subject': ['Topic']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testThemeTopic2(self):		
		text = """A theme is the main messaged passed on through writing while a topic is the major subject explained in writing.
A theme explains the trail of thoughts while a topic explains characters
A theme clarifies why a certain script has been written while a topic explains what the script is all about.
A theme is not clearly described in the piece of writing but a topic is written at the beginning of every piece of writing
A theme reflects opinion while a topic reflects the subject matter
A theme is general while a topic is very specific
A theme is not stated; it is implied, while a topic is clearly stated. On very few occasions, will writers state the themes.
"""
		match_dict = (   {   'aspect': ['description'],
        'contrast': [   'clarifies',
                        'why',
                        'a',
                        'certain',
                        'seript',
                        'has',
                        'been',
                        'written'],
        'subject': ['Theme']},
    {   'aspect': ['description'],
        'contrast': ['describes', 'what', 'the', 'seript', 'is', 'about'],
        'subject': ['Topic']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testThemeTopic3(self):		
		text = """A theme is the main messaged passed on through writing while a topic is the major subject explained in writing.
A theme explains the trail of thoughts while a topic explains characters
A theme clarifies why a certain script has been written while a topic explains what the script is all about.
A theme is not clearly described in the piece of writing but a topic is written at the beginning of every piece of writing
A theme reflects opinion while a topic reflects the subject matter
A theme is general while a topic is very specific
A theme is not stated; it is implied, while a topic is clearly stated. On very few occasions, will writers state the themes.
"""
		match_dict = (   {   'aspect': ['identification', 'specificity'],
        'contrast': [   'not',
                        'clearly',
                        'described',
                        'in',
                        'a',
                        'piece',
                        'of',
                        'writing',
                        'reflects',
                        'opinion'],
        'subject': ['Theme']},
    {   'aspect': ['identification', 'specificity'],
        'contrast': [   'written',
                        'at',
                        'the',
                        'beginning',
                        'of',
                        'every',
                        'script',
                        'explains',
                        'the',
                        'subject',
                        'matter'],
        'subject': ['Topic']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testThemeTopic4(self):		
		text = """A theme is the main messaged passed on through writing while a topic is the major subject explained in writing.
A theme explains the trail of thoughts while a topic explains characters
A theme clarifies why a certain script has been written while a topic explains what the script is all about.
A theme is not clearly described in the piece of writing but a topic is written at the beginning of every piece of writing
A theme reflects opinion while a topic reflects the subject matter
A theme is general while a topic is very specific
A theme is not stated; it is implied, while a topic is clearly stated. On very few occasions, will writers state the themes.
"""
		match_dict = (   {'aspect': ['scope'], 'contrast': ['general'], 'subject': ['Theme']},
    {'aspect': ['scope'], 'contrast': ['specific'], 'subject': ['Topic']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testThemeTopic5(self):		
		text = """A theme is the main messaged passed on through writing while a topic is the major subject explained in writing.
A theme explains the trail of thoughts while a topic explains characters
A theme clarifies why a certain script has been written while a topic explains what the script is all about.
A theme is not clearly described in the piece of writing but a topic is written at the beginning of every piece of writing
A theme reflects opinion while a topic reflects the subject matter
A theme is general while a topic is very specific
A theme is not stated; it is implied, while a topic is clearly stated. On very few occasions, will writers state the themes.
"""
		match_dict = (   {'aspect': ['conveyance'], 'contrast': ['implied'], 'subject': ['Theme']},
    {   'aspect': ['conveyance'],
        'contrast': [   'clearly',
                        'stated',
                        '[',
                        'daditference',
                        'between',
                        ',',
                        'net'],
        'subject': ['Topic']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		

	# good annotation
	def testNewZealandAccentAustralianAccents0(self):		
		text = """The main difference between the two accents is vowel pronunciation. Australian vowels are drawn out while New Zealanders switch such vowels as ‘I’ for something like a ‘u’. An example is pronouncing “fush instead of fish”.
The Australia accent is believed to have originated from native-born children who spoke a new dialect combining dialects from the British Isles. The Kiwi dialect, on the other hand, came with immigrants who entered New Zealand from Britain.
The New Zealand accent is spiced with different British dialect inputs while the Australian accent is a mixture of British and American English.
"""
		match_dict = (   {   'aspect': ['origin'],
        'contrast': ['brough', 'in', 'by', 'immigrants', 'from', 'britain'],
        'subject': ['New', 'Zealand', 'Accent']},
    {   'aspect': ['origin'],
        'contrast': [   'a',
                        'mixture',
                        'of',
                        'british',
                        'and',
                        'american',
                        'english'],
        'subject': ['Australian', 'Accents']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testNewZealandAccentAustralianAccents1(self):		
		text = """The main difference between the two accents is vowel pronunciation. Australian vowels are drawn out while New Zealanders switch such vowels as ‘I’ for something like a ‘u’. An example is pronouncing “fush instead of fish”.
The Australia accent is believed to have originated from native-born children who spoke a new dialect combining dialects from the British Isles. The Kiwi dialect, on the other hand, came with immigrants who entered New Zealand from Britain.
The New Zealand accent is spiced with different British dialect inputs while the Australian accent is a mixture of British and American English.
"""
		match_dict = (   {   'aspect': ['examples'],
        'contrast': [   '“',
                        'yes',
                        '"',
                        'is',
                        'pronounced',
                        'as',
                        'pronounced',
                        'as',
                        '“',
                        'fush',
                        '”'],
        'subject': ['New', 'Zealand', 'Accent']},
    {   'aspect': ['examples'],
        'contrast': [   'most',
                        'australians',
                        'would',
                        'use',
                        'the',
                        'short',
                        'fz=/',
                        'vowel',
                        ',',
                        'like',
                        'in',
                        '“',
                        'cat',
                        '”',
                        'while',
                        'pronouncing',
                        'such',
                        'words',
                        'as',
                        '“',
                        'plant',
                        '”',
                        ',',
                        '“',
                        'branch',
                        '”',
                        ',',
                        '“',
                        'demand',
                        '”',
                        ',',
                        'and',
                        '“',
                        'sample',
                        '”',
                        ',',
                        'difference',
                        'dafiterence'],
        'subject': ['Australian', 'Accents']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		

	# good annotation
	def testThalamusHypothalamus0(self):		
		text = """While the thalamus is located almost directly in the center of the brain, the hypothalamus is located beneath it (which is how it got its name), so their locations are different, although not by very much.
The thalamus consists of two bulbs for each brain hemisphere, each around 6cm in diameter. On the other hand, the hypothalamus consists of a large number of very small bulbs called nuclei, and in total is the size of an almond. This means that the thalamus is larger than the hypothalamus and has a different structure.
The thalamus regulates sleep, alertness and wakefulness, whereas the hypothalamus regulates body temperature, hunger, fatigue and metabolic processes in general.
Although both thalamus and hypothalamus serve as “bridges”, they connect different pairs of things. While the thalamus connects the cerebral cortex with the midbrain, the hypothalamus connects the nervous system in general with the endocrine system. This makes another distinction between the two – the thalamus is a part of only the nervous system, while the hypothalamus can be regarded as both part of the nervous and endocrine system, since it plays an important role in both."""
		match_dict = (   {   'aspect': None,
        'contrast': ['located', 'near', 'the', 'center', 'of', 'the', 'brain'],
        'subject': ['Thalamus']},
    {   'aspect': None,
        'contrast': ['located', 'beneath', 'the', 'thalamus'],
        'subject': ['Hypothalamus']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# annotation missing a side
	def testThalamusHypothalamus1(self):		
		text = """While the thalamus is located almost directly in the center of the brain, the hypothalamus is located beneath it (which is how it got its name), so their locations are different, although not by very much.
The thalamus consists of two bulbs for each brain hemisphere, each around 6cm in diameter. On the other hand, the hypothalamus consists of a large number of very small bulbs called nuclei, and in total is the size of an almond. This means that the thalamus is larger than the hypothalamus and has a different structure.
The thalamus regulates sleep, alertness and wakefulness, whereas the hypothalamus regulates body temperature, hunger, fatigue and metabolic processes in general.
Although both thalamus and hypothalamus serve as “bridges”, they connect different pairs of things. While the thalamus connects the cerebral cortex with the midbrain, the hypothalamus connects the nervous system in general with the endocrine system. This makes another distinction between the two – the thalamus is a part of only the nervous system, while the hypothalamus can be regarded as both part of the nervous and endocrine system, since it plays an important role in both."""
		match_dict = (   {   'aspect': None,
        'contrast': ['two', '6cmsized', 'bulbs'],
        'subject': ['Thalamus']},
    {   'aspect': None,
        'contrast': [   'many',
                        'small',
                        'bulbs',
                        'called',
                        'nuclei',
                        ',',
                        'in',
                        'total',
                        'the',
                        'size',
                        'of',
                        'an',
                        'almond'],
        'subject': ['Hypothalamus']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testThalamusHypothalamus2(self):		
		text = """While the thalamus is located almost directly in the center of the brain, the hypothalamus is located beneath it (which is how it got its name), so their locations are different, although not by very much.
The thalamus consists of two bulbs for each brain hemisphere, each around 6cm in diameter. On the other hand, the hypothalamus consists of a large number of very small bulbs called nuclei, and in total is the size of an almond. This means that the thalamus is larger than the hypothalamus and has a different structure.
The thalamus regulates sleep, alertness and wakefulness, whereas the hypothalamus regulates body temperature, hunger, fatigue and metabolic processes in general.
Although both thalamus and hypothalamus serve as “bridges”, they connect different pairs of things. While the thalamus connects the cerebral cortex with the midbrain, the hypothalamus connects the nervous system in general with the endocrine system. This makes another distinction between the two – the thalamus is a part of only the nervous system, while the hypothalamus can be regarded as both part of the nervous and endocrine system, since it plays an important role in both."""
		match_dict = (   {   'aspect': None,
        'contrast': [   'regulates',
                        'sleep',
                        ',',
                        'alertness',
                        'and',
                        'wakefulness'],
        'subject': ['Thalamus']},
    {   'aspect': None,
        'contrast': [   'regulates',
                        'body',
                        'temperature',
                        ',',
                        'hunger',
                        ',',
                        'fatigue',
                        'and',
                        'metabolic',
                        'processes',
                        'in',
                        'general'],
        'subject': ['Hypothalamus']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testThalamusHypothalamus3(self):		
		text = """While the thalamus is located almost directly in the center of the brain, the hypothalamus is located beneath it (which is how it got its name), so their locations are different, although not by very much.
The thalamus consists of two bulbs for each brain hemisphere, each around 6cm in diameter. On the other hand, the hypothalamus consists of a large number of very small bulbs called nuclei, and in total is the size of an almond. This means that the thalamus is larger than the hypothalamus and has a different structure.
The thalamus regulates sleep, alertness and wakefulness, whereas the hypothalamus regulates body temperature, hunger, fatigue and metabolic processes in general.
Although both thalamus and hypothalamus serve as “bridges”, they connect different pairs of things. While the thalamus connects the cerebral cortex with the midbrain, the hypothalamus connects the nervous system in general with the endocrine system. This makes another distinction between the two – the thalamus is a part of only the nervous system, while the hypothalamus can be regarded as both part of the nervous and endocrine system, since it plays an important role in both."""
		match_dict = (   {   'aspect': None,
        'contrast': [   'connects',
                        'the',
                        'cerebral',
                        'cortex',
                        'with',
                        'the',
                        'midbrain'],
        'subject': ['Thalamus']},
    {   'aspect': None,
        'contrast': [   'connects',
                        'the',
                        'nervous',
                        'and',
                        'endocrine',
                        'systems'],
        'subject': ['Hypothalamus']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		

	# annotation missing a match
	def testDielectricGreaseVaseline0(self):		
		text = """Dielectric grease refers to a translucent substance that is mainly used to seal and protect electrical conductors against sand, dirt, dust, or other foreign materials. Vaseline, on the other hand, is a term used to refer to petroleum jelly.
On a comparison table, the dielectric grease is considered to be more superior than Vaseline when it comes to preserving connections. As such, petroleum jelly (or Vaseline) is weaker and would not last more than the dielectric grease when exposed to extreme temperatures.
Dielectric grease is not an electric conductor while anything soaked in petroleum jelly will burn if exposed to heat or an electric current.
Also, Vaseline has a very low melting point compared to the dielectric grease which can withstand extreme temperatures. This Vaseline property would make it to run and dry out eventually if exposed to any heat.
The dielectric grease is relatively expensive while Vaseline is relatively cheap.
"""
		match_dict = (   {   'aspect': ['cost', 'chemical', 'properties'],
        'contrast': [   'relatively',
                        'pricey',
                        '+',
                        'does',
                        'not',
                        'conduct',
                        'electricity',
                        'high',
                        'melting',
                        'point'],
        'subject': ['Dielectric', 'Grease']},
    {   'aspect': ['cost', 'chemical', 'properties'],
        'contrast': [   'relatively',
                        'cheap',
                        'petroleum',
                        'jelly',
                        'is',
                        'a',
                        'conductor',
                        'of',
                        'electricity',
                        '+',
                        'low',
                        'melting',
                        'point',
                        '[',
                        'da]pitference',
                        'between',
                        ',',
                        'net'],
        'subject': ['Vaseline']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		

	# good annotation
	def testDeductiveReasoningInductiveReasoning0(self):		
		text = """Deductive reasoning is based on general premise and this is usually true and it also gives a true conclusion to the line of thought.
Inductive reasoning specifically induces a particular premise that is then used as the basis for making a decision. The premise is used to support the conclusion that is reached after a certain line of reasoning.
Deductive reasoning is based on top down line of reasoning. It follows that an idea that is widely believed to be true is viewed from the top and it flows down to give a conclusion that forms the basis of making decisions
Inductive reasoning follows a bottom to top reasoning that is based on cause and effect analysis. A cause is assessed and its effect is then analyzed in a bid to give a conclusion to a certain idea.
Deductive reasoning uses scientific method to test the hypothesis. This is a statement that presupposes or assumes something to be true. A hypothesis can be tested to prove its authenticity or truth in a scientific manner.
A conclusion that is reached after the generalizations is the hypothesis. This hypothesis can then be tested to prove or support the idea proposed and can also be used for making decisions.
Deductive reasoning follows steps. In other words, this is a step by step process where certain thoughts that are believed to be true are followed. In most cases, there is a major premise that forms the first step and this is followed by a minor premise and these are used to make inferences that help to form a valid conclusion.
In contrast, it can be seen that inductive reasoning is based on broad generalizations and these are also based on specific observations that are also scientific in nature. The notable aspect here is that inductive reasoning is scientific and it can be tested for authenticity."""
		match_dict = (   {   'aspect': None,
        'contrast': ['based', 'on', 'general', 'premise'],
        'subject': ['Deductive', 'Reasoning']},
    {   'aspect': None,
        'contrast': ['it', 'induces', 'premises', 'for', 'reasoning'],
        'subject': ['Inductive', 'Reasoning']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# annotation spans more than two sentences
	def testDeductiveReasoningInductiveReasoning1(self):		
		text = """Deductive reasoning is based on general premise and this is usually true and it also gives a true conclusion to the line of thought.
Inductive reasoning specifically induces a particular premise that is then used as the basis for making a decision. The premise is used to support the conclusion that is reached after a certain line of reasoning.
Deductive reasoning is based on top down line of reasoning. It follows that an idea that is widely believed to be true is viewed from the top and it flows down to give a conclusion that forms the basis of making decisions
Inductive reasoning follows a bottom to top reasoning that is based on cause and effect analysis. A cause is assessed and its effect is then analyzed in a bid to give a conclusion to a certain idea.
Deductive reasoning uses scientific method to test the hypothesis. This is a statement that presupposes or assumes something to be true. A hypothesis can be tested to prove its authenticity or truth in a scientific manner.
A conclusion that is reached after the generalizations is the hypothesis. This hypothesis can then be tested to prove or support the idea proposed and can also be used for making decisions.
Deductive reasoning follows steps. In other words, this is a step by step process where certain thoughts that are believed to be true are followed. In most cases, there is a major premise that forms the first step and this is followed by a minor premise and these are used to make inferences that help to form a valid conclusion.
In contrast, it can be seen that inductive reasoning is based on broad generalizations and these are also based on specific observations that are also scientific in nature. The notable aspect here is that inductive reasoning is scientific and it can be tested for authenticity."""
		match_dict = (   {   'aspect': None,
        'contrast': [   'based',
                        'on',
                        'true',
                        'premise',
                        'and',
                        'true',
                        'conclusion'],
        'subject': ['Deductive', 'Reasoning']},
    {   'aspect': None,
        'contrast': [   'broad',
                        'generalizations',
                        'based',
                        'on',
                        'specific',
                        'observations'],
        'subject': ['Inductive', 'Reasoning']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# good annotation
	def testDeductiveReasoningInductiveReasoning2(self):		
		text = """Deductive reasoning is based on general premise and this is usually true and it also gives a true conclusion to the line of thought.
Inductive reasoning specifically induces a particular premise that is then used as the basis for making a decision. The premise is used to support the conclusion that is reached after a certain line of reasoning.
Deductive reasoning is based on top down line of reasoning. It follows that an idea that is widely believed to be true is viewed from the top and it flows down to give a conclusion that forms the basis of making decisions
Inductive reasoning follows a bottom to top reasoning that is based on cause and effect analysis. A cause is assessed and its effect is then analyzed in a bid to give a conclusion to a certain idea.
Deductive reasoning uses scientific method to test the hypothesis. This is a statement that presupposes or assumes something to be true. A hypothesis can be tested to prove its authenticity or truth in a scientific manner.
A conclusion that is reached after the generalizations is the hypothesis. This hypothesis can then be tested to prove or support the idea proposed and can also be used for making decisions.
Deductive reasoning follows steps. In other words, this is a step by step process where certain thoughts that are believed to be true are followed. In most cases, there is a major premise that forms the first step and this is followed by a minor premise and these are used to make inferences that help to form a valid conclusion.
In contrast, it can be seen that inductive reasoning is based on broad generalizations and these are also based on specific observations that are also scientific in nature. The notable aspect here is that inductive reasoning is scientific and it can be tested for authenticity."""
		match_dict = (   {   'aspect': None,
        'contrast': ['top', 'down', 'reasoning'],
        'subject': ['Deductive', 'Reasoning']},
    {   'aspect': None,
        'contrast': ['bottom', 'up', 'reasoning'],
        'subject': ['Inductive', 'Reasoning']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# annotation spans more than two sentences
	def testDeductiveReasoningInductiveReasoning3(self):		
		text = """Deductive reasoning is based on general premise and this is usually true and it also gives a true conclusion to the line of thought.
Inductive reasoning specifically induces a particular premise that is then used as the basis for making a decision. The premise is used to support the conclusion that is reached after a certain line of reasoning.
Deductive reasoning is based on top down line of reasoning. It follows that an idea that is widely believed to be true is viewed from the top and it flows down to give a conclusion that forms the basis of making decisions
Inductive reasoning follows a bottom to top reasoning that is based on cause and effect analysis. A cause is assessed and its effect is then analyzed in a bid to give a conclusion to a certain idea.
Deductive reasoning uses scientific method to test the hypothesis. This is a statement that presupposes or assumes something to be true. A hypothesis can be tested to prove its authenticity or truth in a scientific manner.
A conclusion that is reached after the generalizations is the hypothesis. This hypothesis can then be tested to prove or support the idea proposed and can also be used for making decisions.
Deductive reasoning follows steps. In other words, this is a step by step process where certain thoughts that are believed to be true are followed. In most cases, there is a major premise that forms the first step and this is followed by a minor premise and these are used to make inferences that help to form a valid conclusion.
In contrast, it can be seen that inductive reasoning is based on broad generalizations and these are also based on specific observations that are also scientific in nature. The notable aspect here is that inductive reasoning is scientific and it can be tested for authenticity."""
		match_dict = (   {   'aspect': None,
        'contrast': [   'uses',
                        'scientific',
                        'method',
                        'to',
                        'test',
                        'a',
                        'hypothesis'],
        'subject': ['Deductive', 'Reasoning']},
    {   'aspect': None,
        'contrast': ['conclusion', 'is', 'the', 'hypothesis'],
        'subject': ['Inductive', 'Reasoning']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# annotation spans more than two sentences
	def testDeductiveReasoningInductiveReasoning4(self):		
		text = """Deductive reasoning is based on general premise and this is usually true and it also gives a true conclusion to the line of thought.
Inductive reasoning specifically induces a particular premise that is then used as the basis for making a decision. The premise is used to support the conclusion that is reached after a certain line of reasoning.
Deductive reasoning is based on top down line of reasoning. It follows that an idea that is widely believed to be true is viewed from the top and it flows down to give a conclusion that forms the basis of making decisions
Inductive reasoning follows a bottom to top reasoning that is based on cause and effect analysis. A cause is assessed and its effect is then analyzed in a bid to give a conclusion to a certain idea.
Deductive reasoning uses scientific method to test the hypothesis. This is a statement that presupposes or assumes something to be true. A hypothesis can be tested to prove its authenticity or truth in a scientific manner.
A conclusion that is reached after the generalizations is the hypothesis. This hypothesis can then be tested to prove or support the idea proposed and can also be used for making decisions.
Deductive reasoning follows steps. In other words, this is a step by step process where certain thoughts that are believed to be true are followed. In most cases, there is a major premise that forms the first step and this is followed by a minor premise and these are used to make inferences that help to form a valid conclusion.
In contrast, it can be seen that inductive reasoning is based on broad generalizations and these are also based on specific observations that are also scientific in nature. The notable aspect here is that inductive reasoning is scientific and it can be tested for authenticity."""
		match_dict = (   {   'aspect': None,
        'contrast': ['follows', 'steps'],
        'subject': ['Deductive', 'Reasoning']},
    {   'aspect': None,
        'contrast': ['broad', 'generalizations'],
        'subject': ['Inductive', 'Reasoning']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		

	# annotation spans more than two sentences
	def testAIProcessorNormalProcessor0(self):		
		text = """– Processors used in portable devices such as mobile phones are generally referred to as mobile processors or mobile chips. Regular CPUs found in mobile phones as well as desktop computers are like engines of your mobile devices which perform and execute anything you want your phones to do. It’s the central hub of your device and it manages every application you run on your mobile device. AI chips are the future of mobile processors that are capable of doing more than just the basic tasks your phone can do. AI chips are simply designed to do specific AI tasks more effectively and efficiently.
– AI processors are specialized chips, which incorporate AI technology and machine learning to make your mobile devices smart enough to imitate the human brain. AI chips are used to optimize deep learning AI workloads. Machine learning is just a way to achieve artificial intelligence. AI chip refers to a system that uses multiple processors each with specialized functions. Normal CPUs are housed in a smaller chip package and designed to support mobile applications delivering all system capabilities needed to support mobile device applications.
– Normal processors are not well suited or equipped enough to fulfill the demands of machine learning. AI chips have an additional Neural Processing Unit (NPU) that is capable delivering much faster AI performance and a better battery life. With heterogeneous computing capabilities, AI chips offer high performance and power efficiency for AI applications. Image recognition and processing become a lot faster so that your smartphone can perform multiple tasks simultaneously. And they can handle specific programming tasks much faster and efficiently than normal CPUs can manage.
"""
		match_dict = (   {   'aspect': None,
        'contrast': [   'al',
                        'processors',
                        'are',
                        'specialized',
                        'chips',
                        ',',
                        'which',
                        'incorporate',
                        'al',
                        'technology',
                        'and',
                        'machine',
                        'learning',
                        'to',
                        'make',
                        'your',
                        'mobile',
                        'devices',
                        'smart',
                        ','],
        'subject': ['AI', 'Processor']},
    {   'aspect': None,
        'contrast': [   'normal',
                        'cpus',
                        'are',
                        'housed',
                        'in',
                        'a',
                        'smaller',
                        'chip',
                        'package',
                        'and',
                        'are',
                        'designed',
                        'to',
                        'support',
                        'mobile',
                        'applications',
                        ','],
        'subject': ['Normal', 'Processor']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# annotation spans more than two sentences
	def testAIProcessorNormalProcessor1(self):		
		text = """– Processors used in portable devices such as mobile phones are generally referred to as mobile processors or mobile chips. Regular CPUs found in mobile phones as well as desktop computers are like engines of your mobile devices which perform and execute anything you want your phones to do. It’s the central hub of your device and it manages every application you run on your mobile device. AI chips are the future of mobile processors that are capable of doing more than just the basic tasks your phone can do. AI chips are simply designed to do specific AI tasks more effectively and efficiently.
– AI processors are specialized chips, which incorporate AI technology and machine learning to make your mobile devices smart enough to imitate the human brain. AI chips are used to optimize deep learning AI workloads. Machine learning is just a way to achieve artificial intelligence. AI chip refers to a system that uses multiple processors each with specialized functions. Normal CPUs are housed in a smaller chip package and designed to support mobile applications delivering all system capabilities needed to support mobile device applications.
– Normal processors are not well suited or equipped enough to fulfill the demands of machine learning. AI chips have an additional Neural Processing Unit (NPU) that is capable delivering much faster AI performance and a better battery life. With heterogeneous computing capabilities, AI chips offer high performance and power efficiency for AI applications. Image recognition and processing become a lot faster so that your smartphone can perform multiple tasks simultaneously. And they can handle specific programming tasks much faster and efficiently than normal CPUs can manage.
"""
		match_dict = (   {   'aspect': None,
        'contrast': [   'al',
                        'chip',
                        'refers',
                        'to',
                        'a',
                        'system',
                        'that',
                        'uses',
                        'multiple',
                        'processors',
                        'each',
                        'with',
                        'specialized',
                        'functions',
                        ','],
        'subject': ['AI', 'Processor']},
    {   'aspect': None,
        'contrast': [   'regular',
                        'processors',
                        'are',
                        'not',
                        'well',
                        'suited',
                        'or',
                        'equipped',
                        'enough',
                        'to',
                        'fulfill',
                        'the',
                        'demands',
                        'of',
                        'machine',
                        'learning',
                        ','],
        'subject': ['Normal', 'Processor']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		


	# annotation spans more than two sentences
	def testAIProcessorNormalProcessor2(self):		
		text = """– Processors used in portable devices such as mobile phones are generally referred to as mobile processors or mobile chips. Regular CPUs found in mobile phones as well as desktop computers are like engines of your mobile devices which perform and execute anything you want your phones to do. It’s the central hub of your device and it manages every application you run on your mobile device. AI chips are the future of mobile processors that are capable of doing more than just the basic tasks your phone can do. AI chips are simply designed to do specific AI tasks more effectively and efficiently.
– AI processors are specialized chips, which incorporate AI technology and machine learning to make your mobile devices smart enough to imitate the human brain. AI chips are used to optimize deep learning AI workloads. Machine learning is just a way to achieve artificial intelligence. AI chip refers to a system that uses multiple processors each with specialized functions. Normal CPUs are housed in a smaller chip package and designed to support mobile applications delivering all system capabilities needed to support mobile device applications.
– Normal processors are not well suited or equipped enough to fulfill the demands of machine learning. AI chips have an additional Neural Processing Unit (NPU) that is capable delivering much faster AI performance and a better battery life. With heterogeneous computing capabilities, AI chips offer high performance and power efficiency for AI applications. Image recognition and processing become a lot faster so that your smartphone can perform multiple tasks simultaneously. And they can handle specific programming tasks much faster and efficiently than normal CPUs can manage.
"""
		match_dict = (   {   'aspect': None,
        'contrast': [   'al',
                        'chips',
                        'can',
                        'handle',
                        'sgecific',
                        'programming',
                        'tasks',
                        'much',
                        'faster',
                        'and',
                        'efficiently',
                        'than',
                        'normal',
                        'cpus',
                        'can',
                        'manage',
                        ','],
        'subject': ['AI', 'Processor']},
    {   'aspect': None,
        'contrast': [   'the',
                        'main',
                        'idea',
                        'behind',
                        'mobile',
                        'processors',
                        'is',
                        'reducing',
                        'their',
                        'size',
                        ',',
                        'power',
                        'usage',
                        ',',
                        'and',
                        'heat',
                        'generation',
                        ',',
                        'p|pifference',
                        'between',
                        ',',
                        'net'],
        'subject': ['Normal', 'Processor']})
		rule = "text"
		self.assertTrue(test_rule (text, match_dict, rule))
		

	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	#   1 good annotation
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 
	# 