# Improving the Star Wars FFG Dice System?

I love this system, I love the narrative aspect and the fact that it has specific dice that represent different facets of events in our universe.

However, in practice, I feel that certain promises are not kept, and that this is not fair, neither for players nor for GMs. This is why we will dissect everything in detail and perhaps propose a new system compatible with the rules but adjusted, or at least allow GMs to better balance their scenarios.

> [!Caution]
> Everyone is different, we all have particular expectations regarding RPGs. The information that follows reflects my own vision of role-playing games, with a good bit of armchair philosophy. You will find here [1](https://ttftcuts.github.io/sw_dice/),[2](https://illuminatinggames.wordpress.com/2014/09/19/star-wars-age-of-rebellion-a-deep-dive-on-dice-probabilities/),[3](http://rpg-design.wikidot.com/evaluation),[4](https://github.com/johnthagen/eote-dice),[5](https://web.archive.org/web/20160522070459/http://maxmahem.net/wp/star-wars-edge-of-the-empire-die-probabilities/) all the work already done by the community, which I warmly thank.
> Writing is not my main skill, I hope what follows will not be too indigestible.

# Introduction

In this article we will see that there is no perfect system in absolute terms. What I seek is a system that supports the creators' intention, the atmosphere, and the fun of the game!

To do this, we will analyze the dice system in detail to see how it integrates with narration and what its limits are.

> [!Important]
> We will address probabilities and some mathematical concepts here. In my opinion, this is essential in this design/reflection phase because any system, whether we want it or not, is purely a mathematical concept. However, the beauty lies in the fact that all these mathematics form a necessary foundation, but one that will fade during the game to make the narration shine. [6](https://www.scientificamerican.com/article/is-the-universe-made-of-math-excerpt/)

## Our Expectations

Our decisions are often based on an intuitive interpretation of our chances of success; our brain constantly arbitrates reality to make choices.

This concept is, in my opinion, extremely important and must be found in RPGs. In the real world, knowing my physical abilities, I know how to estimate if I have good chances of winning an arm wrestling match against my friends during a bet.

My brain arbitrates the situation. Perhaps certain circumstances increase my chances of success? My friend being certainly more muscular, but especially very drunk today.

There are two interesting things:
- We do this arbitration all the time, and it is intrinsic to "intelligent" species and their intuitive functioning to avoid having to "consciously process" everything and save resources.
- Our brain is a false friend, and it is however not extremely precise at this task.

Although I can estimate my chances of success, even being 90% confident, there remains that 10% of failure. There also remains everything I was not aware of that could have biased my estimate.

Every time we make a decision, it is based on our estimation of *chances of success*, as well as *risk* in case of failure, and the *result* of success.

Chances of success, risk, and result are moreover very well represented conceptually with our different colored dice!

## A System Must Be Fair

With the little reflection above, we can define the concept of fairness in a role-playing game.

> [!IMPORTANT]
> A fair system is a system in which a player *knows* how to estimate their chances of success to make the best decisions. It is also a consistent system that matches the expectations and intuitive interpretation of events in the universe.

This concept is very different from intrinsic difficulty. For example, in a zombie RPG, even if I am an athlete, my chances of sneaking through a horde of zombies are low.

This makes sense because the objective and atmosphere are very specific and we want to feel fear and danger; our characters are not necessarily heroes with extraordinary abilities.

In Star Wars, the introduction of the rulebook tells us that we will seek the epic! Grandiose actions and camera acrobatics! And we do not want (in my opinion) that this same roll could lead to definitive death.

In both cases, I must be able to estimate my chances of success. This does not mean that my estimate is correct 100% of the time, but it must work on average, be *fair* for players and their decision-making.

I don't know if this text clearly conveys my thoughts, but it is the cornerstone of the ideas that will follow and *everything* is based on this. Consequently, if you disagree with this, you may find the rest absurd.

## Dice, Events, and Probability

In this chapter, we will observe certain scenarios (dice pools) to study probabilities and see if this corresponds to what we expect, see if it seems fair and balanced to us. This exercise is a bit difficult if taken separately; the most interesting part will come when we compare different dice pools with each other.

### Distribution

Before looking at scenarios in detail, let's look together at the different types of graphs and how to read them.

#### Standard Symbol Distribution

<details>
<summary>These collapsible text bubbles contain the command to generate the graph, this is not interesting for most readers</summary>

```sh
   python3 eote_dice.py -p ggpp plot single -s s
   # -p dice pool
   # plot command to display the graph
   # single, one line per symbol, 1 graph per pool
   # -s s, symbol to display, s for success (s,a,T,D)
```
</details>

![Success Distribution on a ggpp pool](../stats/standard/ggpp-s-single.png "Success Distribution on a ggpp pool")

The bottom axis indicates the number of symbols (here successes) and the curve points show us the probability of obtaining this number of symbols.

In our present case with two green dice and two purple dice, the probability of obtaining *exactly* 1 success is 25%.

The probability values are interesting, but it is also the shape of the curve that gives us enormous information, which we will see later.

> [!Caution]
> We always have a whole number of symbols. 0 or 1 or 2. It is impossible to have half (0.5) symbols. The curve format above does not represent this very well, but it is the most readable when we add multiple lines.

#### Cumulative Symbol Distribution

<details>
<summary>Command</summary>

```sh
   python3 eote_dice.py -a -p ggpp plot single -s s
   # -a, above, activates cumulative probability mode
```
</details>

![Cumulative Success Distribution on a ggpp pool](../stats/standard/ggpp-s-single-above.png "Cumulative Success Distribution on a ggpp pool")

Here we have cumulative probabilities, meaning that the probability at point x=1 corresponds to the probabilities of obtaining 1 *or more* successes. This is very interesting because in the Star Wars system, this tells us what our chances are of succeeding the action.

Here the probability of having 1 net success is 44%.

#### Special Distribution

In the Star Wars system there are 4 main types of dice results:

- Failure **without** advantage (no net success and no net advantage. noted s-/a-)
- Failure **with** advantage (no net success and at least one net advantage. noted s-/a+)
- Success **without** advantage (at least one net success and no net advantage. noted s+/a-)
- Success **with** advantage (at least one net success and at least one net advantage. noted s+/a+)
- Success **with** 3+ advantage (interesting special case for activating certain weapon attributes. noted S+/+3a)
- Success **with** at least one triumph (special case noted s+/T+)

<details>
<summary>Command</summary>

```sh
    python3 eote_dice.py -p ggpp plot combined
   # combined, plot subcommand, to display these 6 result types.
```
</details>

![Special display on a ggpp pool](../stats/standard/ggpp-combined.png "Special display on a ggpp pool")

Here the display shows the probability of each special case. This will be particularly interesting for understanding the "transfer" of probability when modifying the dice pool.

### Patient Zero and the Advantage Curve

I arrive after the battle because many articles have already debated and shown the limitations of the system. However, while playing with dice pools, here is the graph that made me want to push the reasoning further.

<details>
<summary>Command</summary>

```sh
    python3 eote_dice.py -p gggppp -a plot -u 6 single -s a
   # -u, number of upgrades to make
```
</details>

![Cumulative Advantage Distribution on a gggppp pool with 6 upgrades](../stats/standard/gggppp-single-a-u6.png "Cumulative Advantage Distribution on a gggppp pool with 6 upgrades")

Here we display the cumulative probabilities of advantages, starting from a pool of 3 green 3 purple, and making 6 improvements.

Interesting information:

> [!Important]
> - Between 3 green and 3 yellow, there are *no* significant differences in the number of advantages.
> - Adding a die significantly increases the chances of advantages; this is the gap between line groups.
> - The probability of having at least 3 advantages is relatively low (especially since this can be without success, we are only talking about advantages).

Let's continue with the same graph on success distribution.

<details>
<summary>Command</summary>

```sh
    python3 eote_dice.py -a -p gggppp -a plot -u 6 single -s s
```
</details>

![Cumulative Success Distribution on a gggppp pool with 6 upgrades](../stats/standard/gggppp-single-a-u6-above.png "Cumulative Success Distribution on a gggppp pool with 6 upgrades")

> [!Important]
> - A dice improvement adds 5% chance of having at least one net success. (equivalent to +1 in D&D system)
> - An improvement can be made thanks to a destiny point.
> - We still observe the gap of *+10%* when adding a green die.

This information, although interesting, is not reproaches. Again, everything is a question of expectation and balance. We can nevertheless ask ourselves the question: does this seem fair and coherent to us?

We can continue with our special cases, with only 3 upgrades for more clarity.

<details>
<summary>Command</summary>

```sh
    python3 eote_dice.py -p gggppp -a plot -u 3 combined
   # -u, number of upgrades to make
```
</details>

![Special display on a gggppp pool with 3 upgrades](../stats/standard/gggppp-combined-u3.png "Special display on a gggppp pool with 3 upgrades")

> [!Important]
> With 3 yellow and 3 purple:
> - *12%* chance of having at least 1 success and 1 advantage.
> - *1%* chance of having at least 1 success and 3 advantages.
> - *15%* chance of having at least 1 success and 1 triumph.
> - There is therefore more chance of "critical" success than success with 1 advantage.

#### Patient Zero Conclusion

Let's step away from numbers a bit to conceptually explain what we just saw.

> [!Important]
> - Buying skill ranks weakly increases our chances of success.
> - Buying skill ranks does not significantly increase our chances of advantage.
> - Buying skill ranks significantly increases our chances of triumph.

> [!Note]
> The points raised above have been discussed in detail in these posts [2](https://illuminatinggames.wordpress.com/2014/09/19/star-wars-age-of-rebellion-a-deep-dive-on-dice-probabilities/),[7](https://www.reddit.com/r/swrpg/comments/5rnr35/deep_dive_into_dice_probabilities/)

To summarize the linked articles and what we just saw, upgrading a die to yellow only offers chances of triumph. For certain skills like medicine this can be interesting, but on **average** your character will not succeed much better.

Conceptually this bothers me, because the experience of skills symbolized by yellow dice (mainly) should, in my intuitive interpretation, provide greater chances of success or perhaps, less chance that things go wrong, that is to say, more advantage?

There are other things to take into account that we will see later, but this already represents good ground for reflection and we touch here the heart of balancing and especially the heart of personal expectations that I described above (and which are very well defined here [3](http://rpg-design.wikidot.com/evaluation)).

#### Adding Dice

One of the remarks that we have already observed a little is the fact that adding dice always seems much superior in terms of average success.

Let's look at this with blue boost dice.

### The Impact of Blue Dice

In the rules there are several ways to obtain a blue die:

- Spend an advantage during a test, to give a blue die to the next character (valid for several advantages)
- Aim
- Have an environmental or external advantage (can be requested by the player if they show inventiveness)

However, to obtain an additional yellow die upgrade, only the destiny point and spending a triumph are available.

<details>
<summary>Command</summary>

```sh
    python3 eote_dice.py -C -a -p gggbppp -p ggyppp -p gggppp plot compare -s s
```
</details>

![Cumulative Success Distribution on a comparative pool between gggppp, ggyppp and gggbppp](../stats/standard/ppp-compare-g-y-b-u0-above.png "Cumulative Success Distribution on a comparative pool between gggppp, ggyppp and gggbppp")

Here we see that adding a blue die equals upgrading a die in terms of cumulative success.

<details>
<summary>Command</summary>

```sh
    python3 eote_dice.py -C -a -p gggbppp -p ggyppp -p gggppp plot compare -s a
```
</details>

![Cumulative Advantage Distribution on a comparative pool between gggppp, ggyppp and gggbppp](../stats/standard/ppp-compare-g-y-b-u0-above-advantage.png "Cumulative Advantage Distribution on a comparative pool between gggppp, ggyppp and gggbppp")

Here we see that adding a blue die is significantly **better** than upgrading a yellow die in terms of cumulative advantage.

<details>
<summary>Command</summary>

```sh
    python3 eote_dice.py -C -a -p gggbppp -p ggyppp -p gggppp plot combined
```
</details>

![Special display on a comparative pool between gggppp, ggyppp and gggbppp](../stats/standard/ppp-combined-g-y-b-u0.png "Special display on a comparative pool between gggppp, ggyppp and gggbppp")

Here the impact of the blue die is very interesting. It significantly increases the chances of success with advantage and is better in all cases except in the case of triumph.

> [!Note]
> The chances of success with triumph are **5%**, equivalent to rolling a 20 in a d20 system.

Using a triumph to upgrade a die is not profitable. You consume your triumph, which had little chance of occurring, to add 5% chance of triumph.

This then approaches the critical confirmation of old D&D systems, and the probabilities of getting good results on successive rolls are really bad.

It is therefore really preferable to use the triumph for its free/narrative aspect.

Destiny points, which in the rules are supposed to have a big impact, are also not worth using to upgrade dice. It is always preferable to use their free/narrative aspect.

> We see here one of the first limitations: yellow dice are interesting but do not have at all the power accorded to them in the rules.

> [!Note]
> Die size bias: In a certain number of classic systems, we are used to having to roll big numbers. With this, the more faces a die has, the more interesting it is; 1d12 is better than 1d6.
> Here our blue die with 6 faces seems weaker to us than our green die, which seems weaker than our yellow dice, both because in the rules they are described as less impactful, and because of this bias.

### Maxing Skills at Character Creation

A point that regularly comes up in articles is the fact that buying characteristic points is essential and much superior to choosing skills or talent points. Taking into account that only character creation allows this, the question is interesting because it can create big disadvantages and a feeling of injustice in the group in the long term.

Let's take the example of a character who keeps their natural high stat of three in Agility and who takes two ranks of piloting, compared to a character who chooses to put 4 in Agility and who has no piloting ranks.

<details>
<summary>Command</summary>

```sh
    python3 eote_dice.py -C -a -p ggggppp -p gyyppp  plot compare -s s
```
</details>

![Cumulative success distribution on a comparative pool between ggggppp, gyyppp](../stats/standard/ppp-compare-gggg-gyy-u0-above-success.png "Cumulative success distribution on a comparative pool between ggggppp, gyyppp")

Here we observe no significant difference in success distribution (slightly superior for 4 Agility).

<details>
<summary>Command</summary>

```sh
    python3 eote_dice.py -C -a -p ggggppp -p gyyppp  plot compare -s a
```
</details>

![Cumulative advantage distribution on a comparative pool between ggggppp, gyyppp](../stats/standard/ppp-compare-gggg-gyy-u0-above-advantage.png "Cumulative advantage distribution on a comparative pool between ggggppp, gyyppp")

Here we observe that 4 Agility provides significantly more advantages.

<details>
<summary>Command</summary>

```sh
    python3 eote_dice.py -C -a -p ggggppp -p gyyppp  plot combined
```
</details>

![Special distribution on a comparative pool between ggggppp, gyyppp](../stats/standard/ppp-combined-gggg-gyy-u0.png "Special distribution on a comparative pool between ggggppp, gyyppp")

This distribution confirms and refines the above observations.

> [!Important]
> Two yellow dice are less good overall than one green die; they bring some chances of triumph.
> Here the character with 4 Agility is much better in almost all situations. We have looked at skills vs no skills, but it is good to remember that a characteristic is used with 5-10 skills, which makes the characteristic really superior overall.

How to interpret these results? In my opinion, it is strange that a trained character only has more chance of an exceptional miraculous success. Training brings on the contrary stability, precision, know-how that should reduce variance.