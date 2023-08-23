import unittest 
import pylab
import math

import ps5

class TestPS5(unittest.TestCase):

	def test_generate_models(self):

		degs_msg = "generate_models should return one model for each given degree"
		list_type_msg = "generate_models should return a list of models"
		array_type_msg = "each model returned by generate_models should be of type pylab.array"
		coefficient_mismatch = "coefficients of returned model are not as expected"

		# simple y = x case. 
		x = pylab.array(range(50))
		y = pylab.array(range(50))
		degrees = [1]
		models = ps5.generate_models(x, y, degrees)

		self.assertEqual(len(models), len(degrees), degs_msg)
		self.assertIsInstance(models, list, list_type_msg)
		self.assertIsInstance(models[0], pylab.ndarray, array_type_msg)
		self.assertListEqual(list(models[0]), list(pylab.polyfit(x, y, 1)), coefficient_mismatch)

		# two models for y = 2x case 
		y = pylab.array(range(0,100,2))
		degrees = [1, 2]
		models = ps5.generate_models(x, y, degrees)
		self.assertEqual(len(models), len(degrees), degs_msg)
		self.assertIsInstance(models, list, list_type_msg)
		for m in models:
			self.assertIsInstance(m, pylab.ndarray, array_type_msg)
		for i in range(2):
			self.assertListEqual(list(models[i]), list(pylab.polyfit(x,y, degrees[i])), coefficient_mismatch)

		# three models 
		degrees = [1,2,20]
		models = ps5.generate_models(x, y, degrees)
		self.assertEquals(len(models), len(degrees), degs_msg)
		self.assertIsInstance(models, list, list_type_msg)
		for m in models:
			self.assertIsInstance(m, pylab.ndarray, array_type_msg)
		for i in range(3):
			self.assertListEqual(list(models[i]), list(pylab.polyfit(x,y, degrees[i])), coefficient_mismatch)

		
	def test_r_squared(self):

		# basic case:
		# actual values    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
		# estimated values [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
		y = pylab.array(range(10))
		est = pylab.array([5]*10)
		r_sq = ps5.r_squared(y, est)
		self.assertIsInstance(r_sq, float, "r_squared should return a float")
		rounded = round(r_sq, 6)
		self.assertEquals(rounded, -0.030303)

		# another basic case:
		# actual values    [0, 1, 2, 3, 4, 5, 6, 7, 8]
		# estimated values [0, 2, 4, 6, 8, 10, 12, 14, 16]
		est = pylab.array(range(0,20,2))
		r_sq = ps5.r_squared(y, est)
		self.assertIsInstance(r_sq, float, "r_squared should return a float")
		rounded = round(r_sq, 6)
		self.assertEquals(rounded, -2.454545)

		# case where actual = estimated, so R^2=1
		r_sq = ps5.r_squared(y, y)
		self.assertIsInstance(r_sq, float, "r_squared should return a float")
		self.assertEquals(r_sq, 1.0)

	def test_gen_cities_avg(self):
		# test for just one city
		climate = ps5.Climate('data.csv')
		test_years = pylab.array(ps5.TESTING_INTERVAL)
		result = ps5.gen_cities_avg(climate, ['SEATTLE'], test_years)
		correct = [11.514383561643836,10.586849315068493,11.28319672,12.10643836,12.82917808,13.13178082]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "City averages do not match expected results")

		# multiple cities
		result = ps5.gen_cities_avg(climate, ps5.CITIES, test_years)
		correct = [16.75950424, 16.85749511,17.56180068,16.65717547,16.84499022,17.54460535]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "City averages do not match expected results")

		# years range
		# multiple cities
		result = ps5.gen_cities_avg(climate, ['TAMPA', 'DALLAS'], test_years)
		correct = [20.8040411,22.03910959,22.27206284,21.31136986,20.88123288,22.07794521]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "City averages do not match expected results")

	def test_moving_avg(self):
		y = [1, 2, 3, 4, 5, 6, 7]
		window_length = 3
		correct = pylab.array([1, 1.5, 2, 3, 4, 5, 6])
		result = ps5.moving_average(y, window_length)
		self.assertListEqual(list(result), list(correct), "Moving average values incorrect")

		y = [-1.5, 1.5, -3.0, 3.0, -4.5, 4.5]
		window_length = 2
		correct = [-1.5, 0, -.75, 0, -.75, 0]
		result = ps5.moving_average(y, window_length)
		self.assertListEqual(list(result), list(correct), "Moving average values incorrect")

	def test_rmse(self):
		y = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		estimate = [1, 4, 9, 16, 25, 36, 49, 64, 81]
		result = ps5.rmse(pylab.array(y), pylab.array(estimate))
		correct = 35.8515457593
		self.assertTrue(math.isclose(correct, result), "RMSE value incorrect")

		y = [1, 1, 1, 1, 1, 1, 1, 1, 1]
		estimate = [1, 4, 9, 16, 25, 36, 49, 64, 81]
		result = ps5.rmse(pylab.array(y), pylab.array(estimate))
		correct = 40.513372278
		self.assertTrue(math.isclose(correct, result), "RMSE value incorrect")

	def test_gen_std_devs(self):
		climate = ps5.Climate('data.csv')
		years = pylab.array(ps5.TRAINING_INTERVAL)
		result = ps5.gen_std_devs(climate, ['SEATTLE'], years)
		correct = [6.1119325255476635, 5.4102625076401125, 6.0304210441394801, 5.5823239710637846, 5.5908151965372177, 5.0347634736031583, 6.2485081784971772, 5.6752637253518703, 5.9822493041266327, 5.5376216719090898, 6.0339331562285095, 6.3471434661632733, 5.3872564859222782, 5.7528361897357705, 6.0117329392620285, 5.5922579610955854, 5.67888175212234, 5.7810899373043272, 5.7184178577664087, 5.3955809402004036, 5.1736886920193665, 5.8134229790176573, 5.1915733214759872, 5.4023314139519591, 6.7868442109830855, 5.2952870947334114, 5.6064597624296333, 5.4921097908102086, 6.1450202825415214, 6.3591021848005278, 5.4996866353350615, 5.6516820894310058, 5.7969983303071411, 5.8531227958031931, 5.2545492072097808, 6.0102701017450126, 5.5327493838092865, 5.7703034605336532, 5.0412624972468443, 5.2728662938897264, 5.0859211734722649, 5.5526426823734987, 5.8005720594546748, 5.7391426965165389, 5.5518538235632207, 5.8279562142168073, 5.9089508390885479, 5.9789908401877394, 6.5696153940105573]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "Standard deviations do not match expected results")

		result = ps5.gen_std_devs(climate, ps5.CITIES, years)
		correct = [6.8007729489975439, 6.9344723094071865, 7.2965004501815818, 6.8077243598168549, 6.5055948680511539, 6.959087494608867, 6.4889799240243695, 6.9510430337868963, 7.0585431115159478, 7.0977420580318782, 6.8386579785236048, 6.731347077523127, 6.6616225764762902, 6.4092396746786013, 6.6214217100011084, 6.7136104957814435, 7.2575482189983553, 7.263276360210706, 7.1787611973720633, 7.0859352578611796, 6.8736741252762821, 6.7957043866857889, 7.0815549177622765, 6.7249974778654433, 7.2162729580931124, 6.4560372283957266, 6.7288306794528907, 6.9720986945202927, 6.922958341746317, 6.3033645588306086, 6.5330170805999908, 6.2777429551963237, 6.8488629387504032, 6.8257830274740625, 6.7856101061465059, 6.7592782215870484, 6.6634050127541604, 6.4486321701001552, 6.3413248952817742, 6.7637674361128752, 6.5519930751275384, 6.6831654464946064, 6.7751550280705839, 6.7435411127318146, 6.8720508861149154, 6.381528250607194, 6.9707944558310109, 6.7582457290380731, 6.7451346848899991]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "Standard deviations do not match expected results")

		result = ps5.gen_std_devs(climate, ['TAMPA', 'DALLAS'], years)
		correct = [6.6222742584336203, 7.0831603561201613, 7.7597469401129215, 7.0259613619453818, 6.5638542892147722, 7.2251974365928691, 6.1518558874089617, 7.0391602268356808, 7.1526420227632297, 7.2908275139292842, 6.270260767160857, 6.4782366919527483, 6.6679030134469448, 6.0219388710726411, 6.6228151175078525, 6.4353160709432649, 7.8465935407208427, 8.1048357980863859, 7.2582171660107786, 7.7051951164668244, 7.083156557719672, 6.6459102430953294, 7.3472808518990416, 6.7892304784646278, 7.4543972339551905, 6.3029047021487283, 6.6943381051857225, 6.9549273458644914, 7.0491429730256217, 6.0235494427214373, 6.3241265661686636, 6.125270864250882, 6.8769945045255714, 6.2418939236561259, 6.8146994668451102, 7.2018962701686169, 6.5761298971998094, 7.0293238787351466, 6.3457405064020591, 7.1321062259929908, 6.5963446478678387, 6.750967975464123, 6.839988834120371, 6.4423456425074255, 6.8283808762586897, 6.3536010884491958, 6.6492152503358843, 6.6265277854285625, 6.6375221251962317]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "Standard deviations do not match expected results")


if __name__ == '__main__':
    # Run the tests and print verbose output to stderr.
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS5))
    unittest.TextTestRunner(verbosity=2).run(suite)
