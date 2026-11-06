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
    # Criterion 1: of 10 human-written texts, 0 get the high-confidence AI label.
    # All ten are my own writing. The first five were also used to tune the
    # weights in unit 7; the last five were written after, so they are fresh.
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": [
            "I feel very dejected and confused and I dont really like how my life is going on right now.",
            "I just want to put my thoughts out here and see how it goes. I have too many things on my plate right now. I need to worry about my graduation, visa, job and also project It feels like I do not have enough time to do anything. I want to do so many things but I am unable to do anything",
            "K-Pop music is vey popular in the music industry now a days that every other person is aware of it. it is almost surprising how they managed to make their place in this heavily westernized music industry. BTS played a major role in making this happen. They are famously claimed to be paving the way for kpop into western media. They are very talented and acclaimed and deeply recognized with a huge fanbase.",
            "The aim is to build a novel data science system to evaluate applicants for Data Science and Analytics graduate program. The customer is Graduate Admissions department who receive large volume of applications and must review every application to decide whether a candidate is suitable to get admitted to Georgia State University. This entire process is very long and tedious when done manually. The data science system will enable the admissions department to reduce workload, save time in making admissions decisions while ensuring fairness.",
            "For any data science system, the crucial component is data. We need to figure out the relevant sources of data that would help in assessing a candidate and one of the best sources is the official transcript from the applicant’s college or university. The transcripts will contain details like GPA and the coursework they did during their time as a student. This helps to check if the candidate has enough grip on the technical concepts that are required for the Data Science and Analytics program. The next one would be an experience letter from the company if the candidate has working experience. This should not be a mandatory criterion, but it is an added value if the experience is relevant. Thirdly, SOPs (Statement of Purpose) and LORs (Letter of Recommendation). SOPs are a great way to understand an applicant’s goals and passion; it also provides insight into the academic background of them. LORs can be used as an external evaluation of the candidate. We can also ask for the resume of the candidate which will contain information about the projects, internships and research work they did.",
            "We are plannign a trip to texas to attend our friend's wedding. It is just a 2 day trip so we will not need much luggage. Texas has great food so we have to try as many as we can while also exploring the neighborhood.",
            "A short technical assessment which aims to understand the applicant’s skills. It will contain basic questions on data science concepts, logical reasoning and problem-solving questions. I am planning not to put this as a necessary pass criterion.",
            "I plan to use Logistic regression model as we need to make yes or no predictions. Additionally, most of the key inputs are numeric like GPA, Assessment score, time spent on reading the instructions, number of projects and internships, years of experience etc. We can extract keywords from SOPs, LORs, Resume and experience letters and make a relevance to data science field score.",
            "To further strengthen the model, we can use decision trees. Logistic regression solely depends on numeric values and bases its decisions on them, but there will be few cases that are conditional. A person might have low GPA but might have worked on various projects, such a person might be a good fit to do research work and having them as the university’s alumni would increase the reputation.",
            "The developed system can be deployed as an application that can be used by the committee. The system can be triggered every day or as per requirement. It will be provided with all the necessary accesses to pull data from the applications portal. Once it is triggered, it goes to the portal, downloads all the required data it needs, processes the data and makes a decision.",
        ],
    },
    # Criterion 2: the average combined score of 5 clearly-AI texts is at least
    # 0.3 above the average of 5 clearly-human texts.
    {
        "name": "spread: AI texts",
        "criterion": 2,
        "texts": [
            "The Big Bang Theory is the scientific explanation for how the universe began about 13.8 billion years ago. The universe started in an extremely hot and dense state and has been expanding and cooling ever since. Over time, stars, galaxies, and planets formed as matter came together under gravity. Scientists support this theory through evidence such as the expansion of the universe and cosmic microwave background radiation.",
            "Artificial intelligence is transforming the way we live and work. It offers numerous benefits, including increased efficiency, improved decision-making, and enhanced productivity. However, it is important to consider the ethical implications of these technologies. By working together, we can ensure that AI is developed responsibly and benefits everyone.",
            "Bhimavaram is currently experiencing warm, humid conditions with temperatures hovering around 79°F to 82°F (26°C to 28°C). High humidity levels, exceeding 80%, make the air feel noticeably muggier than the actual reading. Gentle to moderate coastal breezes are present, with mostly clear skies overhead and minimal immediate chance of precipitation. Looking ahead, typical October conditions bring daytime highs reaching the mid-80s accompanied by occasional seasonal coastal cloud cover.",
            "Renewable energy is playing an increasingly important role in addressing the challenges of climate change. Solar and wind power offer clean alternatives to fossil fuels, reducing greenhouse gas emissions and improving air quality. In addition, advances in battery technology are making it easier to store energy and deliver it reliably. By investing in these technologies, governments and businesses can build a more sustainable future for generations to come.",
            "Regular exercise is one of the most effective ways to improve overall health and well-being. It strengthens the heart, builds muscle, and supports a healthy weight. Beyond the physical benefits, exercise also reduces stress and improves mood by releasing endorphins. Incorporating even a modest amount of physical activity into your daily routine can lead to lasting improvements in both body and mind.",
        ],
    },
    {
        "name": "spread: human texts",
        "criterion": 2,
        "texts": [
            "We are plannign a trip to texas to attend our friend's wedding. It is just a 2 day trip so we will not need much luggage. Texas has great food so we have to try as many as we can while also exploring the neighborhood.",
            "A short technical assessment which aims to understand the applicant’s skills. It will contain basic questions on data science concepts, logical reasoning and problem-solving questions. I am planning not to put this as a necessary pass criterion.",
            "I plan to use Logistic regression model as we need to make yes or no predictions. Additionally, most of the key inputs are numeric like GPA, Assessment score, time spent on reading the instructions, number of projects and internships, years of experience etc. We can extract keywords from SOPs, LORs, Resume and experience letters and make a relevance to data science field score.",
            "To further strengthen the model, we can use decision trees. Logistic regression solely depends on numeric values and bases its decisions on them, but there will be few cases that are conditional. A person might have low GPA but might have worked on various projects, such a person might be a good fit to do research work and having them as the university’s alumni would increase the reputation.",
            "The developed system can be deployed as an application that can be used by the committee. The system can be triggered every day or as per requirement. It will be provided with all the necessary accesses to pull data from the applications portal. Once it is triggered, it goes to the portal, downloads all the required data it needs, processes the data and makes a decision.",
        ],
    },
    # Criterion 3: each of the three labels is produced by a real submission.
    # Chosen from unit 7 as one text for each: AI, unsure, human.
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            "The Big Bang Theory is the scientific explanation for how the universe began about 13.8 billion years ago. The universe started in an extremely hot and dense state and has been expanding and cooling ever since. Over time, stars, galaxies, and planets formed as matter came together under gravity. Scientists support this theory through evidence such as the expansion of the universe and cosmic microwave background radiation.",
            "Honestly, I didn't expect remote work to change my routine this much. Productivity is up, sure, but so is the loneliness. My manager says flexibility is the future of work, and maybe she's right, though I miss the noise of the old office.",
            "The aim is to build a novel data science system to evaluate applicants for Data Science and Analytics graduate program. The customer is Graduate Admissions department who receive large volume of applications and must review every application to decide whether a candidate is suitable to get admitted to Georgia State University. This entire process is very long and tedious when done manually. The data science system will enable the admissions department to reduce workload, save time in making admissions decisions while ensuring fairness.",
        ],
    },
    # Criterion 4: whenever the two scores differ by more than 0.4, the label is
    # "unsure". A mix of texts with a large gap and a small one.
    {
        "name": "gap rule",
        "criterion": 4,
        "texts": [
            "For any data science system, the crucial component is data. We need to figure out the relevant sources of data that would help in assessing a candidate and one of the best sources is the official transcript from the applicant’s college or university. The transcripts will contain details like GPA and the coursework they did during their time as a student. This helps to check if the candidate has enough grip on the technical concepts that are required for the Data Science and Analytics program. The next one would be an experience letter from the company if the candidate has working experience. This should not be a mandatory criterion, but it is an added value if the experience is relevant. Thirdly, SOPs (Statement of Purpose) and LORs (Letter of Recommendation). SOPs are a great way to understand an applicant’s goals and passion; it also provides insight into the academic background of them. LORs can be used as an external evaluation of the candidate. We can also ask for the resume of the candidate which will contain information about the projects, internships and research work they did.",
            "Honestly, I didn't expect remote work to change my routine this much. Productivity is up, sure, but so is the loneliness. My manager says flexibility is the future of work, and maybe she's right, though I miss the noise of the old office.",
            "I just want to put my thoughts out here and see how it goes. I have too many things on my plate right now. I need to worry about my graduation, visa, job and also project It feels like I do not have enough time to do anything. I want to do so many things but I am unable to do anything",
            "The Big Bang Theory is the scientific explanation for how the universe began about 13.8 billion years ago. The universe started in an extremely hot and dense state and has been expanding and cooling ever since. Over time, stars, galaxies, and planets formed as matter came together under gravity. Scientists support this theory through evidence such as the expansion of the universe and cosmic microwave background radiation.",
        ],
    },
    # Criterion 5 (appeals) can't be tested by sending text alone: it needs a
    # submission and then an appeal against the content_id that came back. I
    # tested it by hand with curl instead of extending run_eval.py; the README
    # says so.
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
