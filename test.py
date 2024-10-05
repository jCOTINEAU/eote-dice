#! /usr/bin/env python3

"""eote-dice tests."""

import unittest
from unittest import mock
import operator

from dice import (AbilityDice, BoostDice, ChallengeDice, dice_from_color_char, DicePool,
                  DifficultyDice, ProficiencyDice, SetbackDice, Side, Symbol)
from dice import (ExperimentalAbilityDice, ExperimentalBoostDice, ExperimentalChallengeDice,
                  ExperimentalDifficultyDice, ExperimentalProficiencyDice, ExperimentalSetbackDice)
from distribution import QuadDistribution

class ExperimentalTestCase(unittest.TestCase):
    
    def setUp(self):
        # Set experimental mode to True
        DicePool.is_experimental = True

    def tearDown(self):
        # Reset experimental mode to False
        DicePool.is_experimental = False

class SideTestCase(unittest.TestCase):
    def test_count_symbol(self):
        side = Side(symbols=[Symbol.Triumph, Symbol.Triumph, Symbol.Despair])
        self.assertEqual(side.count_symbol(Symbol.Triumph), 2)
        self.assertEqual(side.count_symbol(Symbol.Despair), 1)
        self.assertEqual(side.count_symbol(Symbol.Success), 0)
        self.assertEqual(side.count_symbol(Symbol.Advantage), 0)


class DiceFromColorTestCase(unittest.TestCase):
    def test_invalid_dice_char(self):
        with self.assertRaises(ValueError):
            dice_from_color_char('z')

    def test_valid_dice_char(self):
        self.assertIsInstance(dice_from_color_char('y'), ProficiencyDice)
        self.assertIsInstance(dice_from_color_char('b'), BoostDice)
        self.assertIsInstance(dice_from_color_char('g'), AbilityDice)
        self.assertIsInstance(dice_from_color_char('k'), SetbackDice)
        self.assertIsInstance(dice_from_color_char('p'), DifficultyDice)
        self.assertIsInstance(dice_from_color_char('r'), ChallengeDice)

class ExperimentalDiceFromColorTestCase(ExperimentalTestCase):

    def test_experimental_invalid_dice_char(self):
        with self.assertRaises(ValueError):
            dice_from_color_char('z')

    def test_experimental_valid_dice_char(self):
        self.assertIsInstance(dice_from_color_char('y'), ExperimentalProficiencyDice)
        self.assertIsInstance(dice_from_color_char('b'), ExperimentalBoostDice)
        self.assertIsInstance(dice_from_color_char('g'), ExperimentalAbilityDice)
        self.assertIsInstance(dice_from_color_char('k'), ExperimentalSetbackDice)
        self.assertIsInstance(dice_from_color_char('p'), ExperimentalDifficultyDice)
        self.assertIsInstance(dice_from_color_char('r'), ExperimentalChallengeDice)

class DiceTestCase(unittest.TestCase):
    def test_num_sides(self):
        self.assertEqual(ProficiencyDice().num_sides(), 12)
        self.assertEqual(BoostDice().num_sides(), 6)

    def test_boost_first_roll(self):
        with mock.patch('dice.random.choice', autospec=True, spec_set=True,
                        side_effect=lambda seq: seq[0]):
            symbols = BoostDice().roll()
            self.assertEqual(len(symbols), 0)

    def test_boost_third_roll(self):
        with mock.patch('dice.random.choice', autospec=True, spec_set=True,
                        side_effect=lambda seq: seq[2]):
            symbols = BoostDice().roll()
            self.assertEqual(len(symbols), 2)
            self.assertIs(symbols[0], Symbol.Advantage)
            self.assertIs(symbols[1], Symbol.Advantage)

    def test_difficulty_roll(self):
        symbols = DifficultyDice().roll()
        self.assertGreaterEqual(len(symbols), 0)
        self.assertLessEqual(len(symbols), 2)
        if len(symbols) > 0:
            self.assertIsNot(symbols[0], Symbol.Triumph)
            self.assertIsNot(symbols[0], Symbol.Despair)
            self.assertIsNot(symbols[0], Symbol.Success)
            self.assertIsNot(symbols[0], Symbol.Advantage)


class QuadDistributionTestCase(unittest.TestCase):
    def test_simple_probability_above(self):
        dice = QuadDistribution({(1, 0, 0, 0): 1,
                                 (0, 2, 0, 0): 1,
                                 (1, 1, 0, 0): 2,
                                 (0, 0, 1, 0): 2})
        self.assertEqual(dice.probability_above(tuple([0, 1, 0, 0])), 0.5)
        self.assertEqual(dice.probability_above(tuple([1, 1, 0, 0])), 1/3)
        self.assertEqual(dice.mean(), (0.5, 2/3, 1/3, 0))

    def test_simple_probability(self):
        dice = QuadDistribution({(1, 0, 0, 0): 1,
                                 (0, 2, 0, 0): 1,
                                 (1, 1, 0, 0): 2,
                                 (0, 0, 1, 0): 2})
        self.assertEqual(dice.probability(tuple([0, 1, 0, 0])), 0)
        self.assertEqual(dice.probability(tuple([1, 1, 0, 0])), 2/6)
        self.assertEqual(dice.probability(tuple([1, None, None, None])), 3/6)
        self.assertEqual(dice.mean(), (0.5, 2/3, 1/3, 0))

    def test_simple_probability_with_operator(self):
        dice = QuadDistribution({(1, 0, 0, 0): 1,
                                 (0, 2, 0, 0): 1,
                                 (1, 1, 0, 0): 2,
                                 (0, 0, 1, 0): 2})
        self.assertEqual(dice.probability_with_operator(tuple([[0,operator.ge],[1,operator.ge],[0,operator.ge],[0,operator.ge]])), 0.5)
        self.assertEqual(dice.probability_with_operator(tuple([[1,operator.ge],[1,operator.ge],[0,operator.ge],[0,operator.ge]])), 1/3)
        self.assertEqual(dice.probability_with_operator(tuple([[1,operator.eq],[1,operator.eq],[0,operator.eq],[0,operator.eq]])), 1/3)
        self.assertEqual(dice.probability_with_operator(tuple([[0,operator.eq],[0,operator.eq],[0,operator.eq],[0,operator.eq]])), 0)
        self.assertEqual(dice.probability_with_operator(tuple([[0,operator.eq],[2,operator.eq],[0,operator.eq],[0,operator.eq]])), 1/6)
        self.assertEqual(dice.probability_with_operator(tuple([[1,operator.le],[2,operator.ge],None,None])), 1/6)
        self.assertEqual(dice.probability_with_operator(tuple([None,[1,operator.ge],None,None])), 3/6)
        self.assertEqual(dice.mean(), (0.5, 2/3, 1/3, 0))

    def test_add(self):
        dice1 = QuadDistribution({(0, 1, 0, 0): 1,
                                 (0, 2, 0, 0): 1,
                                 (0, 1, 1, 0): 2,
                                 (0, 0, 1, 0): 2})
        dice2 = QuadDistribution({(0, 1, 0, 0): 2,
                                 (0, 0, 2, 0): 2})
        result = dice1.add(dice2)
        correct_result = QuadDistribution({
                                          (0, 2, 0, 0): 2,
                                          (0, 1, 2, 0): 2,
                                          (0, 3, 0, 0): 2,
                                          (0, 2, 2, 0): 2,
                                          (0, 2, 1, 0): 4,
                                          (0, 1, 3, 0): 4,
                                          (0, 1, 1, 0): 4,
                                          (0, 0, 3, 0): 4})
        self.assertEqual(result.mean(), correct_result.mean())
        self.assertEqual(result.probability_above(cutoff=(0, 2, 1, 0)),
                         correct_result.probability_above(cutoff=(0, 2, 1, 0)))

    def test_empty_distribution(self):
        dice = QuadDistribution()
        self.assertEqual(dice.mean(), (0.0, 0.0, 0.0, 0.0))
        self.assertEqual(dice.median(), (0.0, 0.0, 0.0, 0.0))
        self.assertEqual(dice.standard_deviation(), (0.0, 0.0, 0.0, 0.0))
        self.assertEqual(dice.probability_above(tuple([1, 0, 0, 0])), 0.0)

    def test_median_distribution(self):
        dice = QuadDistribution({(1, 1, 0, 0): 1,
                                 (0, 1, 0, 0): 1,
                                 (2, 1, 0, 0): 1})
        median = dice.median()
        self.assertEqual(median, (1, 1, 0, 0))

        dice = QuadDistribution({(2, 1, 0, 0): 3})
        median = dice.median()
        self.assertEqual(median, (2, 1, 0, 0))

        dice = QuadDistribution({(1, 3, 0, 0): 3,
                                 (0, 1, 0, 0): 1,
                                 (2, 1, 0, 0): 4})
        median = dice.median()
        self.assertEqual(median, (1.5, 1, 0, 0))

    def test_standard_deviation(self):
        dice = QuadDistribution({(1, 1, 0, 0): 1,
                                 (0, 1, 0, 0): 1,
                                 (2, 1, 0, 0): 1})
        std = dice.standard_deviation()
        round_std = tuple(round(x, 2) for x in std)
        self.assertEqual(round_std, (0.82, 0.0, 0.0, 0.0))

class DicePoolTestCase(unittest.TestCase):
    def test_from_string_1(self):
        pool = DicePool.from_string('ygk')
        self.assertEqual(str(pool),
                         '\x1b[1m\x1b[33my\x1b[0m\x1b[1m\x1b[32mg\x1b[0m\x1b[30m\x1b[47mk\x1b[0m')

    def test_from_string_2(self):
        pool = DicePool.from_string('brp')
        self.assertEqual(str(pool),
                         '\x1b[1m\x1b[36mb\x1b[0m\x1b[1m\x1b[31mr\x1b[0m\x1b[1m\x1b[35mp\x1b[0m')

    def test_invalid_from_string(self):
        with self.assertRaises(ValueError):
            DicePool.from_string('yyx')

    def test_good_dice_to_string(self):
        pool_string='gybrpk'
        self.assertEqual(DicePool._good_dice_to_string(pool_string=pool_string), 'ygb')

    def test_bad_dice_to_string(self):
        pool_string='gybrpk'
        self.assertEqual(DicePool._bad_dice_to_string(pool_string=pool_string), 'rpk')

    #TODO add tests about the other probability method added.

    def test_probability_boost(self):
        pool = DicePool([BoostDice()])
        self.assertEqual(pool.probability(triumph_cutoff=1), 0)
        self.assertEqual(pool.probability(despair_cutoff=1), 0)
        self.assertEqual(pool.probability(success_cutoff=1), 2/6)
        self.assertEqual(pool.probability(advantage_cutoff=1), 2/6)
        self.assertEqual(pool.probability(success_cutoff=1, advantage_cutoff=1), 1/6)
        self.assertEqual(pool.probability(advantage_cutoff=2), 1/6)
        mean = pool.mean()
        self.assertEqual(mean.triumph, 0.0)
        self.assertEqual(mean.success, 1/3)
        self.assertEqual(mean.advantage, 2/3)
        self.assertEqual(mean.despair, 0.0)

    def test_probability_above_boost(self):
        pool = DicePool([BoostDice()])
        self.assertEqual(pool.probability_above(triumph_cutoff=1), 0)
        self.assertEqual(pool.probability_above(despair_cutoff=1), 0)
        self.assertEqual(pool.probability_above(success_cutoff=1), 1/3)
        self.assertEqual(pool.probability_above(advantage_cutoff=1), 1/2)
        self.assertEqual(pool.probability_above(success_cutoff=1, advantage_cutoff=1), 1/6)
        mean = pool.mean()
        self.assertEqual(mean.triumph, 0.0)
        self.assertEqual(mean.success, 1/3)
        self.assertEqual(mean.advantage, 2/3)
        self.assertEqual(mean.despair, 0.0)

    def test_probability_above_proficiency_challenge(self):
        pool = DicePool([ProficiencyDice(), ChallengeDice()])
        self.assertEqual(pool.probability_above(triumph_cutoff=1), 1/12)
        self.assertEqual(pool.probability_above(despair_cutoff=1), 1/12)
        self.assertEqual(pool.probability_above(success_cutoff=1), 0.3472222222222222)
        self.assertEqual(pool.probability_above(advantage_cutoff=1), 0.3055555555555556)
        self.assertEqual(pool.probability_above(success_cutoff=1, advantage_cutoff=1),
                         0.020833333333333332)
        mean = pool.mean()
        self.assertEqual(mean.triumph, 1/12)
        self.assertEqual(mean.success, 0.08333333333333333)
        self.assertEqual(mean.advantage, 0.0)
        self.assertEqual(mean.despair, 1/12)

    def test_boost_first_roll(self):
        with mock.patch('dice.random.choice', autospec=True, spec_set=True,
                        side_effect=lambda seq: seq[0]):
            symbols = DicePool([BoostDice(), ]).roll()
            self.assertEqual(len(symbols), 0)

    def test_boost_third_roll(self):
        with mock.patch('dice.random.choice', autospec=True, spec_set=True,
                        side_effect=lambda seq: seq[2]):
            symbols = DicePool([BoostDice(), ]).roll()
            self.assertEqual(len(symbols), 2)
            self.assertIs(symbols[0], Symbol.Advantage)
            self.assertIs(symbols[1], Symbol.Advantage)

    def test_ability_difficulty_fourth_roll(self):
        with mock.patch('dice.random.choice', autospec=True, spec_set=True,
                        side_effect=lambda seq: seq[3]):
            symbols = DicePool([AbilityDice(), DifficultyDice()]).roll()
            self.assertEqual(len(symbols), 4)
            self.assertIs(symbols[0], Symbol.Success)
            self.assertIs(symbols[1], Symbol.Success)
            self.assertIs(symbols[2], Symbol.Failure)
            self.assertIs(symbols[3], Symbol.Threat)

    def test_ability_difficulty_second_roll(self):
        with mock.patch('dice.random.choice', autospec=True, spec_set=True,
                        side_effect=lambda seq: seq[1]):
            symbols = DicePool([AbilityDice(), DifficultyDice()]).roll()
            self.assertEqual(len(symbols), 2)
            self.assertIs(symbols[0], Symbol.Success)
            self.assertIs(symbols[1], Symbol.Failure)

    def test_proficiency_challenge_sixth_roll_ascii(self):
        with mock.patch('dice.random.choice', autospec=True, spec_set=True,
                        side_effect=lambda seq: seq[5]):
            symbols, cancelled_symbols = DicePool([ProficiencyDice(),
                                                   ChallengeDice()]).roll_ascii()
            self.assertEqual(symbols, '\x1b[1m\x1b[32ms\x1b[0m\x1b[1m\x1b[36ma\x1b[0m\x1b[1m\x1b[35mf\x1b[0m\x1b[30m\x1b[47mr\x1b[0m')
            self.assertEqual(cancelled_symbols, '')

    def test_proficiency_challenge_twelfth_roll_ascii(self):
        with mock.patch('dice.random.choice', autospec=True, spec_set=True,
                        side_effect=lambda seq: seq[11]):
            symbols, cancelled_symbols = DicePool([ProficiencyDice(),
                                                   ChallengeDice()]).roll_ascii()
            self.assertEqual(symbols, '\x1b[1m\x1b[33mT\x1b[0m\x1b[1m\x1b[31mD\x1b[0m')
            self.assertEqual(cancelled_symbols, '\x1b[1m\x1b[33mT\x1b[0m\x1b[1m\x1b[31mD\x1b[0m')

    def test_ability_difficulty_second_roll_ascii(self):
        with mock.patch('dice.random.choice', autospec=True, spec_set=True,
                        side_effect=lambda seq: seq[1]):
            symbols, cancelled_symbols = DicePool([AbilityDice(),
                                                   DifficultyDice()]).roll_ascii()
            self.assertEqual(symbols, '\x1b[1m\x1b[32ms\x1b[0m\x1b[1m\x1b[35mf\x1b[0m')
            self.assertEqual(cancelled_symbols, '')

    def test_difficulty_eighth_roll_ascii(self):
        with mock.patch('dice.random.choice', autospec=True, spec_set=True,
                        side_effect=lambda seq: seq[7]):
            symbols, cancelled_symbols = DicePool([DifficultyDice()]).roll_ascii()
            self.assertEqual(symbols, '\x1b[30m\x1b[47mr\x1b[0m\x1b[30m\x1b[47mr\x1b[0m')
            self.assertEqual(cancelled_symbols, '\x1b[30m\x1b[47mr\x1b[0m\x1b[30m\x1b[47mr\x1b[0m')

    def test_str(self):
        self.assertEqual(str(DicePool([ProficiencyDice(), AbilityDice(), SetbackDice()])),
                         '\x1b[1m\x1b[33my\x1b[0m\x1b[1m\x1b[32mg\x1b[0m\x1b[30m\x1b[47mk\x1b[0m')


if __name__ == '__main__':
    unittest.main()
