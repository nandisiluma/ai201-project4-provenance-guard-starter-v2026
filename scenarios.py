"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "False positives",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": [
            "Good day,Unfortunately due to competing priorities, I will not be able to volunteer for the June summit anymore. I apologize for any inconvenience caused and look forward to working with you in the future.",
            "Hello, I am reaching out because a Walmart grocery delivery intended for my residence at Windsor by the Galleria appears to have been mistakenly delivered to your property. The delivery photo shows the items left outside a door labeled “349” in an interior hallway. After reviewing your propertys website and virtual tour, I noticed that the hallway design—including the vertical wall-mounted unit number light—closely matches your building layout, which leads me to believe the delivery was likely made at your community.The order includes multiple grocery bags from Walmart and a large pack of paper products, and it was delivered yesterday at 4:54 pm.",
            "Hi Diana, Thank you for following up with me. I realized that I do not meet the GPA requirement, I have a 3.0/4.0 undergraduate GPA. As such I will not be continuing with my application. Thank you.",
            "Hello CS7 Students, Congratulations again on completing this class! We are so proud of all you've accomplished and can't wait to celebrate with you this Saturday.As part of the ceremony, we will be featuring your profiles in a presentation. This is our way of virtually honoring the traditional walk during graduation. Please visit the presentation slides where you can add your photo and a few personal details. I've completed the first slide with my own details as an example. See you Saturday.",
            "The art of our mindset determines the people we become, directs the way we live and thus what we produce. The Africa before us today is a result of the education engraved in each and every one of our minds. In order for us to change Africa, tapping into her education becomes the primary key.One major arm of our education that is affecting our continent is the discrimination of women and girls.  We are living in a global village now, civilization is dawning on us from all directions and the world requires active participation of all persons in all developmental sectors, regardless of gender. However, african women have been brought up with blinkers to their vision, they lack confidence in their capabilities and are scared to explore because they have been taught that they are not good enough.Today, as an 18 year old girl, who has the world at her disposal, l say no more of that. W can not have our mothers and sisters aspiring to only be stay-at-home mothers. It is high time we let go of yesterdays theories on what we are capable of as women and gain enough courage to dare ourselves. We cannot progress further as a continent when our greater half is being infringed of freedom."],
    },
    {
        "name": "score spread",
                "criterion": 2,
                
                "texts": [
                    "Technology plays an important role in modern education. It helps students learn new skills and access useful information. It also helps teachers share lessons and track student progress. Technology makes learning more engaging and more accessible for everyone. It is important for schools to use technology in a thoughtful way. This helps students prepare for the future and succeed in their careers.",
                    "Okay so — the dog ate my sandwich. Not a metaphor. Actual sandwich, actual dog (Biscuit, a menace). I turned around for ten seconds to answer the door and when I came back there was just a crust and a very guilty face. Dinner was cereal. Again.",
                    "Remote work has changed how many people think about their jobs. It offers flexibility and saves commuting time, but it can also blur the line between work and home. Some people love it. Others miss the office more than they expected, honestly. Companies are still working out what a good balance looks like, and I suspect they will be for a while yet.",
                ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Inputs spread across your score range, so you can check all three
        # labels are actually reachable.
        "texts": [
            "Technology plays an important role in modern education. It helps students learn new skills and access useful information. It also helps teachers share lessons and track student progress. Technology makes learning more engaging and more accessible for everyone. It is important for schools to use technology in a thoughtful way. This helps students prepare for the future and succeed in their careers.",
            "Okay so — the dog ate my sandwich. Not a metaphor. Actual sandwich, actual dog (Biscuit, a menace). I turned around for ten seconds to answer the door and when I came back there was just a crust and a very guilty face. Dinner was cereal. Again.",
            "Remote work has changed how many people think about their jobs. It offers flexibility and saves commuting time, but it can also blur the line between work and home. Some people love it. Others miss the office more than they expected, honestly. Companies are still working out what a good balance looks like, and I suspect they will be for a while yet.",
        ],
    },

    {
        "name": "appeal path",
        "criterion": 4,
        # Five valid submissions. run_eval.py appeals each returned content_id,
        # then also appeals one made-up id, which must error.
        "texts": [
            "Good day, due to competing priorities I will not be able to volunteer for the June summit anymore. I apologize for the inconvenience.",
            "Hi Diana, thank you for following up. I do not meet the GPA requirement, so I will not be continuing with my application.",
            "Okay so, the dog ate my sandwich. Not a metaphor. I turned around for ten seconds and came back to a crust and a guilty face.",
            "Remote work has changed how many people think about their jobs. It offers flexibility, but it can also blur the line between work and home.",
            "Technology plays an important role in modern education. It helps students learn new skills and access useful information.",
        ],
        "appeal": {
            "reasoning": "These are formal emails I wrote myself and the decision is wrong.",
            "unknown_content_id": "eval-does-not-exist",
        },
    },
    {
        "name": "bad input",
        "criterion": 5,
        # Raw request bodies, sent exactly as written. Expect a 4xx with an
        # `error` field for every one, and no label.
        "bodies": [
            {"creator_id": "eval_bad_missing"},                      # no text key
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   \n\t  ", "creator_id": "eval_bad_whitespace"},
            {"text": "word " * 1100, "creator_id": "eval_bad_huge"},  # ~5500 chars, over 5000
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
